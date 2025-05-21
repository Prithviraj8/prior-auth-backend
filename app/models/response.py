from pydantic import BaseModel
from typing import Optional, Dict, Union


class FieldData(BaseModel):
    value: Optional[str]
    confidence: float
    is_missing: bool
    source_file: Optional[str]


class FormExtractionResponse(BaseModel):
    patient_info: Dict[str, FieldData]
    procedure_info: Dict[str, FieldData]
    diagnosis_info: Dict[str, FieldData]
    medical_justification: FieldData
    insurance_info: Dict[str, FieldData]
    processing_metadata: Dict[str, Union[str, int]]
