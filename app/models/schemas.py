from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


# =========================
# ENUMS
# =========================

class WritingCategory(str, Enum):
    academic = "academic"
    professional = "professional"
    business = "business"
    content_marketing = "content_marketing"
    personal_admin = "personal_admin"
    technical = "technical"
    specialized = "specialized"


class CitationStyle(str, Enum):
    apa = "APA"
    harvard = "Harvard"
    mla = "MLA"
    chicago = "Chicago"
    vancouver = "Vancouver"


# =========================
# REQUEST SCHEMAS
# =========================

class OutlineRequest(BaseModel):
    topic: str
    category: WritingCategory
    writing_type: str  # e.g. "Research Paper", "Business Plan"
    citation_style: Optional[CitationStyle] = None
    education_level: Optional[str] = None
    allow_old_citations: bool = False


class ChapterRequest(BaseModel):
    topic: str
    category: WritingCategory
    writing_type: str
    chapter_title: str
    outline_points: List[str]
    citation_style: Optional[CitationStyle] = None
    word_count: int = 5000
    allow_old_citations: bool = False
