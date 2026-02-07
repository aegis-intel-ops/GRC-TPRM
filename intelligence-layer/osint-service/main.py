from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import httpx
import whois
import dns.resolver
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OSINT Enrichment Service",
    description="Open Source Intelligence gathering for vendor risk assessment",
    version="1.0.0"
)

class DomainEnrichRequest(BaseModel):
    """Request model for domain enrichment"""
    domain: str = Field(..., description="Domain name to enrich", example="example.com")

class DomainEnrichResponse(BaseModel):
    """Response model for domain enrichment"""
    domain: str
    whois_data: Optional[Dict[str, Any]] = None
    dns_records: Optional[Dict[str, Any]] = None
    ssl_info: Optional[Dict[str, Any]] = None
    reputation_score: Optional[int] = Field(None, ge=0, le=100)
    last_updated: str

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "osint-enrichment",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/enrich", response_model=DomainEnrichResponse)
async def enrich_domain(request: DomainEnrichRequest):
    """
    Enrich a domain with OSINT data
    
    - Performs WHOIS lookup
    - Retrieves DNS records
    - Checks SSL certificate status
    - Calculates preliminary reputation score
    """
    try:
        logger.info(f"Enriching domain: {request.domain}")
        
        # Get WHOIS data
        whois_data = get_whois_data(request.domain)
        
        # Get DNS records
        dns_records = get_dns_records(request.domain)
        
        # Get SSL info (simplified)
        ssl_info = {"status": "Not implemented yet"}
        
        # Calculate reputation score (simplified algorithm)
        reputation_score = calculate_reputation_score(whois_data, dns_records)
        
        return DomainEnrichResponse(
            domain=request.domain,
            whois_data=whois_data,
            dns_records=dns_records,
            ssl_info=ssl_info,
            reputation_score=reputation_score,
            last_updated=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error enriching domain {request.domain}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error enriching domain: {str(e)}")

def get_whois_data(domain: str) -> Optional[Dict[str, Any]]:
    """Retrieve WHOIS data for a domain"""
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date) if w.creation_date else None,
            "expiration_date": str(w.expiration_date) if w.expiration_date else None,
            "name_servers": w.name_servers if w.name_servers else [],
            "status": w.status if w.status else None,
        }
    except Exception as e:
        logger.warning(f"WHOIS lookup failed for {domain}: {str(e)}")
        return {"error": str(e)}

def get_dns_records(domain: str) -> Optional[Dict[str, Any]]:
    """Retrieve DNS records for a domain"""
    try:
        dns_data = {}
        
        # Get A records
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            dns_data['A'] = [str(r) for r in a_records]
        except:
            dns_data['A'] = []
        
        # Get MX records
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            dns_data['MX'] = [str(r) for r in mx_records]
        except:
            dns_data['MX'] = []
        
        # Get TXT records
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            dns_data['TXT'] = [str(r) for r in txt_records]
        except:
            dns_data['TXT'] = []
        
        return dns_data
    except Exception as e:
        logger.warning(f"DNS lookup failed for {domain}: {str(e)}")
        return {"error": str(e)}

def calculate_reputation_score(whois_data: Optional[Dict], dns_data: Optional[Dict]) -> int:
    """
    Calculate a basic reputation score (0-100)
    Higher score = better reputation
    """
    score = 50  # Start from neutral
    
    if whois_data and "error" not in whois_data:
        # Has valid WHOIS data
        score += 20
        
        # Check domain age (simplified)
        if whois_data.get("creation_date"):
            score += 10
    
    if dns_data and "error" not in dns_data:
        # Has valid DNS configuration
        if dns_data.get("A"):
            score += 10
        if dns_data.get("MX"):
            score += 5
        if dns_data.get("TXT"):
            score += 5
    
    # Ensure score is within bounds
    return max(0, min(100, score))

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OSINT Enrichment Service",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/api/enrich",
            "/docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
