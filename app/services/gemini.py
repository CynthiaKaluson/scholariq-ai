import google.generativeai as genai

from app.core.config import settings
from app.models.schemas import OutlineRequest, ChapterRequest


# =========================
# GEMINI CLIENT SETUP
# =========================

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro"
)


# =========================
# CATEGORY INTELLIGENCE
# =========================

def category_intelligence(category: str) -> str:
    """
    Controls tone, reasoning style, and structure per category.
    """

    mapping = {
        "academic": (
            "Use formal academic language.\n"
            "Follow scholarly structure and depth.\n"
            "Support arguments with peer-reviewed citations.\n"
        ),
        "professional": (
            "Write clearly and concisely.\n"
            "Focus on applied knowledge and clarity.\n"
        ),
        "business": (
            "Write for executives and decision-makers.\n"
            "Emphasize strategy, metrics, and outcomes.\n"
        ),
        "content_marketing": (
            "Write engaging, reader-focused content.\n"
            "Use persuasive and storytelling techniques.\n"
        ),
        "personal_admin": (
            "Write politely, clearly, and professionally.\n"
            "Keep structure simple and direct.\n"
        ),
        "technical": (
            "Write with precision and accuracy.\n"
            "Use structured explanations and definitions.\n"
        ),
        "specialized": (
            "Write with domain-specific rigor.\n"
            "Follow industry or regulatory standards.\n"
        ),
    }

    return mapping.get(category, "")


# =========================
# PROMPT BUILDERS
# =========================

def build_outline_prompt(data: OutlineRequest) -> str:
    category_rules = category_intelligence(data.category)

    citation_rule = (
        "Use references from the last 5 years only.\n"
        if not data.allow_old_citations
        else "Older references are allowed if relevant.\n"
    )

    education_context = (
        f"Education level: {data.education_level}\n"
        if data.education_level
        else ""
    )

    return (
        f"Writing category: {data.category}\n"
        f"Writing type: {data.writing_type}\n"
        f"Citation style: {data.citation_style}\n"
        f"{category_rules}"
        f"{citation_rule}"
        f"{education_context}"
        f"Topic: {data.topic}\n"
        "Generate a clear, logical outline with chapters and sub-sections.\n"
        "Return only the outline.\n"
    )


def build_chapter_prompt(data: ChapterRequest) -> str:
    category_rules = category_intelligence(data.category)

    citation_rule = (
        "Use references from the last 5 years only.\n"
        if not data.allow_old_citations
        else "Older references are allowed if relevant.\n"
    )

    outline_block = "\n".join(f"- {point}" for point in data.outline_points)

    return (
        f"Writing category: {data.category}\n"
        f"Writing type: {data.writing_type}\n"
        f"Chapter title: {data.chapter_title}\n"
        f"Citation style: {data.citation_style}\n"
        f"{category_rules}"
        f"{citation_rule}"
        f"Write approximately {data.word_count} words.\n"
        "Follow the outline strictly.\n"
        "Outline points:\n"
        f"{outline_block}\n"
        "Ensure logical flow and proper citations.\n"
    )


# =========================
# GENERATION FUNCTIONS
# =========================

def generate_outline(data: OutlineRequest) -> str:
    response = model.generate_content(
        build_outline_prompt(data),
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,
            max_output_tokens=2048,
        ),
    )
    return response.text


def generate_chapter(data: ChapterRequest) -> str:
    response = model.generate_content(
        build_chapter_prompt(data),
        generation_config=genai.types.GenerationConfig(
            temperature=0.5,
            max_output_tokens=8192,
        ),
    )
    return response.text
