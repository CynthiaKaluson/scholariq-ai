from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import api_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Hybrid academic and professional knowledge synthesis platform",
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "status": "running",
    }