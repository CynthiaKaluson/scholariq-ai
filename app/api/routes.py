from fastapi import APIRouter

# ✅ CRITICAL: Prefix goes HERE, not in main.py
api_router = APIRouter(prefix="/api")

@api_router.get("/status")
async def status():
    return {
        "status": "ok",
        "service": "Scholariq-AI",
        "stage": "scaffold"
    }