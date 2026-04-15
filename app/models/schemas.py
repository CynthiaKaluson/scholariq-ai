import uuid
from datetime import datetime
from pydantic import BaseModel


# =========================
# DOCUMENT SCHEMAS
# =========================

class DocumentResponse(BaseModel):
    id: uuid.UUID
    filename: str
    is_public: bool
    chunk_count: int
    upload_date: datetime

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


# =========================
# WRITING SCHEMAS
# =========================

class WritingRequest(BaseModel):
    topic: str
    writing_type: str
    word_count: int = 500


class SourceReference(BaseModel):
    document_name: str
    page_number: int
    excerpt: str


class WritingResponse(BaseModel):
    id: uuid.UUID
    topic: str
    writing_type: str
    content: str
    sources: list[SourceReference]
    created_at: datetime

    model_config = {"from_attributes": True}


class GenerationListResponse(BaseModel):
    generations: list[WritingResponse]
    total: int