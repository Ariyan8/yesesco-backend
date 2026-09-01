from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SolarApplicantCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    national_id: str = Field(..., min_length=10, max_length=10)
    phone_number: str = Field(..., min_length=10, max_length=15)
    province: Optional[str] = "البرز"
    city: Optional[str] = "کرج"
    land_area_sqm: Optional[float] = 0.0
    requested_capacity_kw: Optional[float] = 0.0
    roof_type: Optional[str] = "سوله صنعتی"
    electricity_bill_id: Optional[str] = ""
    latitude: Optional[float] = 35.8327
    longitude: Optional[float] = 50.9915
    notes: Optional[str] = ""

class SolarApplicantResponse(BaseModel):
    id: int
    full_name: str
    national_id: str
    phone_number: str
    province: Optional[str] = None
    city: Optional[str] = None
    land_area_sqm: Optional[float] = None
    requested_capacity_kw: Optional[float] = None
    roof_type: Optional[str] = None
    electricity_bill_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = "در حال بررسی"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
