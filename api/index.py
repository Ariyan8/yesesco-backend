from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
@app.get("/api/")
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "YesESCo API",
        "message": "Connected successfully!"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
