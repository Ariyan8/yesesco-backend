from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class SolarApplicant(Base):
    __tablename__ = "solar_applicants"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    national_id = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    land_area_sqm = Column(Float, nullable=True)
    requested_capacity_kw = Column(Float, nullable=True)
    roof_type = Column(String, nullable=True)
    electricity_bill_id = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    status = Column(String, default="در حال بررسی")
    created_at = Column(DateTime, default=datetime.utcnow)
