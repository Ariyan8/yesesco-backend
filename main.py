@app.get("/")
async def read_root():
    return {
        "status": "online",
        "service": "YesESCo Backend",
        "message": "API is running successfully"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "yesesco-backend"}
