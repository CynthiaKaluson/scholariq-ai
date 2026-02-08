from fastapi import APIRouter, HTTPException

from app.models.schemas import OutlineRequest
from app.services.gemini import generate_outline

from app.models.schemas import ChapterRequest
from app.services.gemini import generate_chapter


router = APIRouter(
    prefix="/writing",
    tags=["Writing"]
)


@router.post("/outline")
def create_outline(payload: OutlineRequest):
    """
    Generate a structured outline for any writing category/type.
    """

    try:
        outline = generate_outline(payload)
        return {
            "status": "success",
            "category": payload.category,
            "writing_type": payload.writing_type,
            "outline": outline
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/chapter")
def generate_chapter_content(payload: ChapterRequest):
    """
    Generate a single long-form chapter based on an approved outline.
    """

    try:
        chapter = generate_chapter(payload)
        return {
            "status": "success",
            "category": payload.category,
            "writing_type": payload.writing_type,
            "chapter_title": payload.chapter_title,
            "content": chapter
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
