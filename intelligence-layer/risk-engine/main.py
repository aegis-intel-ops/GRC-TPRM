from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Risk Scoring Engine",
    description="Automated vendor risk assessment and scoring",
    version="1.0.0"
)

class RiskLevel(str, Enum):
    """Risk level classification"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"

class VendorRiskFactors(BaseModel):
    """Input factors for risk calculation"""
    vendor_id: str
    domain: str
    company_age_years: Optional[int] = Field(None, ge=0, description="Age of company in years")
    employee_count: Optional[int] = Field(None, ge=0)
    has_ssl: bool = Field(True, description="Has valid SSL certificate")
    breach_count: int = Field(0, ge=0, description="Number of known data breaches")
    cve_count: int = Field(0, ge=0, description="Number of known CVEs")
    compliance_certifications: List[str] = Field(default_factory=list, description="e.g., ISO27001, SOC2, PCI-DSS")
    domain_reputation_score: Optional[int] = Field(None, ge=0, le=100, description="From OSINT service")
    financial_health_score: Optional[int] = Field(None, ge=0, le=100)
    incident_history_score: Optional[int] = Field(None, ge=0, le=100)

class RiskScoreResponse(BaseModel):
    """Risk assessment response"""
    vendor_id: str
    overall_risk_score: int = Field(..., ge=0, le=100, description="Lower = riskier, Higher = safer")
    risk_level: RiskLevel
    risk_factors: Dict[str, int]
    recommendations: List[str]
    calculated_at: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "risk-engine",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/calculate", response_model=RiskScoreResponse)
async def calculate_risk_score(factors: VendorRiskFactors):
    """
    Calculate comprehensive risk score for a vendor
    
    Risk score ranges from 0-100:
    - 0-20: Critical risk
    - 21-40: High risk
    - 41-60: Medium risk
    - 61-80: Low risk
    - 81-100: Minimal risk
    """
    try:
        logger.info(f"Calculating risk score for vendor: {factors.vendor_id}")
        
        # Initialize score breakdown
        risk_factors = {}
        
        # 1. Company maturity (max 20 points)
        maturity_score = calculate_maturity_score(factors.company_age_years, factors.employee_count)
        risk_factors["company_maturity"] = maturity_score
        
        # 2. Security posture (max 25 points)
        security_score = calculate_security_score(factors.has_ssl, factors.compliance_certifications)
        risk_factors["security_posture"] = security_score
        
        # 3. Breach and incident history (max 25 points)
        incident_score = calculate_incident_score(factors.breach_count, factors.cve_count)
        risk_factors["incident_history"] = incident_score
        
        # 4. Domain and online reputation (max 15 points)
        reputation_score = factors.domain_reputation_score or 50
        reputation_score = int((reputation_score / 100) * 15)
        risk_factors["online_reputation"] = reputation_score
        
        # 5. Financial health (max 15 points)
        financial_score = factors.financial_health_score or 50
        financial_score = int((financial_score / 100) * 15)
        risk_factors["financial_health"] = financial_score
        
        # Calculate overall score
        overall_score = sum(risk_factors.values())
        
        # Determine risk level
        risk_level = determine_risk_level(overall_score)
        
        # Generate recommendations
        recommendations = generate_recommendations(factors, risk_factors, overall_score)
        
        return RiskScoreResponse(
            vendor_id=factors.vendor_id,
            overall_risk_score=overall_score,
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendations=recommendations,
            calculated_at=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error calculating risk score: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating risk: {str(e)}")

def calculate_maturity_score(company_age: Optional[int], employee_count: Optional[int]) -> int:
    """Calculate company maturity score (0-20)"""
    score = 0
    
    # Age scoring (0-12 points)
    if company_age:
        if company_age >= 10:
            score += 12
        elif company_age >= 5:
            score += 8
        elif company_age >= 2:
            score += 5
        else:
            score += 2
    else:
        score += 5  # Neutral if unknown
    
    # Employee count scoring (0-8 points)
    if employee_count:
        if employee_count >= 500:
            score += 8
        elif employee_count >= 100:
            score += 6
        elif employee_count >= 20:
            score += 4
        else:
            score += 2
    else:
        score += 3  # Neutral if unknown
    
    return min(score, 20)

def calculate_security_score(has_ssl: bool, certifications: List[str]) -> int:
    """Calculate security posture score (0-25)"""
    score = 0
    
    # SSL certificate (0-5 points)
    if has_ssl:
        score += 5
    
    # Compliance certifications (0-20 points)
    cert_scores = {
        "ISO27001": 7,
        "SOC2": 7,
        "PCI-DSS": 6,
        "HIPAA": 6,
        "GDPR": 5,
        "FedRAMP": 8,
    }
    
    for cert in certifications:
        cert_upper = cert.upper().replace(" ", "").replace("-", "")
        for key, value in cert_scores.items():
            if key.replace("-", "") in cert_upper:
                score += value
                break
    
    return min(score, 25)

def calculate_incident_score(breach_count: int, cve_count: int) -> int:
    """Calculate incident history score (0-25)"""
    # Start from full score and deduct for incidents
    score = 25
    
    # Deduct for breaches (more severe)
    score -= min(breach_count * 8, 18)  # Max 18 point deduction
    
    # Deduct for CVEs (less severe)
    score -= min(cve_count * 2, 7)  # Max 7 point deduction
    
    return max(score, 0)

def determine_risk_level(score: int) -> RiskLevel:
    """Determine risk level from overall score"""
    if score <= 20:
        return RiskLevel.CRITICAL
    elif score <= 40:
        return RiskLevel.HIGH
    elif score <= 60:
        return RiskLevel.MEDIUM
    elif score <= 80:
        return RiskLevel.LOW
    else:
        return RiskLevel.MINIMAL

def generate_recommendations(factors: VendorRiskFactors, risk_factors: Dict[str, int], overall_score: int) -> List[str]:
    """Generate actionable recommendations based on risk assessment"""
    recommendations = []
    
    if overall_score <= 40:
        recommendations.append("🚨 HIGH PRIORITY: Conduct immediate security audit before proceeding")
    
    if risk_factors["security_posture"] < 15:
        recommendations.append("Request security certification documentation (ISO27001, SOC2)")
    
    if not factors.has_ssl:
        recommendations.append("⚠️ No SSL certificate detected - verify data transmission security")
    
    if factors.breach_count > 0:
        recommendations.append(f"Review {factors.breach_count} past data breach(es) and remediation measures")
    
    if factors.cve_count > 5:
        recommendations.append(f"High CVE count ({factors.cve_count}) - verify patch management processes")
    
    if risk_factors["company_maturity"] < 10:
        recommendations.append("Young company - consider more frequent reviews")
    
    if len(factors.compliance_certifications) == 0:
        recommendations.append("No compliance certifications found - request evidence of security practices")
    
    if overall_score >= 80:
        recommendations.append("✅ Low risk vendor - standard monitoring recommended")
    
    if not recommendations:
        recommendations.append("Maintain regular monitoring and periodic reassessment")
    
    return recommendations

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Risk Scoring Engine",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/api/calculate",
            "/docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
