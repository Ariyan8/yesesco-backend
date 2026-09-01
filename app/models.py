from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class SolarApplicant(Base):
    __tablename__ = "solar_applicants"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    national_id = Column(String(10), nullable=False, index=True)
    phone_number = Column(String(15), nullable=False, index=True)
    province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    land_area_sqm = Column(Float, nullable=True, default=0.0)
    requested_capacity_kw = Column(Float, nullable=True, default=0.0)
    roof_type = Column(String(100), nullable=True)
    electricity_bill_id = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    notes = Column(String(500), nullable=True)
    status = Column(String(50), default="در حال بررسی")
    created_at = Column(DateTime(timezone=True), default=utc_now)
