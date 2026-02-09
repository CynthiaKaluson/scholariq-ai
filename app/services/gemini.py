from google.generativeai import GenerativeModel, configure
from google.generativeai.types import GenerationConfig

from app.core.config import settings
from app.models.schemas import OutlineRequest, ChapterRequest


# =========================
# GEMINI CLIENT SETUP
# =========================

configure(api_key=settings.GEMINI_API_KEY)

# ✅ CORRECT: Just the model name
model = GenerativeModel(
    model_name="gemini-3-pro-preview"
)


# =========================
# INTELLIGENCE LAYERS
# =========================

def category_intelligence(category: str) -> str:
    return {
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
        ),
        "personal_admin": (
            "Write politely and professionally.\n"
        ),
        "technical": (
            "Write with precision and accuracy.\n"
        ),
        "specialized": (
            "Follow domain-specific standards.\n"
        ),
    }.get(category, "")


def writing_type_intelligence(writing_type: str) -> str:
    return {
        "research paper": (
            "Include abstract, methodology, results, and discussion.\n"
        ),
        "literature review": (
            "Synthesize existing studies and identify gaps.\n"
        ),
        "business plan": (
            "Focus on execution strategy and financial viability.\n"
        ),
        "market research report": (
            "Present structured data-driven insights.\n"
        ),
        "blog post": (
            "Maintain conversational flow and engagement.\n"
        ),
        "email": (
            "Be concise and action-oriented.\n"
        ),
    }.get(writing_type.lower(), "")


def long_form_intelligence(mode: str) -> str:
    return {
        "single": "Produce a complete standalone work.\n",
        "chapters": (
            "This is part of a multi-chapter work.\n"
            "Do not conclude the entire work.\n"
        ),
        "series": (
            "This is part of a series.\n"
            "Avoid final conclusions.\n"
        ),
    }.get(mode, "")


# =========================
# CITATION ENFORCEMENT (NEW - PHASE 1)
# =========================

def citation_intelligence(style: str, allow_old: bool) -> str:
    """Enforce citation rules at prompt level."""
    style_rules = {
        "APA": (
            "Use APA format (author, year) in-text citations.\n"
            "Reference list must be alphabetical, hanging indent.\n"
        ),
        "Harvard": (
            "Use Harvard format (author year) in-text citations.\n"
            "Separate references by medium type.\n"
        ),
        "MLA": (
            "Use MLA format (author page) in-text citations.\n"
            "Works Cited list, alphabetical order.\n"
        ),
        "Chicago": (
            "Use Chicago notes-bibliography format.\n"
            "Footnotes with full citations first, shortened after.\n"
        ),
        "Vancouver": (
            "Use Vancouver numbered citations [1], [2], etc.\n"
            "Reference list in citation order.\n"
        ),
    }.get(style, "")

    age_rule = (
        "Use ONLY references from the last 5 years.\n"
        if not allow_old
        else "Older references may be used if highly relevant.\n"
    )

    anti_hallucination = (
        "CRITICAL: Do NOT fabricate sources.\n"
        "Only cite sources you are certain exist.\n"
        "If unsure about a source, use conditional language: 'research suggests' instead of citing.\n"
        "If a source cannot be verified, DO NOT include it.\n"
    )

    return f"{style_rules}{age_rule}{anti_hallucination}"


# =========================
# PROMPT BUILDERS
# =========================

def build_outline_prompt(data: OutlineRequest) -> str:
    return (
        f"Writing category: {data.category.value}\n"
        f"Writing type: {data.writing_type}\n"
        f"Long-form mode: {data.long_form_mode.value}\n"
        f"Citation style: {data.citation_style.value}\n"
        f"\n{category_intelligence(data.category.value)}"
        f"{writing_type_intelligence(data.writing_type)}"
        f"{long_form_intelligence(data.long_form_mode.value)}"
        f"{citation_intelligence(data.citation_style.value, data.allow_old_citations)}"
        f"\nEducation level: {data.education_level or 'Not specified'}\n"
        f"\nTopic: {data.topic}\n"
        "\n--- INSTRUCTION ---\n"
        "Generate a detailed, structured outline.\n"
        "Include point descriptions (2-3 sentences each).\n"
        "Return ONLY the outline, no preamble.\n"
    )


def build_chapter_prompt(data: ChapterRequest) -> str:
    outline_block = "\n".join(f"- {p}" for p in data.outline_points)

    return (
        f"Writing category: {data.category.value}\n"
        f"Writing type: {data.writing_type}\n"
        f"Long-form mode: {data.long_form_mode.value}\n"
        f"Chapter title: {data.chapter_title}\n"
        f"Citation style: {data.citation_style.value}\n"
        f"\n{category_intelligence(data.category.value)}"
        f"{writing_type_intelligence(data.writing_type)}"
        f"{long_form_intelligence(data.long_form_mode.value)}"
        f"{citation_intelligence(data.citation_style.value, data.allow_old_citations)}"
        f"\nTarget length: ~{data.word_count} words.\n"
        f"\nOutline points to cover:\n{outline_block}\n"
        "\n--- INSTRUCTION ---\n"
        "Write a deep, substantive chapter.\n"
        "Do NOT summarize the entire work.\n"
        "Do NOT write conclusions that end the overall piece.\n"
        "Include inline citations where appropriate.\n"
        "Return ONLY the chapter content, no metadata.\n"
    )


# =========================
# GENERATION
# =========================

def generate_outline(data: OutlineRequest) -> str:
    response = model.generate_content(
        build_outline_prompt(data),
        generation_config=GenerationConfig(
            temperature=0.3,  # Lower = more consistent structure
            max_output_tokens=4096,
        ),
    )
    return response.text


def generate_chapter(data: ChapterRequest) -> str:
    response = model.generate_content(
        build_chapter_prompt(data),
        generation_config=GenerationConfig(
            temperature=0.4,  # Slightly lower for academic credibility
            max_output_tokens=16384,
        ),
    )
    return response.text