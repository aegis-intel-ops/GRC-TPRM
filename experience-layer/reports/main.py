from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
import httpx
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Executive Reports Service",
    description="Automated report generation for vendor risk assessments",
    version="1.0.0"
)

# Jinja2 template environment
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class VendorSummary(BaseModel):
    """Vendor information for report"""
    vendor_id: str
    vendor_name: str
    domain: str
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    last_assessment: str

class ReportRequest(BaseModel):
    """Report generation request"""
    report_title: str = Field(default="Vendor Risk Assessment Report")
    report_period: str = Field(default="Q1 2026")
    vendors: List[VendorSummary]
    include_charts: bool = Field(default=True)
    format: str = Field(default="pdf", pattern="^(pdf|html)$")

class ReportMetrics(BaseModel):
    """Overall metrics for the report"""
    total_vendors: int
    critical_risk: int
    high_risk: int
    medium_risk: int
    low_risk: int
    minimal_risk: int
    average_risk_score: float

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "executive-reports",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/generate")
async def generate_report(request: ReportRequest):
    """
    Generate an executive summary report
    
    Returns PDF or HTML based on format parameter
    """
    try:
        logger.info(f"Generating {request.format} report: {request.report_title}")
        
        # Calculate metrics
        metrics = calculate_metrics(request.vendors)
        
        # Prepare template data
        template_data = {
            "title": request.report_title,
            "period": request.report_period,
            "generated_date": datetime.now().strftime("%B %d, %Y"),
            "vendors": request.vendors,
            "metrics": metrics,
            "include_charts": request.include_charts
        }
        
        # Render HTML template
        template = env.get_template('executive_summary.html')
        html_content = template.render(**template_data)
        
        if request.format == "html":
            return HTMLResponse(content=html_content)
        
        # Generate PDF
        pdf_buffer = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        
        filename = f"vendor_risk_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/api/demo")
async def generate_demo_report():
    """Generate a demo report with sample data"""
    demo_vendors = [
        VendorSummary(
            vendor_id="V001",
            vendor_name="TechCorp Solutions",
            domain="techcorp.com",
            risk_score=85,
            risk_level="minimal",
            last_assessment="2026-02-01"
        ),
        VendorSummary(
            vendor_id="V002",
            vendor_name="DataSecure Inc",
            domain="datasecure.io",
            risk_score=72,
            risk_level="low",
            last_assessment="2026-02-03"
        ),
        VendorSummary(
            vendor_id="V003",
            vendor_name="CloudSystems LLC",
            domain="cloudsys.net",
            risk_score=45,
            risk_level="medium",
            last_assessment="2026-02-05"
        ),
        VendorSummary(
            vendor_id="V004",
            vendor_name="LegacyTech Partners",
            domain="legacytech.com",
            risk_score=28,
            risk_level="high",
            last_assessment="2026-02-06"
        ),
    ]
    
    request = ReportRequest(
        report_title="Q1 2026 Vendor Risk Assessment",
        report_period="January - March 2026",
        vendors=demo_vendors,
        format="html"
    )
    
    return await generate_report(request)

def calculate_metrics(vendors: List[VendorSummary]) -> ReportMetrics:
    """Calculate overall metrics from vendor list"""
    total = len(vendors)
    
    # Count by risk level
    risk_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "minimal": 0
    }
    
    total_score = 0
    for vendor in vendors:
        risk_level = vendor.risk_level.lower()
        if risk_level in risk_counts:
            risk_counts[risk_level] += 1
        total_score += vendor.risk_score
    
    avg_score = total_score / total if total > 0 else 0
    
    return ReportMetrics(
        total_vendors=total,
        critical_risk=risk_counts["critical"],
        high_risk=risk_counts["high"],
        medium_risk=risk_counts["medium"],
        low_risk=risk_counts["low"],
        minimal_risk=risk_counts["minimal"],
        average_risk_score=round(avg_score, 1)
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Executive Reports Service",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/api/generate",
            "/api/demo",
            "/docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003)
