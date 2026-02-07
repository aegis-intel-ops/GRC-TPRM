# GRC-TPRM Platform - User Guide & Testing Manual

**Version**: 1.0  
**Last Updated**: February 6, 2026  
**Platform**: Windows 11 with WSL2 (Ubuntu)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Guide](#installation-guide)
3. [Starting the Platform](#starting-the-platform)
4. [Testing Each Layer](#testing-each-layer)
5. [Using the Platform](#using-the-platform)
6. [Troubleshooting](#troubleshooting)
7. [Stopping Services](#stopping-services)

---

## Prerequisites

### ✅ Already Installed
- ✅ Windows 11 with WSL2 (Ubuntu)
- ✅ Docker Desktop (version 29.1.5)
- ✅ Docker Compose (version 5.0.1)
- ✅ Git (version 2.43.0)
- ✅ Node.js and npm (for dashboard)

### ✅ Repository Cloned
Your code is already at: `C:\Users\kmlal\GRC-TPRM`

---

## Installation Guide

### Step 1: Verify WSL and Docker

Open **PowerShell** and run:

```powershell
# Check WSL
wsl --list --verbose

# Check Docker
wsl bash -c "docker --version"
wsl bash -c "docker compose version"
```

**Expected Output**:
```
Docker version 29.1.5
Docker Compose version v5.0.1
```

### Step 2: Navigate to Project Directory

```powershell
cd C:\Users\kmlal\GRC-TPRM
```

---

## Starting the Platform

### Option A: Start All Services (Recommended for Testing)

#### 1. Start Base Layer (Eramba)

```powershell
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/eramba && docker compose up -d"
```

**Wait Time**: 2-3 minutes for initialization

#### 2. Start Intelligence Layer

```powershell
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/intelligence-layer && docker compose up -d"
```

**Wait Time**: 30-60 seconds

#### 3. Start n8n Workflow Automation

```powershell
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer/workflows && docker compose up -d"
```

**Wait Time**: 30-60 seconds

#### 4. (Optional) Start Reports Service

```powershell
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer && docker compose up -d reports"
```

#### 5. (Optional) Start Dashboard

```powershell
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer/dashboard && npm install && npm run dev"
```

### Option B: Quick Start Script

Create a file `start-all.ps1`:

```powershell
Write-Host "Starting GRC-TPRM Platform..." -ForegroundColor Green

Write-Host "`n[1/3] Starting Base Layer (Eramba)..." -ForegroundColor Cyan
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/eramba && docker compose up -d"

Write-Host "`n[2/3] Starting Intelligence Layer..." -ForegroundColor Cyan
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/intelligence-layer && docker compose up -d"

Write-Host "`n[3/3] Starting Workflow Automation..." -ForegroundColor Cyan
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer/workflows && docker compose up -d"

Write-Host "`n✅ All services started! Waiting for initialization..." -ForegroundColor Green
Start-Sleep -Seconds 30

Write-Host "`nChecking service health..." -ForegroundColor Cyan
wsl bash -c "docker ps --format 'table {{.Names}}\t{{.Status}}'"

Write-Host "`n🚀 Platform is ready!" -ForegroundColor Green
Write-Host "`nAccess points:" -ForegroundColor Yellow
Write-Host "  Eramba: https://localhost:8443"
Write-Host "  OSINT API: http://localhost:5001/docs"
Write-Host "  Risk Engine: http://localhost:5002/docs"
Write-Host "  n8n: http://localhost:5678"
```

Run it:
```powershell
.\start-all.ps1
```

---

## Testing Each Layer

### 🧪 Test 1: Verify All Containers Are Running

```powershell
wsl bash -c "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
```

**Expected Output**: 9 containers running
- `eramba`
- `eramba_mysql`
- `eramba_redis`
- `eramba_cron`
- `grc_osint_service`
- `grc_risk_engine`
- `grc_intel_postgres`
- `grc_intel_redis`
- `grc_n8n`

✅ **PASS**: All 9 containers show "Up"  
❌ **FAIL**: See [Troubleshooting](#troubleshooting)

---

### 🧪 Test 2: Base Layer - Eramba

#### Access Eramba Web Interface

1. Open browser: **https://localhost:8443**
2. **Accept SSL warning** (self-signed certificate)
3. You should see the **Eramba login page**

**First Time Setup**:
- Follow the setup wizard
- Create admin account
- Configure database settings

✅ **PASS**: Eramba login page loads  
❌ **FAIL**: Check container logs: `wsl bash -c "docker logs eramba"`

#### Test Database Connection

```powershell
wsl bash -c "docker exec eramba_mysql mysql -u eramba -pChange_Eramba_Password_123 -e 'SHOW DATABASES;'"
```

✅ **PASS**: Shows list of databases including `eramba`  
❌ **FAIL**: Check MySQL is running

---

### 🧪 Test 3: Intelligence Layer - OSINT Service

#### Test Health Endpoint

```powershell
wsl bash -c "curl -s http://localhost:5001/health"
```

**Expected Output**:
```json
{"status":"healthy","service":"osint-enrichment","timestamp":"2026-02-06T..."}
```

✅ **PASS**: Returns healthy status  
❌ **FAIL**: Check logs: `wsl bash -c "docker logs grc_osint_service"`

#### Test Domain Enrichment (Interactive API)

1. Open browser: **http://localhost:5001/docs**
2. You'll see the **Swagger/OpenAPI interface**
3. Click **POST /api/enrich** → **Try it out**
4. Enter test data:
   ```json
   {
     "domain": "google.com"
   }
   ```
5. Click **Execute**

**Expected Response**:
```json
{
  "domain": "google.com",
  "whois_data": { ... },
  "dns_records": { ... },
  "reputation_score": 85,
  "last_updated": "..."
}
```

✅ **PASS**: Returns enriched domain data  
❌ **FAIL**: Check service logs

#### Test from Command Line

```powershell
wsl bash -c "curl -X POST http://localhost:5001/api/enrich -H 'Content-Type: application/json' -d '{\"domain\":\"example.com\"}'"
```

---

### 🧪 Test 4: Intelligence Layer - Risk Engine

#### Test Health Endpoint

```powershell
wsl bash -c "curl -s http://localhost:5002/health"
```

**Expected Output**:
```json
{"status":"healthy","service":"risk-engine","timestamp":"2026-02-06T..."}
```

#### Test Risk Calculation (Interactive API)

1. Open browser: **http://localhost:5002/docs**
2. Click **POST /api/calculate** → **Try it out**
3. Enter test data:
   ```json
   {
     "vendor_id": "TEST-001",
     "domain": "example.com",
     "company_age_years": 5,
     "employee_count": 100,
     "has_ssl": true,
     "breach_count": 0,
     "cve_count": 2,
     "compliance_certifications": ["ISO27001", "SOC2"],
     "domain_reputation_score": 85,
     "financial_health_score": 75
   }
   ```
4. Click **Execute**

**Expected Response**:
```json
{
  "vendor_id": "TEST-001",
  "overall_risk_score": 78,
  "risk_level": "low",
  "risk_factors": {
    "company_maturity": 16,
    "security_posture": 25,
    "incident_history": 23,
    "online_reputation": 13,
    "financial_health": 11
  },
  "recommendations": [...]
}
```

✅ **PASS**: Returns calculated risk score  
❌ **FAIL**: Check service logs

---

### 🧪 Test 5: Experience Layer - n8n Workflows

#### Access n8n Interface

1. Open browser: **http://localhost:5678**
2. **Login**:
   - Username: `admin`
   - Password: `change_this_password`
3. You should see the **n8n workflow builder**

✅ **PASS**: n8n dashboard loads  
❌ **FAIL**: Check logs: `wsl bash -c "docker logs grc_n8n"`

#### Create Test Workflow

1. Click **"New Workflow"**
2. Add a **Schedule Trigger** node
3. Add an **HTTP Request** node
4. Configure HTTP Request:
   - Method: GET
   - URL: `http://grc_osint_service:5001/health`
5. Click **"Execute Node"**

**Expected**: Health check response shown

✅ **PASS**: Workflow executes successfully  
❌ **FAIL**: Check service connectivity

---

### 🧪 Test 6: Experience Layer - Reports Service (Optional)

#### Start Reports Service

```powershell
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer/reports && docker build -t grc-reports . && docker run -d -p 5003:5003 --name grc_reports grc-reports"
```

#### Test Health Endpoint

```powershell
wsl bash -c "curl -s http://localhost:5003/health"
```

#### Generate Demo Report

1. Open browser: **http://localhost:5003/docs**
2. Click **GET /api/demo** → **Try it out** → **Execute**
3. You should see an **HTML report** in the response

**Or download as file**:
```powershell
wsl bash -c "curl http://localhost:5003/api/demo > demo_report.html"
```

Open `demo_report.html` in browser to view

✅ **PASS**: Report generates successfully  
❌ **FAIL**: Check WeasyPrint dependencies

---

### 🧪 Test 7: Experience Layer - Dashboard (Optional)

#### Start Dashboard

```powershell
cd experience-layer\dashboard
npm install
npm run dev
```

#### Access Dashboard

1. Open browser: **http://localhost:5173**
2. You should see the **premium dashboard** with:
   - Risk metric cards
   - Pie chart (risk distribution)
   - Bar chart (vendor scores)
   - Vendor table

✅ **PASS**: Dashboard loads with charts  
❌ **FAIL**: Check console for errors

---

## Using the Platform

### Workflow 1: Add a New Vendor to Eramba

1. **Login to Eramba**: https://localhost:8443
2. Navigate to **Third Parties** → **Add Vendor**
3. Enter vendor details:
   - Name: "Test Vendor Inc"
   - Domain: "testvendor.com"
   - Contact info, etc.
4. Save the vendor

### Workflow 2: Enrich Vendor with OSINT Data

1. **Get vendor domain**: `testvendor.com`
2. **Call OSINT API**:
   ```powershell
   wsl bash -c "curl -X POST http://localhost:5001/api/enrich -H 'Content-Type: application/json' -d '{\"domain\":\"testvendor.com\"}'"
   ```
3. **Review the response**:
   - WHOIS data
   - DNS records
   - Reputation score

### Workflow 3: Calculate Vendor Risk Score

1. **Prepare vendor data** (from Eramba + OSINT)
2. **Call Risk Engine**:
   ```powershell
   wsl bash -c "curl -X POST http://localhost:5002/api/calculate -H 'Content-Type: application/json' -d '{\"vendor_id\":\"V001\",\"domain\":\"testvendor.com\",\"company_age_years\":3,\"employee_count\":50,\"has_ssl\":true,\"breach_count\":0,\"cve_count\":0,\"compliance_certifications\":[\"ISO27001\"],\"domain_reputation_score\":80,\"financial_health_score\":70}'"
   ```
3. **Review risk score** and recommendations
4. **Update Eramba** with risk level

### Workflow 4: Generate Executive Report

1. **Access Reports API**: http://localhost:5003/docs
2. **Use POST /api/generate** endpoint
3. **Provide vendor list**:
   ```json
   {
     "report_title": "Q1 2026 Vendor Risk Report",
     "report_period": "January - March 2026",
     "vendors": [
       {
         "vendor_id": "V001",
         "vendor_name": "Test Vendor Inc",
         "domain": "testvendor.com",
         "risk_score": 75,
         "risk_level": "low",
         "last_assessment": "2026-02-06"
       }
     ],
     "format": "pdf"
   }
   ```
4. **Download PDF** or view HTML

### Workflow 5: Automate with n8n

1. **Access n8n**: http://localhost:5678
2. **Create workflow**: "Vendor Onboarding Automation"
3. **Add nodes**:
   - Webhook (trigger on new vendor)
   - HTTP Request → OSINT Service
   - HTTP Request → Risk Engine
   - Email (send notification if high risk)
4. **Activate workflow**
5. **Test** by adding vendor to Eramba

---

## Troubleshooting

### Problem: Containers Won't Start

**Symptoms**: `docker compose up -d` fails

**Solutions**:

1. **Check Docker is running**:
   ```powershell
   wsl bash -c "docker ps"
   ```

2. **Check ports are available**:
   ```powershell
   netstat -ano | findstr "8443"
   netstat -ano | findstr "5001"
   ```

3. **Check logs**:
   ```powershell
   wsl bash -c "docker compose logs"
   ```

4. **Restart Docker Desktop**

### Problem: Eramba Shows SSL Error

**Symptoms**: Browser won't connect to https://localhost:8443

**Solutions**:

1. **Wait 2-3 minutes** for Eramba to fully initialize
2. **Accept self-signed certificate** in browser:
   - Chrome: Click "Advanced" → "Proceed to localhost"
   - Edge: Click "Advanced" → "Continue to localhost"
3. **Check container is running**:
   ```powershell
   wsl bash -c "docker logs eramba"
   ```

### Problem: OSINT/Risk Engine Returns Errors

**Symptoms**: API calls return 500 errors

**Solutions**:

1. **Check service logs**:
   ```powershell
   wsl bash -c "docker logs grc_osint_service"
   wsl bash -c "docker logs grc_risk_engine"
   ```

2. **Restart service**:
   ```powershell
   wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/intelligence-layer && docker compose restart osint-service"
   ```

3. **Check database connection**:
   ```powershell
   wsl bash -c "docker exec grc_intel_postgres pg_isready"
   ```

### Problem: n8n Won't Load

**Symptoms**: http://localhost:5678 times out

**Solutions**:

1. **Wait for startup** (can take 30-60 seconds)
2. **Check health**:
   ```powershell
   wsl bash -c "curl http://localhost:5678/healthz"
   ```
3. **Check logs**:
   ```powershell
   wsl bash -c "docker logs grc_n8n"
   ```

### Problem: Dashboard Won't Start

**Symptoms**: `npm run dev` fails

**Solutions**:

1. **Install dependencies**:
   ```powershell
   cd experience-layer\dashboard
   npm install
   ```

2. **Check Node.js version**:
   ```powershell
   node --version  # Should be v18 or higher
   ```

3. **Clear cache and reinstall**:
   ```powershell
   rm -rf node_modules package-lock.json
   npm install
   ```

### Problem: Port Already in Use

**Symptoms**: "Port 5001 is already allocated"

**Solutions**:

1. **Find process using port**:
   ```powershell
   netstat -ano | findstr "5001"
   ```

2. **Kill process** (replace PID):
   ```powershell
   taskkill /PID <PID> /F
   ```

3. **Or change port** in `docker-compose.yml`

---

## Stopping Services

### Stop All Services

```powershell
# Stop Eramba
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/eramba && docker compose down"

# Stop Intelligence Layer
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/intelligence-layer && docker compose down"

# Stop n8n
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer/workflows && docker compose down"

# Stop Dashboard (Ctrl+C in terminal)
```

### Quick Stop Script

Create `stop-all.ps1`:

```powershell
Write-Host "Stopping GRC-TPRM Platform..." -ForegroundColor Yellow

wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/eramba && docker compose down"
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/intelligence-layer && docker compose down"
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer/workflows && docker compose down"

Write-Host "✅ All services stopped" -ForegroundColor Green
```

### Stop and Remove All Data (Fresh Start)

⚠️ **WARNING**: This deletes all data!

```powershell
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/eramba && docker compose down -v"
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/intelligence-layer && docker compose down -v"
wsl bash -c "cd /mnt/c/Users/kmlal/GRC-TPRM/experience-layer/workflows && docker compose down -v"
```

---

## Quick Reference Card

### Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Eramba | https://localhost:8443 | Setup wizard |
| OSINT API | http://localhost:5001/docs | None |
| Risk Engine | http://localhost:5002/docs | None |
| n8n | http://localhost:5678 | admin / change_this_password |
| Reports | http://localhost:5003/docs | None |
| Dashboard | http://localhost:5173 | None |

### Useful Commands

```powershell
# Check all containers
wsl bash -c "docker ps"

# Check logs for a service
wsl bash -c "docker logs <container_name>"

# Restart a service
wsl bash -c "cd <service_dir> && docker compose restart"

# View service health
wsl bash -c "curl http://localhost:5001/health"
wsl bash -c "curl http://localhost:5002/health"
wsl bash -c "curl http://localhost:5678/healthz"
```

### Support

- **Documentation**: See `README.md`, `ARCHITECTURE.md`
- **API Docs**: http://localhost:5001/docs, http://localhost:5002/docs
- **GitHub**: git@github.com:aegis-intel-ops/GRC-TPRM.git

---

**Last Updated**: February 6, 2026  
**Platform Version**: 1.0  
**Testing Status**: ✅ All layers tested and operational
