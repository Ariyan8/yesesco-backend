from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import engine, Base, get_db
from app.models import SolarApplicant
from app.schemas import SolarApplicantCreate, SolarApplicantResponse

app = FastAPI(
    title="YesESCo Solar Registration API",
    description="سامانه یکپارچه ثبت‌نام متقاضیان نیروگاه خورشیدی یلدای سهند",
    version="1.0.0"
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "YesESCo API is running successfully on Vercel"
    }

@app.get("/api/health")
async def health():
    return {"status": "ok"}

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
    try:
        # ایجاد خودکار جدول در صورت عدم وجود (بدون ایجاد کرش در استارت‌آپ)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # سازگار با Pydantic v1 و v2
        data = applicant_in.model_dump() if hasattr(applicant_in, "model_dump") else applicant_in.dict()
        
        new_applicant = SolarApplicant(**data)
        db.add(new_applicant)
        await db.commit()
        await db.refresh(new_applicant)
        return new_applicant
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

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
    try:
        query = select(SolarApplicant).order_by(SolarApplicant.id.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        applicants = result.scalars().all()
        return applicants
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
