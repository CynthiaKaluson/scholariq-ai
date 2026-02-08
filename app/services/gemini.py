from google.generativeai import GenerativeModel, configure
from google.generativeai.types import GenerationConfig

from app.core.config import settings
from app.models.schemas import OutlineRequest, ChapterRequest


# =========================
# GEMINI CLIENT SETUP
# =========================

configure(api_key=settings.GEMINI_API_KEY)

model = GenerativeModel(model_name="models/gemini-1.5-pro")


# =========================
# CATEGORY INTELLIGENCE
# =========================

def category_intelligence(category: str) -> str:
    mapping = {
        "academic": (
            "Use formal academic language.\n"
            "Apply scholarly structure and analytical depth.\n"
            "Ground arguments in credible academic sources.\n"
        ),
        "professional": (
            "Write clearly and directly.\n"
            "Prioritize usefulness and clarity.\n"
        ),
        "business": (
            "Write for decision-makers.\n"
            "Focus on strategy, performance, and outcomes.\n"
        ),
        "content_marketing": (
            "Write engaging and reader-focused content.\n"
            "Maintain flow and persuasive clarity.\n"
        ),
        "personal_admin": (
            "Write politely and professionally.\n"
            "Use simple and respectful language.\n"
        ),
        "technical": (
            "Write with precision and accuracy.\n"
            "Explain concepts systematically.\n"
        ),
        "specialized": (
            "Follow domain-specific standards.\n"
            "Use precise professional terminology.\n"
        ),
    }

    return mapping.get(category, "")


# =========================
# WRITING-TYPE INTELLIGENCE
# =========================

def writing_type_intelligence(writing_type: str) -> str:
    wt = writing_type.lower()

    mapping = {
        "research paper": (
            "Structure content with abstract, methodology, results, and discussion.\n"
            "Emphasize evidence-based reasoning and citations.\n"
        ),
        "literature review": (
            "Synthesize existing studies.\n"
            "Compare findings and identify gaps.\n"
        ),
        "thesis": (
            "Maintain formal academic rigor.\n"
            "Develop arguments progressively across sections.\n"
        ),
        "business plan": (
            "Focus on execution strategy, market opportunity, and financial logic.\n"
            "Write persuasively but realistically.\n"
        ),
        "market research report": (
            "Present structured analysis and insights.\n"
            "Interpret trends and data clearly.\n"
        ),
        "blog post": (
            "Use conversational tone.\n"
            "Maintain reader engagement and clarity.\n"
        ),
        "email": (
            "Be concise and action-oriented.\n"
            "Avoid unnecessary elaboration.\n"
        ),
        "copywriting": (
            "Write persuasively with clear value propositions.\n"
            "Guide the reader toward action.\n"
        ),
        "ghostwriting": (
            "Adapt to a neutral professional voice.\n"
            "Avoid personal identifiers or stylistic bias.\n"
        ),
        "technical documentation": (
            "Explain systems and processes step by step.\n"
            "Use structured formatting and definitions.\n"
        ),
    }

    return mapping.get(wt, "")


# =========================
# PROMPT BUILDERS
# =========================

def build_outline_prompt(data: OutlineRequest) -> str:
    category_rules = category_intelligence(data.category)
    writing_type_rules = writing_type_intelligence(data.writing_type)

    citation_rule = (
        "Use references from the last 5 years only.\n"
        if not data.allow_old_citations
        else "Older references may be used if relevant.\n"
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
        f"{writing_type_rules}"
        f"{citation_rule}"
        f"{education_context}"
        f"Topic: {data.topic}\n"
        "Generate a structured outline with chapters and sub-sections.\n"
        "Return only the outline.\n"
    )


def build_chapter_prompt(data: ChapterRequest) -> str:
    category_rules = category_intelligence(data.category)
    writing_type_rules = writing_type_intelligence(data.writing_type)

    citation_rule = (
        "Use references from the last 5 years only.\n"
        if not data.allow_old_citations
        else "Older references may be used if relevant.\n"
    )

    outline_block = "\n".join(f"- {point}" for point in data.outline_points)

    return (
        f"Writing category: {data.category}\n"
        f"Writing type: {data.writing_type}\n"
        f"Chapter title: {data.chapter_title}\n"
        f"Citation style: {data.citation_style}\n"
        f"{category_rules}"
        f"{writing_type_rules}"
        f"{citation_rule}"
        f"Target length: {data.word_count} words.\n"
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
        generation_config=GenerationConfig(
            temperature=0.4,
            max_output_tokens=2048,
        ),
    )
    return response.text


def generate_chapter(data: ChapterRequest) -> str:
    response = model.generate_content(
        build_chapter_prompt(data),
        generation_config=GenerationConfig(
            temperature=0.5,
            max_output_tokens=8192,
        ),
    )
    return response.text
