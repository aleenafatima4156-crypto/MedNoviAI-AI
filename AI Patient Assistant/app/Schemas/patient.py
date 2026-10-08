from typing import List, Optional
from pydantic import BaseModel, Field


class PatientInput(BaseModel):
    patient_name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=120)
    gender: Optional[str] = None

    symptoms: List[str] = Field(default_factory=list)

    duration: Optional[str] = None
    severity: Optional[str] = None

    additional_information: Optional[str] = None

    conversation_id: Optional[str] = None

class PatientAnalysis(BaseModel):
    symptoms: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)

    urgency_level: str = "unknown"

    recommended_specialties: List[str] = Field(default_factory=list)

    patient_summary: str = ""

class ChatRequest(BaseModel):
    conversation_id: str
    message: str = Field(min_length=1)

class SymptomMessage(BaseModel):
    conversation_id: str
    message: str = Field(min_length=1)