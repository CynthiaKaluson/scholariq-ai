from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="Scholariq-AI",
    description="Hybrid academic and professional knowledge synthesis platform",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Scholariq-AI backend is running"}
