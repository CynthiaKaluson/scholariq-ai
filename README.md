# Scholariq-AI

**AI-powered long-form writing engine for academic & professional content**

A backend API that generates **credible, structured, citation-aware written content** using Google Gemini 3 models—with built-in hallucination detection and citation validation.

---

## Problem

Most AI writing tools:
- ❌ Hallucinate fake references
- ❌ Ignore academic structure
- ❌ Don't respect citation standards
- ❌ Produce shallow long-form outputs

**Scholariq-AI solves this.**

---

## Features

✅ **Writing Intelligence**
- 7 writing categories (academic, professional, business, technical, etc.)
- Multiple writing types (research paper, thesis, blog post, email, etc.)
- Long-form modes (single, chapters, series)

✅ **Citation Enforcement**
- APA, Harvard, MLA, Chicago, Vancouver formats
- Anti-hallucination detection (8+ pattern recognition)
- Citation age validation (default: last 5 years)
- Hallucination scoring (0-100%)

✅ **Production-Ready**
- FastAPI backend
- Gemini-3 integration (pro & flash models)
- Structured prompt engineering
- Pydantic validation

---

## Stack

- **Backend**: Python 3.11 + FastAPI
- **AI Model**: Google Gemini-3 (pro-preview, flash-preview)
- **Validation**: Pydantic v2
- **Server**: Uvicorn

---

## API Documentation

Interactive Swagger UI available at:

http://localhost:8000/docs

![Swagger UI](docs/swagger.png)


## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/CynthiaKaluson/scholariq-ai.git
cd scholariq-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt