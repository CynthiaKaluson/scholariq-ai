from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.limiter import limiter
from app.routes.documents import router as documents_router
from app.routes.writing import router as writing_router

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    description="RAG-powered academic writing API. Upload your research documents and generate grounded academic content with real citations.",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(documents_router)
app.include_router(writing_router)


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
    }