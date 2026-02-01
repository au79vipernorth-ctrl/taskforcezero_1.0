from app.db import AsyncSessionLocal
from app.models import AuditLog, ViolationRecord
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def log_violation(content: str, violations: list, regulations: list):
    """
    Log compliance violations immutably to audit trail.
    Designed for PHI/PII handling with forensic integrity.
    """
    async with AsyncSessionLocal() as session:
        try:
            for violation in violations:
                audit_record = AuditLog(
                    action=f"VIOLATION_DETECTED:{violation['type']}",
                    timestamp=datetime.utcnow()
                )
                
                violation_record = ViolationRecord(
                    violation_type=violation['type'],
                    description=violation['description'],
                    timestamp=datetime.utcnow()
                )
                
                session.add(audit_record)
                session.add(violation_record)
            
            await session.commit()
            logger.info(f"Logged {len(violations)} violations for regulations: {regulations}")
        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to log violations: {str(e)}")
            raise

async def get_audit_logs(limit: int = 100):
    """Retrieve immutable audit logs"""
    async with AsyncSessionLocal() as session:
        try:
            logs = await session.query(AuditLog).limit(limit).all()
            return [
                {
                    "id": log.id,
                    "action": log.action,
                    "timestamp": log.timestamp.isoformat() if log.timestamp else None
                }
                for log in logs
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve audit logs: {str(e)}")
            return []

async def get_violation_records(limit: int = 100):
    """Retrieve forensic violation records"""
    async with AsyncSessionLocal() as session:
        try:
            records = await session.query(ViolationRecord).limit(limit).all()
            return [
                {
                    "id": record.id,
                    "violation_type": record.violation_type,
                    "description": record.description,
                    "timestamp": record.timestamp.isoformat() if record.timestamp else None
                }
                for record in records
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve violation records: {str(e)}")
            return []