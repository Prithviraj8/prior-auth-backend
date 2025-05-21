from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class AuthRequestCreate(BaseModel):
    patient_name: str
    patient_id: str
    procedure_code: str
    procedure_description: str
    diagnosis_code: str
    diagnosis_description: str
    medical_justification: str
    priority: str = "Standard"  # Can be "Standard", "Urgent", or "Emergency"
    payer_name: Optional[str] = None
    payer_id: Optional[str] = None
    provider_id: UUID


class AuthRequestResponse(BaseModel):
    id: UUID
    patient_name: str
    patient_id: str
    procedure_code: str
    procedure_description: str
    diagnosis_code: str
    diagnosis_description: str
    medical_justification: str
    priority: str
    payer_name: Optional[str]
    payer_id: Optional[str]
    status: str
    submitted_at: datetime
    updated_at: datetime
    provider_id: UUID

    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility
        orm_mode = True  # Required for older versions of Pydantic 