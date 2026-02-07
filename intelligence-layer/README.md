# Intelligence Layer Services

This directory contains the custom microservices that form the **Intelligence Layer** of the GRC-TPRM platform.

## Services Overview

### 1. OSINT Service (Port 5001)
**Purpose**: Open Source Intelligence gathering for vendor enrichment

**Features**:
- Domain WHOIS lookups
- DNS record retrieval (A, MX, TXT records)
- SSL certificate validation
- Preliminary reputation scoring
- Data breach monitoring integration (planned)

**API Endpoints**:
- `GET /health` - Service health check
- `POST /api/enrich` - Enrich domain with OSINT data

**Example**:
```bash
curl -X POST http://localhost:5001/api/enrich \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

### 2. Risk Engine (Port 5002)
**Purpose**: Automated vendor risk assessment and scoring

**Features**:
- Multi-factor risk calculation
- Weighted scoring algorithm (0-100 scale)
- Risk level classification (Critical/High/Medium/Low/Minimal)
- Actionable recommendations

**Scoring Factors**:
- Company maturity (20 points)
- Security posture (25 points)
- Incident history (25 points)
- Online reputation (15 points)
- Financial health (15 points)

**API Endpoints**:
- `GET /health` - Service health check
- `POST /api/calculate` - Calculate vendor risk score

**Example**:
```bash
curl -X POST http://localhost:5002/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_id": "vendor-001",
    "domain": "example.com",
    "company_age_years": 5,
    "has_ssl": true,
    "breach_count": 0,
    "compliance_certifications": ["ISO27001", "SOC2"]
  }'
```

### 3. Vendor Monitor (Port 5003) - Coming Soon
**Purpose**: Continuous monitoring of vendor security posture

**Planned Features**:
- Scheduled CVE checks
- Domain status monitoring
- Certificate expiration alerts
- Automated risk score updates

## Quick Start

### Start All Intelligence Services

```bash
cd intelligence-layer
docker compose up -d
```

### Check Service Status

```bash
docker compose ps
```

Expected output:
```
NAME                    STATUS      PORTS
grc_intel_postgres      Up          5432/tcp
grc_intel_redis         Up          6379/tcp
grc_osint_service       Up          0.0.0.0:5001->5001/tcp
grc_risk_engine         Up          0.0.0.0:5002->5002/tcp
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f osint-service
docker compose logs -f risk-engine
```

### Test Services

```bash
# OSINT Service
curl http://localhost:5001/health

# Risk Engine
curl http://localhost:5002/health
```

## API Documentation

Each service provides interactive API documentation via FastAPI:

- **OSINT Service**: http://localhost:5001/docs
- **Risk Engine**: http://localhost:5002/docs

## Database

Services share a PostgreSQL database for persistence:
- **Host**: postgres (within Docker network) or localhost:5432 (from host)
- **Database**: intelligence
- **User**: intel_user
- **Password**: See `.env` file (change default!)

## Redis Cache

Shared Redis instance for caching and temporary data:
- **Host**: redis (within Docker network) or localhost:6379 (from host)

## Development

### Adding Dependencies

For Python services (OSINT, Risk Engine):

```bash
# Add to requirements.txt
cd osint-service  # or risk-engine
echo "new-package==1.0.0" >> requirements.txt

# Rebuild container
docker compose build osint-service
docker compose up -d osint-service
```

### Local Development (Without Docker)

```bash
cd osint-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5001
```

## Integration with Eramba

The Intelligence Layer integrates with Eramba base layer through:

1. **API Calls**: React dashboard calls intelligence services
2. **Scheduled Jobs**: Periodic vendor enrichment
3. **Webhooks**: Event-driven updates (planned)

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker compose logs service-name

# Common issues:
# - Port already in use: Change port in docker-compose.yml
# - Database not ready: Wait for postgres health check to pass
```

### Database Connection Issues

```bash
# Verify PostgreSQL is running
docker compose exec postgres pg_isready -U intel_user

# Connect to database
docker compose exec postgres psql -U intel_user -d intelligence
```

### Reset Everything

```bash
# Stop and remove all containers, networks, volumes
docker compose down -v

# Rebuild and start fresh
docker compose up -d --build
```

## Security Notes

- **Change default passwords** in `.env` before production
- **Use environment variables** for all secrets
- **Enable HTTPS** for production deployments
- **Implement API authentication** before exposing publicly

## Next Steps

- [ ] Add vendor monitor service
- [ ] Implement authentication/API keys
- [ ] Add database migrations
- [ ] Set up monitoring and alerting
- [ ] Integrate with Eramba API
