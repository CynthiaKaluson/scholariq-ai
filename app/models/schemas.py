from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


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


class LongFormMode(str, Enum):
    single = "single"
    chapters = "chapters"
    series = "series"


class OutlineRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    category: WritingCategory
    writing_type: str = Field(..., min_length=1)
    citation_style: Optional[CitationStyle] = CitationStyle.apa
    education_level: Optional[str] = None
    long_form_mode: LongFormMode = LongFormMode.single
    allow_old_citations: bool = False


class ChapterRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    category: WritingCategory
    writing_type: str = Field(..., min_length=1)
    chapter_title: str = Field(..., min_length=1)
    outline_points: List[str] = Field(..., min_items=1)
    citation_style: Optional[CitationStyle] = CitationStyle.apa
    word_count: int = Field(default=5000, ge=300)
    long_form_mode: LongFormMode = LongFormMode.chapters
    allow_old_citations: bool = False
