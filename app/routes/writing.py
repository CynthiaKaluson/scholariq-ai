from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.schemas import OutlineRequest, ChapterRequest
from app.services.gemini import generate_outline, generate_chapter


router = APIRouter(prefix="/writing", tags=["Writing"])


# =========================
# QUICK GENERATE ENDPOINT
# =========================

class QuickGenerateRequest(BaseModel):
    topic: str


@router.post("/quick-generate")
def quick_generate(data: QuickGenerateRequest):
    """
    Simplified endpoint that only requires a topic.
    The backend fills the rest of the parameters automatically.
    """

    try:
        payload = OutlineRequest(
            topic=data.topic,
            category="academic",
            writing_type="research_explanation",
            citation_style="APA",
            education_level="undergraduate",
            long_form_mode="single",
            allow_old_citations=False,
        )

        return {
            "status": "success",
            "topic": data.topic,
            "outline": generate_outline(payload),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# EXISTING ENDPOINTS
# =========================

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