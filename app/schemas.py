from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# اسکیمای داده‌های ورودی فرم
class SolarApplicantCreate(BaseModel):
    full_name: str
    national_id: str
    phone_number: str
    province: str
    city: str
    land_area_sqm: Optional[float] = 0.0
    requested_capacity_kw: Optional[float] = 0.0
    roof_type: Optional[str] = ""
    electricity_bill_id: Optional[str] = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = ""

# اسکیمای داده‌های خروجی و پاسخ سرور
class SolarApplicantResponse(BaseModel):
    id: int
    full_name: str
    national_id: str
    phone_number: str
    province: str
    city: str
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
