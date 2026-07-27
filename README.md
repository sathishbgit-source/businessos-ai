# BusinessOS AI

A production-grade AI SaaS platform built using a modern monorepo architecture.

## Repository Structure

```
businessos-ai/
├── apps/
│   ├── api/
│   ├── web/
│   └── worker/
├── packages/
├── modules/
├── infrastructure/
├── docs/
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── Makefile
├── package.json
└── pyproject.toml
```

## Tech Stack

### Backend
- Python 3.13
- FastAPI (planned)
- uv
- Ruff
- MyPy
- Pytest

### Frontend
- Node.js 22 LTS
- npm Workspaces
- Next.js (planned)
- TypeScript (planned)

### Infrastructure
- Docker
- PostgreSQL
- Redis

## Development

```bash
make help
```

## Project Status

- ✅ PR-001 — Repository & Monorepo Initialization
- 🚧 PR-002 — Development Toolchain
- ⏳ PR-003 — Backend Foundation
- ⏳ PR-004 — Frontend Foundation

## License

MIT