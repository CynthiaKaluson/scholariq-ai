import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.session import get_db
from app.core.security import verify_api_key
from app.core.limiter import limiter
from app.models.database import Document, DocumentChunk, User
from app.models.schemas import DocumentResponse, DocumentListResponse
from app.services.pdf import extract_chunks
from app.services.embeddings import embed_batch
from fastapi import Request

router = APIRouter(prefix="/documents", tags=["Documents"])


async def get_or_create_user(api_key: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.api_key == api_key))
    user = result.scalar_one_or_none()
    if not user:
        user = User(api_key=api_key)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user


@router.post("/upload", response_model=DocumentResponse)
@limiter.limit("10/minute")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    file_bytes = await file.read()

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 10MB.")

    chunks = extract_chunks(file_bytes)

    if not chunks:
        raise HTTPException(status_code=400, detail="No readable text found in PDF.")

    user = await get_or_create_user(api_key, db)

    document = Document(
        user_id=user.id,
        filename=file.filename,
        is_public=False,
        chunk_count=len(chunks),
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    texts = [chunk.content for chunk in chunks]
    embeddings = await embed_batch(texts)

    for chunk, embedding in zip(chunks, embeddings):
        db.add(DocumentChunk(
            document_id=document.id,
            content=chunk.content,
            page_number=chunk.page_number,
            embedding=embedding,
        ))

    await db.commit()
    return document


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    user = await get_or_create_user(api_key, db)
    result = await db.execute(
        select(Document).where(Document.user_id == user.id)
    )
    documents = result.scalars().all()
    return DocumentListResponse(documents=list(documents), total=len(documents))


@router.delete("/{document_id}")
async def delete_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    user = await get_or_create_user(api_key, db)
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == user.id,
        )
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    await db.execute(
        delete(DocumentChunk).where(DocumentChunk.document_id == document_id)
    )
    await db.delete(document)
    await db.commit()
    return {"message": "Document deleted successfully."}