from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    national_id = Column(String)
    phone_number = Column(String)
    province = Column(String)
    city = Column(String)
    land_area_sqm = Column(Float)
    requested_capacity_kw = Column(Float)
    roof_type = Column(String)
    electricity_bill_id = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    notes = Column(Text, nullable=True)
