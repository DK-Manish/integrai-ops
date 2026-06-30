
## Phase 2 — Open Decisions Resolved

### OD-01 — Refresh token browser storage

**Decision:** Option A — HttpOnly, Secure, SameSite=Strict cookie.

**Rationale:** The refresh token is never exposed to JavaScript, eliminating XSS-based theft of the long-lived credential. The access token remains a short-lived JWT returned in the response body and held in frontend memory only. CORS will be configured with an explicit allowed origin and `credentials: true` to support this.

**Alternative considered:** localStorage. Rejected — readable by any script on the page, so a single XSS vulnerability anywhere in the frontend compromises the refresh token.

### OD-02 — Python 3.12 compatibility

**Decision:** Confirmed. FastAPI, SQLAlchemy 2.x and Alembic fully support Python 3.12. The official MCP Python SDK requires Python 3.10+ and recommends 3.12+. Local environment confirmed: Python 3.12.4.

**Note for Phase 4:** pin `mcp>=1.27,<2` to stay on the stable v1.x release line, since v2 is in active pre-release development.

### OD-04 — uv availability

**Decision:** Confirmed. `uv 0.11.26` installed and working locally via the official Astral install script.

