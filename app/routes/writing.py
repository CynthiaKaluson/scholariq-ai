from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.models.schemas import (
    OutlineRequest,
    ChapterRequest,
    WritingCategory,
    CitationStyle,
    LongFormMode,
)

from app.services.gemini import generate_outline, generate_chapter
from app.core.auth import verify_api_key

router = APIRouter(prefix="/writing", tags=["Writing"])


class QuickGenerateRequest(BaseModel):
    topic: str


@router.post("/quick-generate")
def quick_generate(
    data: QuickGenerateRequest,
    _: str = Depends(verify_api_key),
):
    """
    Simplified endpoint that only requires a topic.
    The backend fills the rest with default parameters automatically.
    """

    try:
        payload = OutlineRequest(
            topic=data.topic,
            category=WritingCategory.academic,
            writing_type="research_explanation",
            citation_style=CitationStyle.apa,
            education_level="undergraduate",
            long_form_mode=LongFormMode.single,
            allow_old_citations=False,
        )

        return {
            "status": "success",
            "topic": data.topic,
            "outline": generate_outline(payload),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/outline")
def create_outline_endpoint(
    payload: OutlineRequest,
    _: str = Depends(verify_api_key),
):
    try:
        return {
            "status": "success",
            "outline": generate_outline(payload),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chapter")
def create_chapter_endpoint(
    payload: ChapterRequest,
    _: str = Depends(verify_api_key),
):
    try:
        return {
            "status": "success",
            "chapter_title": payload.chapter_title,
            "content": generate_chapter(payload),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))