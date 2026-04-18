# ScholarIQ

RAG-powered academic writing API. Upload your research documents and generate grounded academic content — every citation traces back to a source you provided.

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-blue)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-black)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![Deployment](https://img.shields.io/badge/deployment-render-purple)

---

## The Problem

AI writing tools generate content confidently — including fake citations. Most solutions try to filter hallucinations after the fact. ScholarIQ takes a different approach: the AI can only write from documents you uploaded. Hallucinated references aren't filtered out — they're structurally impossible.

---

## Live API
https://scholariq-ai.onrender.com

Interactive documentation:
https://scholariq-ai.onrender.com/docs

---

## How It Works
You upload a PDF
↓
System extracts text and splits into chunks
↓
OpenAI generates embeddings for each chunk
↓
Embeddings stored in PostgreSQL via pgvector
↓
You request writing on a topic
↓
Your topic is embedded and matched against your documents
↓
Top matching chunks retrieved via vector similarity search
↓
GPT-4o-mini generates content grounded in those chunks
↓
Response includes generated text + source citations
(document name, page number, excerpt)

---
```
## API Endpoints
POST   /documents/upload        Upload a PDF document
GET    /documents               List your uploaded documents
DELETE /documents/{id}          Delete a document and its vectors
POST   /writing/generate        Generate content from your documents
GET    /writing/history         Retrieve past generations
```
---

## Technical Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python 3.11 |
| Database | PostgreSQL + pgvector |
| ORM | SQLAlchemy 2.0 async |
| Embeddings | OpenAI text-embedding-3-small |
| Generation | GPT-4o-mini |
| PDF Processing | PyMuPDF |
| Auth | API Key (X-API-Key header) |
| Rate Limiting | SlowAPI |
| Containerization | Docker |
| Deployment | Render |

### Database Note

ScholarIQ uses PostgreSQL with the pgvector extension for vector similarity search. There is no SQLite. Document embeddings, generation history, and user data are all persisted in a single production-grade database.

---

## Quick Start

### Authentication

All endpoints require an API key passed in the request header:
X-API-Key: your-api-key

### Upload a document

```bash
curl -X POST "https://scholariq-ai.onrender.com/documents/upload" \
  -H "X-API-Key: your-api-key" \
  -F "file=@your-paper.pdf"
```

### Generate content

```bash
curl -X POST "https://scholariq-ai.onrender.com/writing/generate" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Impact of climate change on food security",
    "writing_type": "research summary",
    "word_count": 500
  }'
```

---

## Running Locally

```bash
git clone https://github.com/CynthiaKaluson/scholariq-ai.git
cd scholariq-ai

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
```
Create a `.env` file:
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/scholariq
OPENAI_API_KEY=your_openai_api_key
API_SECRET_KEY=your_secret_key
```
Run migrations:

```bash
alembic upgrade head
```

Start the server:

```bash
uvicorn app.main:app --reload
```

---
```
## Project Structure
scholariq-ai/
├── app/
│   ├── core/           # Config, auth, rate limiting
│   ├── db/             # Async database session
│   ├── models/         # SQLAlchemy models + Pydantic schemas
│   ├── routes/         # API endpoints
│   ├── services/       # PDF processing, embeddings, retrieval, generation
│   └── main.py
├── alembic/            # Database migrations
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
---

## Author
```
Cynthia Kalu Okorie

Backend developer building AI-powered APIs.
[GitHub](https://github.com/CynthiaKaluson) · [LinkedIn](https://linkedin.com/in/cynthia-kalu-okorie)
```