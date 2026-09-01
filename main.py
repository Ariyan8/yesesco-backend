from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from models import Applicant
from schemas import ApplicantCreate, ApplicantResponse

app = FastAPI(
    title="YesESCo Backend API",
    description="Backend API for YesESCo solar energy services",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# وابستگی اتصال دیتابیس
async def get_db():
    if AsyncSessionLocal is None:
        raise HTTPException(status_code=500, detail="Database configuration is missing")
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# روت‌های اصلی و تست
@app.get("/")
async def read_root():
    return {
        "status": "online",
        "service": "YesESCo Backend",
        "message": "API is running successfully"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "yesesco-backend"}

# روت‌های جدول متقاضیان
@app.post("/api/applicants", response_model=ApplicantResponse, status_code=201)
async def create_applicant(
    applicant_data: ApplicantCreate,
    db: AsyncSession = Depends(get_db),
):
    applicant = Applicant(**applicant_data.model_dump())
    db.add(applicant)
    await db.commit()
    await db.refresh(applicant)
    return applicant

@app.get("/api/applicants", response_model=List[ApplicantResponse])
async def get_applicants(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Applicant).order_by(Applicant.id.desc()))
    return result.scalars().all()

@app.get("/api/applicants/{applicant_id}", response_model=ApplicantResponse)
async def get_applicant(
    applicant_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Applicant).where(Applicant.id == applicant_id))
    applicant = result.scalar_one_or_none()
    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant
