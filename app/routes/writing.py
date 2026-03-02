from fastapi import APIRouter, HTTPException

from app.models.schemas import OutlineRequest, ChapterRequest
from app.services.gemini import generate_outline, generate_chapter

router = APIRouter(prefix="/writing", tags=["Writing"])


@router.post("/outline")
def create_outline_endpoint(payload: OutlineRequest):
    try:
        return {
            "status": "success",
            "outline": generate_outline(payload),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chapter")
def create_chapter_endpoint(payload: ChapterRequest):
    try:
        return {
            "status": "success",
            "chapter_title": payload.chapter_title,
            "content": generate_chapter(payload),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))