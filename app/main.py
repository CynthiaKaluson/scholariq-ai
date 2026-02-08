from fastapi import FastAPI

from app.core.config import settings
from app.routes import router as api_router
from app.api.writing import router as writing_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Hybrid academic and professional knowledge synthesis platform",
)

app.include_router(api_router, prefix="/api")
app.include_router(writing_router)

@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "status": "running",
    }
