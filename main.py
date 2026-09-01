from fastapi import FastAPI

app = FastAPI(title="YesESCo Backend")

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
