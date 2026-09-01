from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicantCreate(BaseModel):
    full_name: str
    phone_number: str
    province: Optional[str] = None
    city: Optional[str] = None
    service_type: Optional[str] = None
    description: Optional[str] = None

class ApplicantResponse(ApplicantCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
