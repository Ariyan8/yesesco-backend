from pydantic import BaseModel
from typing import Optional

class ApplicantCreate(BaseModel):
    full_name: str
    national_id: str
    phone_number: str
    province: str
    city: str
    land_area_sqm: float
    requested_capacity_kw: float
    roof_type: str
    electricity_bill_id: Optional[str] = None
    latitude: float
    longitude: float
    notes: Optional[str] = None
