from google.generativeai import GenerativeModel, configure
from google.generativeai.types import GenerationConfig

from app.core.config import settings
from app.models.schemas import OutlineRequest, ChapterRequest


# =========================
# GEMINI CLIENT SETUP
# =========================

configure(api_key=settings.GEMINI_API_KEY)

model = GenerativeModel(
    model_name="models/gemini-3-pro-preview"
)


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
            "Adopt a neutral, professional voice.\n"
            "Avoid identifiable stylistic fingerprints.\n"
        ),
        "technical documentation": (
            "Explain systems and processes step by step.\n"
            "Use structured formatting and definitions.\n"
        ),
    }

    return mapping.get(wt, "")


# =========================
# LONG-FORM INTELLIGENCE
# =========================

def long_form_intelligence(mode: str) -> str:
    mapping = {
        "single": (
            "Produce a complete standalone work.\n"
            "Ensure internal coherence.\n"
        ),
        "chapters": (
            "This is part of a multi-chapter work.\n"
            "Do not conclude the entire work.\n"
            "Maintain continuity for subsequent chapters.\n"
        ),
        "series": (
            "This content is part of a series.\n"
            "Avoid final conclusions.\n"
            "Create anticipation for the next part.\n"
        ),
    }

    return mapping.get(mode, "")


# =========================
# PROMPT BUILDERS
# =========================

def build_outline_prompt(data: OutlineRequest) -> str:
    return (
        f"Writing category: {data.category.value}\n"
        f"Writing type: {data.writing_type}\n"
        f"Long-form mode: {data.long_form_mode.value}\n"
        f"Citation style: {data.citation_style}\n"
        f"{category_intelligence(data.category.value)}"
        f"{writing_type_intelligence(data.writing_type)}"
        f"{long_form_intelligence(data.long_form_mode.value)}"
        f"{'Use references from the last 5 years only.\n' if not data.allow_old_citations else ''}"
        f"{f'Education level: {data.education_level}\n' if data.education_level else ''}"
        f"Topic: {data.topic}\n"
        "Generate a structured outline.\n"
        "Return only the outline.\n"
    )


def build_chapter_prompt(data: ChapterRequest) -> str:
    outline_block = "\n".join(f"- {p}" for p in data.outline_points)

    return (
        f"Writing category: {data.category.value}\n"
        f"Writing type: {data.writing_type}\n"
        f"Long-form mode: {data.long_form_mode.value}\n"
        f"Chapter title: {data.chapter_title}\n"
        f"Citation style: {data.citation_style}\n"
        f"{category_intelligence(data.category.value)}"
        f"{writing_type_intelligence(data.writing_type)}"
        f"{long_form_intelligence(data.long_form_mode.value)}"
        f"{'Use references from the last 5 years only.\n' if not data.allow_old_citations else ''}"
        f"Target length: {data.word_count} words.\n"
        "Outline points:\n"
        f"{outline_block}\n"
        "Do not summarize the entire work.\n"
    )


# =========================
# GENERATION FUNCTIONS
# =========================

def _safe_generate(prompt: str, config: GenerationConfig) -> str:
    try:
        response = model.generate_content(prompt, generation_config=config)
        if not response or not response.text:
            raise RuntimeError("Empty response from Gemini")
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini generation failed: {e}")


def generate_outline(data: OutlineRequest) -> str:
    return _safe_generate(
        build_outline_prompt(data),
        GenerationConfig(temperature=0.4, max_output_tokens=4096),
    )


def generate_chapter(data: ChapterRequest) -> str:
    return _safe_generate(
        build_chapter_prompt(data),
        GenerationConfig(temperature=0.5, max_output_tokens=16384),
    )
