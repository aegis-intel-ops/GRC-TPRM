# GRC-TPRM Experience Layer

The **Experience Layer** provides premium user experience components for the GRC-TPRM platform.

## Components

### 1. Premium Dashboard (Port 5173)
- **Technology**: React 18 + Vite
- **Features**:
  - Real-time vendor risk metrics
  - Interactive charts (pie, bar)
  - Vendor overview table
  - Responsive design
  - Modern gradient UI

### 2. Executive Reports (Port 5003)
- **Technology**: Python/FastAPI + WeasyPrint
- **Features**:
  - PDF/HTML report generation
  - Executive summaries
  - Risk distribution metrics
  - Professional templates

### 3. Workflow Automation (Port 5678)
- **Technology**: n8n
- **Features**:
  - Visual workflow builder
  - Automated vendor onboarding
  - Periodic reviews
  - Alert routing

## Quick Start

```bash
# Start all Experience Layer services
docker compose up -d

# Start individual services
cd workflows && docker compose up -d  # n8n
cd reports && docker compose up -d    # Reports service

# Start dashboard (dev mode)
cd dashboard && npm install && npm run dev
```

## Access Points

- **Dashboard**: http://localhost:5173
- **Reports API**: http://localhost:5003/docs
- **n8n Workflows**: http://localhost:5678

## Documentation

- Dashboard: `./dashboard/README.md`
- Reports: `./reports/main.py` (see docstrings)
- Workflows: `./workflows/README.md`

## Integration

All Experience Layer services integrate with:
- **Base Layer** (Eramba): Vendor data source
- **Intelligence Layer**: OSINT & Risk scoring APIs

---

**Status**: ✅ All components ready  
**Last Updated**: 2026-02-06
