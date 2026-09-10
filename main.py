import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI(title="YesESCo Solar Registration API")

# تنظیمات کامل CORS برای فرانت‌اند Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ساخت جداول دیتابیس در زمان استارت اپلیکیشن
@app.on_event("startup")
def on_startup():
    try:
        models.Base.metadata.create_all(bind=database.engine)
        print("✅ Database tables checked/created successfully.")
    except Exception as e:
        print(f"❌ Database connection error on startup: {e}")

@app.get("/")
def read_root():
    return {"status": "running", "service": "YesESCo Backend API"}

@app.post("/api/applicants", status_code=status.HTTP_201_CREATED)
def create_applicant(applicant: schemas.ApplicantCreate, db: Session = Depends(database.get_db)):
    try:
        db_applicant = models.Applicant(**applicant.model_dump() if hasattr(applicant, "model_dump") else applicant.dict())
        db.add(db_applicant)
        db.commit()
        db.refresh(db_applicant)
        return {"id": db_applicant.id, "message": "درخواست با موفقیت ثبت شد"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
