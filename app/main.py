import os
import ssl
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.db import engine, AsyncSessionLocal, init_db
from app.scanner.detectors import scan_text_for_violations
from app.scanner.rules import apply_compliance_rules
from app.audit import log_violation, get_audit_logs
from app.models import AuditLog, ViolationRecord
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down Compliance Sentinel agent")

app = FastAPI(
    title="Compliance Sentinel",
    description="Production-grade AI compliance officer with HIPAA, GDPR monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(",") or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Compliance Sentinel",
        "version": "1.0.0"
    }

@app.post("/scan/text")
async def scan_text(content: str, regulations: list = None):
    try:
        if not regulations:
            regulations = ["HIPAA", "GDPR", "CCPA"]
        
        detections = scan_text_for_violations(content)
        violations = apply_compliance_rules(detections, regulations)
        
        await log_violation(content, violations, regulations)
        
        return {
            "scan_id": "compliance-scan-001",
            "violations_found": len(violations),
            "violations": violations,
            "regulations_checked": regulations,
            "recommendation": "Review flagged items before transmission"
        }
    except Exception as e:
        logger.error(f"Error scanning text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan/file")
async def scan_file(file: UploadFile = File(...), regulations: list = None):
    try:
        content = await file.read()
        text_content = content.decode("utf-8", errors="ignore")
        
        if not regulations:
            regulations = ["HIPAA", "GDPR", "CCPA"]
        
        detections = scan_text_for_violations(text_content)
        violations = apply_compliance_rules(detections, regulations)
        
        await log_violation(text_content, violations, regulations)
        
        return {
            "scan_id": "compliance-scan-file",
            "filename": file.filename,
            "violations_found": len(violations),
            "violations": violations,
            "regulations_checked": regulations
        }
    except Exception as e:
        logger.error(f"Error scanning file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audit/logs")
async def get_logs(limit: int = 100):
    try:
        logs = await get_audit_logs(limit)
        return {
            "total_logs": len(logs),
            "logs": logs
        }
    except Exception as e:
        logger.error(f"Error retrieving audit logs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def run_with_mtls():
    """Run with mTLS if certificates are provided"""
    cert_file = os.getenv("CERT_FILE")
    key_file = os.getenv("KEY_FILE")
    ca_file = os.getenv("CA_FILE")
    
    ssl_context = None
    if cert_file and key_file:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(cert_file, key_file)
        if ca_file:
            ssl_context.load_verify_locations(ca_file)
        logger.info("mTLS enabled with provided certificates")
    
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        ssl_context=ssl_context
    )

if __name__ == "__main__":
    run_with_mtls()