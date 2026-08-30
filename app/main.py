from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import engine, Base, get_db
from app.models import SolarApplicant
from app.schemas import SolarApplicantCreate, SolarApplicantResponse

app = FastAPI(
    title="YesESCo Solar Registration API",
    description="سامانه یکپارچه ثبت‌نام متقاضیان نیروگاه خورشیدی یلدای سهند",
    version="1.0.0"
)

# تنظیمات CORS برای دسترسی فرانت‌اند Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "YesESCo API is running successfully"}

@app.post(
    "/api/applicants",
    response_model=SolarApplicantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="ثبت متقاضی جدید"
)
async def create_applicant(
    applicant_in: SolarApplicantCreate,
    db: AsyncSession = Depends(get_db)
):
    # ثبت مستقیم بدون جلوگیری از کد ملی تکراری
    new_applicant = SolarApplicant(**applicant_in.dict())
    db.add(new_applicant)
    await db.commit()
    await db.refresh(new_applicant)
    return new_applicant

@app.get(
    "/api/applicants",
    response_model=List[SolarApplicantResponse],
    summary="دریافت لیست تمام درخواست‌ها"
)
async def get_all_applicants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(SolarApplicant).order_by(SolarApplicant.id.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    applicants = result.scalars().all()
    return applicants
