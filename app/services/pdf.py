import fitz
from dataclasses import dataclass


@dataclass
class TextChunk:
    content: str
    page_number: int


def extract_chunks(file_bytes: bytes, chunk_size: int = 500) -> list[TextChunk]:
    """Extract text from PDF bytes and split into chunks."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    chunks = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()

        if not text:
            continue

        words = text.split()
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words).strip()

            if chunk_text:
                chunks.append(TextChunk(
                    content=chunk_text,
                    page_number=page_num + 1,
                ))

    doc.close()
    return chunks