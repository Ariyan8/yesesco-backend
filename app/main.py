import os
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


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Database dependency
# ---------------------------------------------------------

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/")
async def read_root():
    return {
        "status": "online",
        "service": "YesESCo Backend",
        "service": "YesESCo Backend",
        "message": "API isasync def health_check():
    return {
        "status": "healthy",
        "service": "yesesco-backend",
    }


# ---------------------------------------------------------
# Applicants endpoints
# ---------------------------------------------------------

@app.post ---------------------------------------------------------

@app.post(
    "/api/applicants",
    response_model=Applicant_code=201,
)
async def create_applicant(
    applicant_data: ApplicantCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    ثبت اطلاعات متقاضی نیروگاه خورشیدی.
    """

    applicant = Applicant(
        **applicant_data.model_dump()
    )

    db.add(applicant)
    await db.commit()
    await db.refresh(applicant)

    return applicant


@app.get(
    "/api/applicants",
    response_model=List[ApplicantResponse],
)
async def get_applicants(
    db: AsyncSession = Depends(get_db),
):
    """
    دریافت فهرست متقاضیان.
    """

    result = await db.execute(
        select(Applicant).order_by(Applicant.id.desc())
    )

    applicants = result.scalars().all()

    return applicants


@app.get(
    "/api/applicants/{applicant_id}",
    response_model=ApplicantResponse,
)
async def get_applicant(
    applicant_id: int,
    db: AsyncSession =: int,
    db: AsyncSession = Depends(get_db),
):
    اساس شناسه.
    """

    result = await db.execute(
        select(Applicant).where(Applicant.id == applicant_id)
    )

    applicant = result.scalar_one_or_none()

    if applicant is None:
        raise HTTPException(
            status_code=404,
            detail="Applicant not found",
        )

    return applicant


@app.delete(
    "/api/applicants/{applicant_id}",
    status_code=204,
)
async def delete_applicant(
    applicant_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    حذف یک متقاضی.
    """

    result = await db.execute(
        select(Applicant).where(Applicant.id == applicant_id)
    )

    applicant = result.scalar_one_or_none()

    if applicant is None:
        raise HTTPException(
            status_code=404,
            detail="Applicant not found",
        )

    await db.delete(applicant)
    await db.commit()

    return None


# ---------------------------------------------------------
# Optional API information route
# ---------------------------------------------------------

@app.get("/api")
async def api_info():
    return {
        "name": "YesESCo API",
        "version": "1.0.0",
        "docs": "/docs",
        "applicants_endpoint": "/api/applicants",
    }
