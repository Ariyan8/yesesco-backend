from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Request
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

# پیکربندی استاندارد CORS برای پشتیبانی از تمام کلاینت‌ها و مرورگرها
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# روت‌های وضعیت و سلامت سرویس
@app.get("/", summary="بررسی وضعیت سرویس", tags=["General"])
@app.get("/api", include_in_schema=False)
@app.get("/api/index.py", include_in_schema=False)
async def root():
    return {
        "status": "online",
        "service": "YesESCo Solar Backend",
        "platform": "Vercel Serverless"
    }

@app.get("/api/health", summary="بررسی سلامت سیستم", tags=["General"])
@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy"}

# تابع کمکی برای همگام‌سازی فیلدهای ورودی فرانت‌اند با دیتابیس
def normalize_applicant_payload(raw_data: dict) -> dict:
    data = raw_data.copy()
    
    # مپ کردن مساحت زمین
    if "available_area_sqm" in data and "land_area_sqm" not in data:
        data["land_area_sqm"] = data.pop("available_area_sqm")
        
    # مپ کردن ظرفیت درخواستی
    if "proposed_capacity_kw" in data and "requested_capacity_kw" not in data:
        data["requested_capacity_kw"] = data.pop("proposed_capacity_kw")
        
    # مپ کردن نوع سقف/سازه
    if "structure_type" in data and "roof_type" not in data:
        data["roof_type"] = data.pop("structure_type")
        
    # مپ کردن توضیحات
    if "description" in data and "notes" not in data:
        data["notes"] = data.pop("description")
        
    return data

# روت ثبت‌نام متقاضی جدید
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
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        raw_body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فرمت دیتای ارسالی JSON معتبر نیست."
        )

    # نرمال‌سازی فیلدها و تبدیل به آبجکت اسکیما
    normalized_data = normalize_applicant_payload(raw_body)
    
    try:
        applicant_data = SolarApplicantCreate(**normalized_data)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err)
        )

    try:
        # ایجاد جدول در صورت عدم وجود در Supabase
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        data_dict = applicant_data.model_dump() if hasattr(applicant_data, "model_dump") else applicant_data.dict()
        
        new_applicant = SolarApplicant(**data_dict)
        db.add(new_applicant)
        await db.commit()
        await db.refresh(new_applicant)
        return new_applicant

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در پایگاه داده: {str(e)}"
        )

# روت دریافت لیست تمام درخواست‌ها
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
            detail=f"خطا در پایگاه داده: {str(e)}"
        )
