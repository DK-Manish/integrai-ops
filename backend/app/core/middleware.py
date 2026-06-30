import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

CORRELATION_ID_HEADER = "X-Correlation-ID"


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Attach a correlation ID to every request and include it in the response headers.

    The ID is taken from the incoming X-Correlation-ID header if present (so upstream
    callers can trace a request across services), or generated fresh if not.
    Every log record emitted during the request lifetime will include this ID.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        correlation_id = request.headers.get(CORRELATION_ID_HEADER) or str(uuid.uuid4())

        # Attach to the request state so route handlers can access it if needed
        request.state.correlation_id = correlation_id

        # Inject into the logging context for this request
        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs) -> logging.LogRecord:
            record = old_factory(*args, **kwargs)
            record.correlation_id = correlation_id
            return record

        logging.setLogRecordFactory(record_factory)

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        finally:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            # Restore the original factory after the request completes
            logging.setLogRecordFactory(old_factory)

            logger.info(
                "request completed",
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "path": str(request.url.path),
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
            )

        response.headers[CORRELATION_ID_HEADER] = correlation_id
        return response