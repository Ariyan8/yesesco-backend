from fastapi import FastAPI

app = FastAPI(
    title="YesESCo Backend",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "YesESCo Backend"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
