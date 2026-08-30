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
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# روت ریشه و سلامت‌سنجی
@app.get("/", summary="بررسی وضعیت سرویس", tags=["General"])
@app.get("/api", include_in_schema=False)
async def root():
    return {
        "status": "online",
        "message": "YesESCo API is running successfully on Vercel"
    }

@app.get("/api/health", summary="بررسی سلامت سیستم", tags=["General"])
@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}

# ثبت متقاضی جدید
@app.post(
    "/api/applicants",
    response_model=SolarApplicantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="ثبت متقاضی جدید",
    tags=["Applicants"]
)
@app.post(
    "/applicants",
    response_model=SolarApplicantResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
async def create_applicant(
    applicant_in: SolarApplicantCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        # ایجاد جدول در صورت عدم وجود

        await db.commit()
        await db.refresh(new_applicant)
        return new_applicant
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# دریافت لیست متقاضیان
@app.get(
    "/api/applicants",
    response_model=List[SolarApplicantResponse],
    summary="دریافت لیست تمام درخواست‌ها",
    tags=["Applicants"]
)
@app.get(
    "/applicants",_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# دریافت لیست متقاضیان
@app.get(
    "/api/applicants",
    response_model=List[SolarApplicantResponse],
    summary="دریافت لیست تمام درخواست‌ها",
    tags=["Applicants"]
)
@app.get(
    "/applicants",
    response_model=List[SolarApplicantResponse],
    include_in_schema=False
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
