# IntegrAI Ops

> AI-powered integration monitoring and incident resolution platform.

IntegrAI Ops is a full-stack, production-style application that monitors
simulated e-commerce integrations across Order, Inventory and Payment services.
When transactions fail, an AI investigation assistant analyses the root cause
using MCP tools, recommends a resolution and guides the operator through a
human-in-the-loop approval workflow before any remediation action is taken.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React · TypeScript · Vite · React Router · Axios |
| Backend | Python · FastAPI · Pydantic · SQLAlchemy · Alembic |
| Database | PostgreSQL (local via Docker · production on Neon) |
| AI | Gemini API (primary) · Ollama (optional local provider) |
| MCP | Model Context Protocol · Python MCP SDK |
| Auth | JWT · bcrypt |
| Testing | Pytest · Vitest · Postman · Newman |
| Infrastructure | Docker · Docker Compose · GitHub Actions |
| Deployment | Vercel (frontend) · Railway (backend) · Neon (database) |

---

## Project Status

| Phase | Description | Status |
|---|---|---|
| 1 | Planning and repository setup | ✅ In Progress |
| 2 | FastAPI foundation | 🔲 Not started |
| 3 | Integration services | 🔲 Not started |
| 4 | MCP server and tools | 🔲 Not started |
| 5 | AI agent | 🔲 Not started |
| 6 | Approval and remediation | 🔲 Not started |
| 7 | React frontend | 🔲 Not started |
| 8 | Testing and infrastructure | 🔲 Not started |
| 9 | Deployment | 🔲 Not started |
| 10 | Portfolio completion | 🔲 Not started |

---

## Repository Structure

integrai-ops/

├── backend/          # FastAPI application, MCP server, migrations, tests

├── frontend/         # React + TypeScript application

├── postman/          # Postman collection and environment files

├── scripts/          # Utility and seed scripts

├── docs/             # Architecture, decisions and deployment documentation

├── .github/          # GitHub Actions workflows and PR template

├── docker-compose.yml

└── .env.example

---

## Quick Start (local development)

> Full setup instructions will be added in Phase 2 once the application
> foundation is implemented.

Prerequisites:
- Docker and Docker Compose
- Python 3.12+ (confirm version compatibility before use)
- Node 20 LTS (confirm version compatibility before use)
- uv (Python package manager — confirm availability before use)
- pnpm (Node package manager — confirm availability before use)

```bash
# Clone the repository
git clone https://github.com/DK-Manish/integrai-ops.git
cd integrai-ops

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your values before continuing

# Start the full local stack
docker compose up
```

---

## Documentation

| Document | Location |
|---|---|
| Architecture | [docs/architecture.md](docs/architecture.md) |
| Technical decisions | [docs/decisions.md](docs/decisions.md) |
| Risks and mitigations | [docs/risks.md](docs/risks.md) |
| Deployment guide | [docs/deployment.md](docs/deployment.md) |
| Postman guide | [postman/README.md](postman/README.md) |

---

## Licence

MIT — see [LICENSE](LICENSE) for details.