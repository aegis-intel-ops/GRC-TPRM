# GRC-TPRM Platform - Architecture Documentation

## Executive Summary

The GRC-TPRM (Governance, Risk, Compliance - Third-Party Risk Management) platform is a hybrid solution that combines open-source foundations with custom intelligence and experience layers to provide comprehensive vendor risk management capabilities.

## System Architecture

### Three-Layer Hybrid Design

```
┌─────────────────────────────────────────────────────────┐
│          EXPERIENCE LAYER (Premium UX)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │   Dashboard  │  │   Reports    │  │   Workflows   │ │
│  │   (React)    │  │  (Python)    │  │     (n8n)     │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │ REST APIs
                          ▼
┌─────────────────────────────────────────────────────────┐
│       INTELLIGENCE LAYER (Custom Microservices)          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │    OSINT     │  │ Risk Engine  │  │ Vendor Monitor│ │
│  │   Service    │  │              │  │               │ │
│  │  (Port 5001) │  │  (Port 5002) │  │  (Port 5003)  │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
│          │                  │                  │         │
│          └──────────┬───────┴──────────┬──────┘         │
│                     ▼                   ▼               │
│           ┌──────────────┐    ┌──────────────┐         │
│           │  PostgreSQL  │    │    Redis     │         │
│           └──────────────┘    └──────────────┘         │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │ API / Database
                          ▼
┌─────────────────────────────────────────────────────────┐
│          BASE LAYER (Eramba Community Edition)           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Eramba Web Application              │   │
│  │         (Port 8443 - HTTPS)                      │   │
│  └──────────────────────────────────────────────────┘   │
│          │                                  │            │
│          ▼                                  ▼            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    MySQL     │  │    Redis     │  │  Cron Jobs   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Layer Details

### 1. Base Layer - Eramba Community Edition

**Purpose**: Foundation for GRC processes

**Components**:
- **Eramba Web App**: PHP-based GRC platform
- **MySQL**: Database for vendor registry, questionnaires, audits
- **Redis**: Session and cache management
- **Cron**: Scheduled jobs and background tasks

**Key Features**:
- Vendor registry management
- Risk registers and controls
- Questionnaire creation and management
- Evidence collection and storage
- Complete audit trails
- Compliance framework mapping
- Periodic review scheduling

**Access**: `https://localhost:8443`

**Technology Stack**:
- PHP/CakePHP Framework
- Apache Web Server
- MySQL 8.4
- Redis 7.4

### 2. Intelligence Layer - Custom Microservices

**Purpose**: Automated intelligence gathering and risk assessment

#### 2.1 OSINT Service (Port 5001)

**Function**: Open Source Intelligence enrichment

**Capabilities**:
- **WHOIS Lookups**: Domain registration information
- **DNS Analysis**: A, MX, TXT records retrieval
- **SSL Certificate Validation**: Security posture assessment
- **Domain Reputation Scoring**: Preliminary risk indicators
- **Data Breach Monitoring**: Historical breach detection (planned)

**API Endpoints**:
```
GET  /health          - Health check
POST /api/enrich      - Domain enrichment
GET  /docs            - OpenAPI documentation
```

**Technology**:
- Python 3.11
- FastAPI framework
- python-whois library
- dnspython for DNS queries

#### 2.2 Risk Scoring Engine (Port 5002)

**Function**: Automated vendor risk assessment

**Scoring Algorithm** (0-100 scale):
- **Company Maturity** (20 points):
  - Company age (12 pts)
  - Employee count (8 pts)
- **Security Posture** (25 points):
  - SSL certificate (5 pts)
  - Compliance certifications (20 pts)
- **Incident History** (25 points):
  - Data breaches (deduct up to 18 pts)
  - CVE count (deduct up to 7 pts)
- **Online Reputation** (15 points):
  - From OSINT service
- **Financial Health** (15 points):
  - External financial data (planned)

**Risk Levels**:
- 0-20: **CRITICAL** 🔴
- 21-40: **HIGH** 🟠
- 41-60: **MEDIUM** 🟡
- 61-80: **LOW** 🟢
- 81-100: **MINIMAL** ✅

**API Endpoints**:
```
GET  /health          - Health check
POST /api/calculate   - Calculate risk score
GET  /docs            - OpenAPI documentation
```

**Technology**:
- Python 3.11
- FastAPI framework
- Pydantic for data validation

#### 2.3 Vendor Monitor (Port 5003) - Planned

**Function**: Continuous vendor monitoring

**Planned Features**:
- Scheduled CVE checks (daily)
- Domain status monitoring
- Certificate expiration alerts
- Automated risk score updates
- Alert generation and routing

**Technology Stack** (Intelligence Layer):
- PostgreSQL 16: Persistent storage
- Redis 7.4: Caching and session storage
- Docker Compose: Service orchestration

### 3. Experience Layer - Premium UX

**Purpose**: Enhanced user experience and automation

#### 3.1 Premium Dashboard (Planned)

**Features**:
- Real-time vendor risk visualization
- Interactive charts and graphs
- Vendor detail modals
- Alert notifications
- Risk trend analysis

**Technology**:
- React 18
- Vite build tool
- Chart.js/Recharts
- TailwindCSS or CSS Modules

#### 3.2 Executive Reports (Planned)

**Features**:
- Auto-generated PDF/HTML reports
- Customizable templates
- Branding support
- Executive summary formatting
- Trend analysis

**Technology**:
- Python (ReportLab/WeasyPrint)
- Jinja2 templates
- Chart generation

#### 3.3 Workflow Orchestration (Planned)

