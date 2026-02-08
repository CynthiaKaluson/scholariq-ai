from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/status")
async def status():
    return {
        "status": "ok",
        "service": "Scholariq-AI",
        "stage": "scaffold"
    }
