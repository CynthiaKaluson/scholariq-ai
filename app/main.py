from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import api_router
from app.routes.writing import router as writing_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Hybrid academic and professional knowledge synthesis platform",
)

# ✅ FIXED: Remove prefix from here (it's already in routes.py)
app.include_router(api_router)
app.include_router(writing_router)

@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "status": "running",
    }