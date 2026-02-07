# Testing Documentation

This document outlines the testing strategy, test cases, and validation procedures for the GRC-TPRM platform.

## Testing Strategy

### 1. Layer-Based Testing
Each layer is tested independently before integration testing:
- **Base Layer**: Eramba functionality validation
- **Intelligence Layer**: Microservice unit and integration tests
- **Experience Layer**: UI/UX and workflow tests

### 2. Test Types
- **Unit Tests**: Individual function/component testing
- **Integration Tests**: Layer-to-layer communication
- **End-to-End Tests**: Complete workflow validation
- **Performance Tests**: Load and stress testing
- **Security Tests**: Vulnerability scanning

## Test Environment

### WSL Testing Environment
```bash
# Environment details
OS: Ubuntu (WSL2)
Docker: Latest stable
Docker Compose: v2.x
```

### Test Data
- Sample vendor records
- Mock questionnaire responses
- Synthetic OSINT data
- Test user accounts with different roles

## Base Layer Tests (Eramba CE)

### Installation Verification

#### Test Case 1.1: Docker Container Status
```bash
# Command
docker ps

# Expected Result
Container 'eramba' should be running
Status: Up X minutes
Port: 0.0.0.0:80->80/tcp
```

**Status**: ⏳ Pending

---

#### Test Case 1.2: Web Interface Access
- **URL**: `http://localhost:80`
- **Expected**: Eramba login page loads
- **Status**: ⏳ Pending

---

#### Test Case 1.3: Initial Setup Wizard
- **Action**: Complete first-time setup
- **Verify**: 
  - Admin account creation
  - Database initialization
  - Default settings applied
- **Status**: ⏳ Pending

---

### Core Functionality Tests

#### Test Case 2.1: Vendor Registry
- **Action**: Add new vendor
- **Input**: Vendor name, contact, domain
- **Expected**: Vendor appears in registry
- **Status**: ⏳ Pending

---

#### Test Case 2.2: Questionnaire Creation
- **Action**: Create risk assessment questionnaire
- **Verify**: 
  - Multiple question types supported
  - Logic/branching works
  - Can assign to vendor
- **Status**: ⏳ Pending

---

#### Test Case 2.3: Evidence Upload
- **Action**: Upload vendor documentation
- **Verify**: File storage and retrieval
- **Status**: ⏳ Pending

---

## Intelligence Layer Tests

### OSINT Service

#### Test Case 3.1: Domain Lookup
```bash
# Test endpoint (when implemented)
curl -X POST http://localhost:5001/api/osint/domain \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'

# Expected Response
{
  "domain": "example.com",
  "registrar": "...",
  "creation_date": "...",
  "reputation_score": ...
}
```

**Status**: ⏳ Pending

---

#### Test Case 3.2: CVE Monitoring
- **Action**: Query CVEs for specific vendor technology
- **Expected**: List of relevant CVEs with severity scores
- **Status**: ⏳ Pending

---

### Risk Scoring Engine

#### Test Case 4.1: Calculate Vendor Risk Score
- **Input**: Vendor profile with various attributes
- **Expected**: Risk score (0-100) with breakdown
- **Status**: ⏳ Pending

---

#### Test Case 4.2: Risk Score Updates
- **Action**: Update vendor information
- **Expected**: Risk score recalculated automatically
- **Status**: ⏳ Pending

---

## Experience Layer Tests

### Dashboard Tests

#### Test Case 5.1: Dashboard Load Time
- **Metric**: Page load under 2 seconds
- **Status**: ⏳ Pending

---

#### Test Case 5.2: Real-Time Updates
- **Action**: Trigger alert in backend
- **Expected**: Dashboard reflects change within 5 seconds
- **Status**: ⏳ Pending

---

### Report Generation

#### Test Case 6.1: Executive Summary
- **Action**: Generate summary for date range
- **Expected**: PDF/HTML report with key metrics
- **Status**: ⏳ Pending

---

## Integration Tests

### End-to-End Workflow

#### Test Case 7.1: Complete Vendor Onboarding
1. Add vendor to Eramba
2. OSINT service enriches vendor data
3. Risk score calculated
4. Questionnaire auto-sent
5. Dashboard shows new vendor
6. Alert triggered for high-risk vendor

**Status**: ⏳ Pending

---

#### Test Case 7.2: Periodic Review Workflow
1. Scheduled review triggered
2. Vendor monitoring checks for changes
3. Risk score updated
4. Notification sent if score changed significantly

**Status**: ⏳ Pending

---

## Performance Tests

### Load Testing

#### Test Case 8.1: Concurrent Vendor Processing
- **Load**: 100 vendors processed simultaneously
- **Metric**: All complete within acceptable time
- **Status**: ⏳ Pending

---

#### Test Case 8.2: Dashboard Under Load
- **Load**: 50 concurrent users
- **Metric**: No degradation in response time
- **Status**: ⏳ Pending

---

## Security Tests

### Vulnerability Scanning

#### Test Case 9.1: Container Security Scan
```bash
# Using Docker Scout or Trivy
docker scout cves eramba/community:latest
```

**Status**: ⏳ Pending

---

#### Test Case 9.2: API Authentication
- **Test**: Attempt access without credentials
- **Expected**: 401 Unauthorized
- **Status**: ⏳ Pending

---

## Manual Testing Checklist

### Pre-Deployment Validation
- [ ] All Docker containers start successfully
- [ ] No errors in container logs
- [ ] All API endpoints respond correctly
- [ ] Database migrations applied
- [ ] Configuration files properly loaded
- [ ] Environment variables set correctly

### User Acceptance Testing
- [ ] Admin can manage vendors
- [ ] Questionnaires can be created and sent
- [ ] Reports generate successfully
- [ ] Alerts are received
- [ ] Dashboard is responsive and accurate

## Testing Commands Reference

### Check All Services
```bash
# Docker containers
docker compose ps

# Service logs
docker compose logs -f

# Test database connection
docker compose exec eramba mysql -u root -p
```

### Run Automated Tests
```bash
# Intelligence layer (when implemented)
cd intelligence-layer
npm test

# Experience layer (when implemented)
cd experience-layer
npm test
```

## Known Issues

### Issue Log
1. **Issue**: [To be filled as issues are discovered]
   - **Severity**: 
   - **Impact**: 
   - **Workaround**: 
   - **Status**: 

## Test Results Summary

| Layer | Total Tests | Passed | Failed | Pending |
|-------|-------------|--------|--------|---------|
| Base Layer | 6 | 0 | 0 | 6 |
| Intelligence Layer | 4 | 0 | 0 | 4 |
| Experience Layer | 4 | 0 | 0 | 4 |
| Integration | 2 | 0 | 0 | 2 |
| Performance | 2 | 0 | 0 | 2 |
| Security | 2 | 0 | 0 | 2 |
| **Total** | **20** | **0** | **0** | **20** |

---

**Testing Guidelines:**
1. Update test status (✅ Pass, ❌ Fail, ⏳ Pending) after each test
2. Document any failures with full error details
3. Re-test after fixes
4. Keep this document updated with new tests as features are added

**Last Updated**: 2026-02-06
