from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import api_router
from app.routes.writing import router as writing_router

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.limiter import limiter


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Hybrid academic and professional knowledge synthesis platform",
)

# Attach limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Existing routers
app.include_router(api_router)
app.include_router(writing_router)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "status": "running",
    }