from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="YesESCo Backend API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS
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
        "service": "YesESCo API",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# اگر روتر متقاضیان دارید:
# app.include_router(applicants_router, prefix="/api/applicants")
