from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BYTEA
from pgvector.sqlalchemy import Vector
import datetime

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='audit_logs')  # Assuming User model exists

class ViolationRecord(Base):
    __tablename__ = 'violation_records'

    id = Column(Integer, primary_key=True)
    violation_type = Column(String(255))
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    forensic_data = Column(Vector(1536))  # or whatever dimension you need
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='violation_records')  # Assuming User model exists
