# n8n Workflow Automation

This directory contains the **n8n** workflow automation setup for the GRC-TPRM platform.

## Overview

n8n is a powerful workflow automation tool that connects different services together. In this platform, it orchestrates:
- Automated vendor onboarding processes
- Periodic vendor reviews and reassessments
- Alert routing and notifications
- Report generation and distribution
- Integration between Eramba, Intelligence Layer, and Experience Layer

## Quick Start

### Start n8n

```bash
cd workflows
docker compose up -d
```

### Access n8n

Open your browser and navigate to:
- **URL**: `http://localhost:5678`
- **Username**: `admin`
- **Password**: `change_this_password` (⚠️ Change this!)

## Default Workflows

### 1. Vendor Onboarding Automation

**Trigger**: New vendor added to Eramba  
**Actions**:
1. Extract vendor domain from Eramba
2. Call OSINT service to enrich vendor data
3. Call risk engine to calculate initial risk score
4. Update Eramba with enriched data
5. Send notification if high risk detected

**Use Case**: Automatically gather intelligence and assess risk when new vendors are added

### 2. Periodic Review Scheduler

**Trigger**: Scheduled (weekly/monthly)  
**Actions**:
1. Query Eramba for vendors due for review
2. Re-run OSINT checks for each vendor
3. Recalculate risk scores
4. Compare with previous scores
5. Generate alerts for significant changes
6. Schedule review meetings for high-risk changes

**Use Case**: Continuous monitoring of vendor risk posture

### 3. Executive Report Generation

**Trigger**: Monthly (first day of month)  
**Actions**:
1. Aggregate all vendor risk scores
2. Call reports service to generate executive PDF
3. Email report to stakeholders
4. Archive report in document storage

**Use Case**: Automated monthly executive reporting

### 4. Alert Routing

**Trigger**: High-risk vendor detected  
**Actions**:
1. Create ticket in Eramba
2. Send email to compliance team
3. Post to Slack/Teams channel
4. Log alert in tracking system

**Use Case**: Immediate notification for critical risk events

## Creating Custom Workflows

### Via UI

1. Access n8n at http://localhost:5678
2. Click "New Workflow"
3. Add nodes from the sidebar
4. Connect nodes to define flow
5. Configure each node
6. Test and activate

### Available Integrations

n8n provides 400+ integrations including:
- **HTTP Request**: Call any REST API
- **Webhook**: Receive HTTP requests
- **Schedule**: Time-based triggers
- **Email**: Send/receive emails
- **Slack/Teams**: Team notifications
- **PostgreSQL/MySQL**: Database operations
- **Code**: Custom JavaScript/Python

### Example: Call OSINT Service

```javascript
// HTTP Request node configuration
{
  "method": "POST",
  "url": "http://grc_osint_service:5001/api/enrich",
  "body": {
    "domain": "{{$json.vendor_domain}}"
  },
  "headers": {
    "Content-Type": "application/json"
  }
}
```

## Workflow Files

Workflows can be exported as JSON files and stored in the `./workflows` directory for version control:

```bash
# Export workflow from n8n UI
Settings → Export

# Save to ./workflows/vendor_onboarding.json
```

## Environment Variables

Configure n8n via environment variables in `docker-compose.yml`:

```yaml
- N8N_BASIC_AUTH_ACTIVE=true    # Enable authentication
- N8N_BASIC_AUTH_USER=admin     # Username
- N8N_BASIC_AUTH_PASSWORD=pass  # Password (CHANGE THIS!)
- WEBHOOK_URL=http://...        # Webhook base URL
```

## Security

### Change Default Password

⚠️ **CRITICAL**: Change the default password before production use!

Edit `docker-compose.yml`:
```yaml
- N8N_BASIC_AUTH_PASSWORD=your_secure_password_here
```

Then restart:
```bash
docker compose restart
```

### API Authentication

For calling intelligence services, configure authentication in HTTP Request nodes.

## Integration Points

### With Eramba (Base Layer)

- **Webhook**: Eramba triggers n8n on vendor events
- **API**: n8n queries Eramba API for vendor data
- **Database**: Direct database read (read-only recommended)

### With Intelligence Layer

- **OSINT Service**: `http://grc_osint_service:5001/api/enrich`
- **Risk Engine**: `http://grc_risk_engine:5002/api/calculate`

### With Experience Layer

- **Reports Service**: `http://grc_reports:5003/api/generate`
- **Dashboard**: Post updates via webhook

## Monitoring

### View Workflow Executions

n8n UI → Executions  
- See all workflow runs
- View input/output data
- Debug failed executions

### Logs

```bash
# View n8n logs
docker compose logs -f n8n

# Check health
curl http://localhost:5678/healthz
```

## Common Use Cases

### 1. Vendor Risk Score Changed

```
Trigger: Scheduled daily
→ Query all vendors from Eramba
→ Calculate new risk scores
→ Compare with yesterday's scores
→ If change > 10 points:
  → Send alert
  → Create review task
```

### 2. New Compliance Certification Added

```
Trigger: Webhook from Eramba
→ Extract vendor ID and certification
→ Recalculate risk score
→ Update vendor record
→ Log certification event
```

### 3. Quarterly Review Automation

```
Trigger: Quarterly (Jan 1, Apr 1, Jul 1, Oct 1)
→ Generate executive report
→ Create review tasks in Eramba
→ Send calendar invites
→ Post reminder in Slack
```

## Troubleshooting

### n8n Won't Start

```bash
# Check logs
docker compose logs n8n

# Common issues:
# - Port 5678 in use: Change in docker-compose.yml
# - Volume permission issues: Check Docker volume permissions
```

### Workflow Not Triggering

1. Check webhook URL is accessible
2. Verify authentication credentials
3. Review execution history for errors
4. Test trigger manually

### Cannot Connect to Services

Ensure you're using Docker service names:
- ✅ `http://grc_osint_service:5001`
- ❌ `http://localhost:5001` (won't work from inside container)

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [Workflow Templates](https://n8n.io/workflows/)

## Next Steps

1. ✅ Change default password
2. ✅ Create vendor onboarding workflow
3. ✅ Configure webhooks from Eramba
4. ✅ Test end-to-end integration
5. ✅ Set up monitoring and alerts

---

**Status**: 🟢 Running  
**Port**: 5678  
**Authentication**: Basic Auth (change password!)