**Features**:
- Automated vendor onboarding
- Periodic review scheduling
- Alert routing and escalation
- Email/Slack notifications
- Multi-step approval workflows

**Technology**:
- n8n (self-hosted)
- Visual workflow builder
- Integration connectors

## Data Flow

### Vendor Onboarding Flow

```
1. Vendor Added to Eramba
   ↓
2. Webhook/API trigger to Intelligence Layer
   ↓
3. OSINT Service enriches vendor data
   - WHOIS lookup
   - DNS analysis
   - SSL check
   ↓
4. Risk Engine calculates score
   - Combines OSINT data
   - Applies scoring algorithm
   - Generates recommendations
   ↓
5. Results stored in PostgreSQL
   ↓
6. Dashboard displays enriched vendor profile
   ↓
7. Workflow triggers based on risk level
   - High risk → Immediate review
   - Medium risk → Quarterly review
   - Low risk → Annual review
```

### Periodic Review Flow

```
1. Cron job triggers review (Eramba)
   ↓
2. Vendor Monitor checks for changes
   - Domain status
   - New CVEs
   - Breach databases
   ↓
3. Risk Engine recalculates score
   ↓
4. If score changed significantly:
   - Alert generated
   - Notification sent
   - Review scheduled
```

## Deployment Architecture

### Development Environment (Current)

All services run on localhost via Docker Compose:
- **Eramba**: `https://localhost:8443`
- **OSINT Service**: `http://localhost:5001`
- **Risk Engine**: `http://localhost:5002`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

### Production Deployment (Planned)

**Option 1: Single Server**
- All containers on one VPS
- Nginx reverse proxy
- SSL certificates (Let's Encrypt)
- Domain-based routing

**Option 2: Distributed**
- Eramba on dedicated server
- Intelligence Layer on separate server
- Shared database server
- Load balancing

## Security Considerations

### Authentication & Authorization
- Eramba: Built-in user management
- Intelligence Layer: API key authentication (to implement)
- Dashboard: SSO integration (planned)

### Data Protection
- SSL/TLS for all communication
- Database encryption at rest
- Secrets management via environment variables
- Regular backups

### Network Security
- Docker network isolation
- Firewall rules
- Rate limiting on APIs
- DDoS protection

## Scalability

### Horizontal Scaling
- Intelligence services: Multiple instances behind load balancer
- PostgreSQL: Read replicas for reporting
- Redis: Cluster mode for high availability

### Vertical Scaling
- Increase container resources as needed
- Database optimization and indexing
- Caching strategies

## Monitoring & Logging

### Health Monitoring
- Service health endpoints
- Container health checks
- Database connection monitoring

### Logging Strategy
- Centralized logging (planned)
- ELK stack or similar
- Log retention policies

### Metrics (Planned)
- API request rates
- Response times
- Error rates
- Resource utilization

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|----------|
| **Base Layer** |
| Eramba | PHP/CakePHP | Latest | GRC Platform |
| MySQL | MySQL | 8.4.3 | Database |
| Redis | Redis | 7.4.2 | Cache |
| **Intelligence Layer** |
| OSINT Service | Python/FastAPI | 3.11/0.115 | Intelligence |
| Risk Engine | Python/FastAPI | 3.11/0.115 | Risk Scoring |
| PostgreSQL | PostgreSQL | 16 | Data Store |
| Redis | Redis | 7.4.2 | Cache |
| **Experience Layer** |
| Dashboard | React/Vite | 18/Latest | UI |
| Reports | Python | 3.11 | PDF Generation |
| Workflows | n8n | Latest | Automation |
| **Infrastructure** |
| Container Runtime | Docker | 29.1.5 | Containerization |
| Orchestration | Docker Compose | 5.0.1 | Service Management |
| OS | Ubuntu (WSL) | Latest | Development Environment |

## API Contracts

### OSINT Service API

```json
POST /api/enrich
Request:
{
  "domain": "example.com"
}

Response:
{
  "domain": "example.com",
  "whois_data": {
    "registrar": "Example Registrar",
    "creation_date": "2020-01-01",
    "expiration_date": "2026-01-01"
  },
  "dns_records": {
    "A": ["93.184.216.34"],
    "MX": ["mail.example.com"]
  },
  "reputation_score": 85,
  "last_updated": "2026-02-06T19:10:00Z"
}
```

### Risk Engine API

```json
POST /api/calculate
Request:
{
  "vendor_id": "vendor-001",
  "domain": "example.com",
  "company_age_years": 5,
  "has_ssl": true,
  "breach_count": 0,
  "compliance_certifications": ["ISO27001", "SOC2"]
}

Response:
{
  "vendor_id": "vendor-001",
  "overall_risk_score": 78,
  "risk_level": "low",
  "risk_factors": {
    "company_maturity": 16,
    "security_posture": 19,
    "incident_history": 25,
    "online_reputation": 13,
    "financial_health": 5
  },
  "recommendations": [
    "✅ Low risk vendor - standard monitoring recommended"
  ],
  "calculated_at": "2026-02-06T19:10:00Z"
}
```

## Future Enhancements

1. **Machine Learning Integration**
   - Predictive risk modeling
   - Anomaly detection
   - Natural language processing for questionnaires

2. **Additional Integrations**
   - CRM systems (Salesforce, HubSpot)
   - Security tools (SIEM, vulnerability scanners)
   - Communication platforms (Slack, Teams)

3. **Advanced Analytics**
   - Vendor risk trends over time
   - Industry benchmarking
   - Portfolio risk analysis

4. **Mobile Application**
   - iOS/Android apps
   - Push notifications
   - Quick approvals

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-06  
**Status**: ✅ Core architecture implemented
