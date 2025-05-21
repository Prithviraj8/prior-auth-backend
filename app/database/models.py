from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from .base import Base
from ..models.user import User  # Import User model


class AuthRequest(Base):
    __tablename__ = "auth_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_name = Column(String, nullable=False)
    patient_dob = Column(String, nullable=False)
    insurance_provider = Column(String, nullable=False)
    procedure_code = Column(String, nullable=False)
    diagnosis_code = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDING")
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    notes = Column(Text)


class User(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 