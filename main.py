from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI()

# تنظیمات CORS برای ارتباط با Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # در حالت پروداکشن دامنه سایت خود را بنویسید
    allow_methods=["*"],
    allow_headers=["*"],
)

# ایجاد جداول در اولین اجرا
models.Base.metadata.create_all(bind=database.engine)

@app.post("/api/applicants")
def create_applicant(applicant: schemas.ApplicantCreate, db: Session = Depends(database.get_db)):
    db_applicant = models.Applicant(**applicant.dict())
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)
    return {"id": db_applicant.id, "message": "ثبت شد"}
