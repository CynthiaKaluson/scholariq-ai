import uuid
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.security import verify_api_key
from app.core.limiter import limiter
from app.models.database import Generation, User
from app.models.schemas import WritingRequest, WritingResponse, GenerationListResponse, SourceReference
from app.services.retrieval import retrieve_relevant_chunks
from app.services.generation import generate_content
from app.routes.documents import get_or_create_user
from fastapi import Request

router = APIRouter(prefix="/writing", tags=["Writing"])


@router.post("/generate", response_model=WritingResponse)
@limiter.limit("5/minute")
async def generate_writing(
    request: Request,
    payload: WritingRequest,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    user = await get_or_create_user(api_key, db)

    chunks = await retrieve_relevant_chunks(
        db=db,
        query=payload.topic,
        user_id=user.id,
    )

    content, sources_used = await generate_content(
        topic=payload.topic,
        writing_type=payload.writing_type,
        word_count=payload.word_count,
        chunks=chunks,
    )

    generation = Generation(
        user_id=user.id,
        topic=payload.topic,
        writing_type=payload.writing_type,
        content=content,
        sources_used=json.dumps(sources_used),
    )
    db.add(generation)
    await db.commit()
    await db.refresh(generation)

    return WritingResponse(
        id=generation.id,
        topic=generation.topic,
        writing_type=generation.writing_type,
        content=generation.content,
        sources=[SourceReference(**s) for s in sources_used],
        created_at=generation.created_at,
    )


@router.get("/history", response_model=GenerationListResponse)
async def get_history(
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    user = await get_or_create_user(api_key, db)
    result = await db.execute(
        select(Generation)
        .where(Generation.user_id == user.id)
        .order_by(Generation.created_at.desc())
    )
    generations = result.scalars().all()

    items = []
    for g in generations:
        sources = json.loads(g.sources_used) if g.sources_used else []
        items.append(WritingResponse(
            id=g.id,
            topic=g.topic,
            writing_type=g.writing_type,
            content=g.content,
            sources=[SourceReference(**s) for s in sources],
            created_at=g.created_at,
        ))

    return GenerationListResponse(generations=items, total=len(items))