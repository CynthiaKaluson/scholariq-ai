import uuid
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import DocumentChunk, Document
from app.services.embeddings import embed_text


async def retrieve_relevant_chunks(
    db: AsyncSession,
    query: str,
    user_id: uuid.UUID,
    top_k: int = 5,
) -> list[dict]:
    """Find most relevant chunks for a query using vector similarity search."""
    query_embedding = await embed_text(query)
    embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    result = await db.execute(
        text("""
            SELECT
                dc.content,
                dc.page_number,
                d.filename,
                dc.embedding <=> CAST(:embedding AS vector) AS distance
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            WHERE d.user_id = :user_id OR d.is_public = true
            ORDER BY distance ASC
            LIMIT :top_k
        """),
        {
            "embedding": embedding_str,
            "user_id": str(user_id),
            "top_k": top_k,
        }
    )

    rows = result.fetchall()
    return [
        {
            "content": row.content,
            "page_number": row.page_number,
            "document_name": row.filename,
            "distance": row.distance,
        }
        for row in rows
    ]