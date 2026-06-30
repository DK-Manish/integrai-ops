import logging
import sys
from typing import Any

from app.core.config import get_settings


class JSONFormatter(logging.Formatter):
    """Format log records as single-line JSON objects for structured log ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        import json
        import traceback

        log_object: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S")
                + f".{int(record.msecs):03d}Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Include correlation ID if set by the middleware
        if hasattr(record, "correlation_id"):
            log_object["correlation_id"] = record.correlation_id

        # Include extra fields attached via logger.info(..., extra={...})
        for key, value in record.__dict__.items():
            if key not in {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "message",
                "correlation_id", "taskName",
            }:
                log_object[key] = value

        if record.exc_info:
            log_object["exception"] = traceback.format_exception(*record.exc_info)

        import json
        return json.dumps(log_object, default=str)


def setup_logging() -> None:
    """Configure structured JSON logging for the application.
    Call once at application startup."""
    settings = get_settings()

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Suppress noisy third-party loggers at WARNING level
    for noisy in ("uvicorn.access", "sqlalchemy.engine", "asyncpg"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger. Use this throughout the app instead of logging.getLogger directly."""
    return logging.getLogger(name)