import uuid
from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

GENERATION_MODEL = "gpt-4o-mini"


async def generate_content(
    topic: str,
    writing_type: str,
    word_count: int,
    chunks: list[dict],
) -> tuple[str, list[dict]]:
    """Generate academic content grounded in retrieved document chunks."""

    if not chunks:
        raise ValueError(
            "No relevant documents found. "
            "Please upload documents related to your topic before generating content."
        )

    context_block = ""
    for i, chunk in enumerate(chunks, 1):
        context_block += (
            f"[Source {i}] {chunk['document_name']} — Page {chunk['page_number']}\n"
            f"{chunk['content']}\n\n"
        )

    prompt = (
        f"You are an academic writing assistant. "
        f"Write a {writing_type} of approximately {word_count} words on the topic: '{topic}'.\n\n"
        f"You MUST ground your writing exclusively in the sources provided below. "
        f"Do not introduce any facts, claims, or references that are not present in the sources. "
        f"Cite sources inline using [Source N] notation.\n\n"
        f"SOURCES:\n{context_block}"
        f"\n\nWrite the {writing_type} now:"
    )

    response = await client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=word_count * 2,
    )

    generated_text = response.choices[0].message.content or ""

    sources_used = [
        {
            "document_name": chunk["document_name"],
            "page_number": chunk["page_number"],
            "excerpt": chunk["content"][:200],
        }
        for chunk in chunks
    ]

    return generated_text, sources_used