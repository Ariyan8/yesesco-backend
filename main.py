from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="YesESCo Backend")

# تنظیم CORS برای اتصال فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online", "message": "YesESCo API is running successfully"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
