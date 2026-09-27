# GRC-TPRM — project context

**Repo:** `aegis-intel-ops/GRC-TPRM` (public) · branch `main`

Governance, Risk & Compliance / Third-Party Risk Management platform in three layers, each
its own Docker Compose stack. Dev environment is WSL2 (Ubuntu) + Docker.

**Read:** `README.md` (architecture), `PLATFORM_SUMMARY.md`, `USER_GUIDE.md`, per-layer READMEs.

## Layers
| Layer | Path | What |
|---|---|---|
| Base | `eramba/` | Eramba Community Edition (PHP) + MySQL 8.4 + Redis + cron; UI on `${ERAMBA_PORT:-8443}` |
| Intelligence | `intelligence-layer/osint-service/` | FastAPI — `POST /api/enrich` (vendor domain OSINT) |
| | `intelligence-layer/risk-engine/` | FastAPI — `POST /api/calculate` (vendor risk score) |
| Experience | `experience-layer/dashboard/` | React + Vite dashboard (currently mock vendor data) |
| | `experience-layer/reports/` | FastAPI + Jinja2 — `POST /api/generate`, `GET /api/demo` (executive summary) |
| | `experience-layer/workflows/` | n8n |

Each Python service is a single `main.py` with `/health`.

## Run / verify
```bash
cd eramba && docker compose up -d
cd ../intelligence-layer && docker compose up -d
cd ../experience-layer && docker compose up -d
# dashboard without Docker:
cd experience-layer/dashboard && npm install && npm run build   # or npm run dev
```
No automated tests. Checks: dashboard `npm run build` passes; each service imports cleanly
after `pip install -r requirements.txt`. `npm run lint` has 2 known issues in `src/App.jsx`
(unused `axios`, setState in effect for mock data).

## Gotchas
- Root `.gitignore` ignores `*.html` (for generated reports). Source HTML must be whitelisted
  with `!path` entries — that rule once kept `dashboard/index.html` out of git and broke the build.
- `experience-layer/reports/templates/executive_summary.html` is loaded by `reports/main.py` but
  is **not in the repo** yet (same ignore rule) — commit it before relying on the reports service.
- Don't commit Eramba/MySQL/Postgres data dirs or `.env` files (ignored; keep it that way).
