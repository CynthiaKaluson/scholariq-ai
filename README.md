# Scholariq-AI

Scholariq-AI is a backend API that generates structured long-form academic and professional content using large language models while actively checking citations for potential hallucinations.

The idea behind the project came from a simple observation: many AI writing tools generate impressive text, but they often fabricate references, break citation formats, or produce poorly structured research writing. That makes their output difficult to trust in academic or professional settings.

Scholariq-AI experiments with a different approach. Instead of stopping at text generation, it introduces a validation layer that inspects citations and flags suspicious references before the content is used.

---

# The Problem

Many AI writing systems today produce fluent text but struggle with academic reliability.

Common issues include:

• Fake or non-existent citations
• Broken citation formatting
• Poorly structured research writing
• Lack of transparency about reference credibility

For students, researchers, and professionals, this creates a trust problem.

Scholariq-AI introduces an additional validation layer that analyzes citations and highlights potential hallucinations.

---

# What Scholariq-AI Does

The API focuses on three main capabilities.

## Structured Writing Generation

The system supports several writing contexts:

• Academic papers
• Research chapters
• Technical documentation
• Professional reports
• Blog content

It also supports different long-form generation modes:

• Single document generation
• Chapter-based writing
• Multi-part writing series

This helps maintain structure across long documents instead of generating disconnected paragraphs.

---

## Citation Validation Layer

After content is generated, the system analyzes citations and checks them for suspicious patterns.

Supported citation styles:

• APA
• Harvard
• MLA
• Chicago
• Vancouver

The validator searches for patterns such as:

• Placeholder author names
• Impossible publication years
• Repeated fabricated references
• Fake publishers
• Formatting inconsistencies

Each analysis produces a **hallucination score** that indicates how trustworthy the citations appear.

---

## Modular API Architecture

Scholariq-AI was built as a modular FastAPI backend.

The project separates responsibilities clearly so that generation logic, validation logic, and routing remain independent.

This architecture makes the system easier to test, maintain, and extend.

---

# Technical Stack

Backend Framework
FastAPI

Language
Python 3.11

AI Integration
Google Gemini API

Validation
Pydantic v2

Server
Uvicorn

Environment Management
python-dotenv

---

# Project Structure

```
scholariq-ai/
│
├── app/
│   ├── main.py
│   ├── api/
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── core/
│   ├── tests/
│   └── workers/
│
├── Docs/
│   ├── swagger-ui.png
│   └── schemas.png
│
├── requirements.txt
├── Dockerfile
├── Procfile
├── .env.example
├── README.md
└── .gitignore
```

Folder responsibilities:

• `routes/` defines API endpoints
• `services/` contains AI generation and validation logic
• `models/` defines request and response schemas
• `core/` manages configuration and environment settings
• `tests/` contains validation and API tests

---

# Running the Project Locally

Clone the repository.

```
git clone https://github.com/CynthiaKaluson/scholariq-ai.git
cd scholariq-ai
```

Create a virtual environment.

```
python -m venv venv
```

Activate the environment.

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies.

```
pip install -r requirements.txt
```

Start the API server.

```
uvicorn app.main:app --reload
```

The server will start at:

```
http://localhost:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Once the server is running, open:

```
http://localhost:8000/docs
```

The Swagger interface allows you to explore endpoints and test requests directly from your browser.

### API Endpoints

![Swagger UI](Docs/swagger-ui.png)

---

### Request / Response Schemas

FastAPI also documents all request and response models automatically.

![Schemas](Docs/schemas.png)

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

Important:

The `.env` file should **never be committed to GitHub**.

Use `.env.example` to document required variables.

---

# Deployment

The project is prepared for container-based deployment.

Example start command used by platforms such as Render:

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Environment variables should be configured in the hosting platform dashboard.

---

# Why This Project Matters

Large language models are powerful writing tools, but reliability remains a challenge.

Scholariq-AI explores a practical direction: combining AI text generation with automated validation.

Instead of blindly trusting generated output, the system analyzes citations and highlights potential issues before the content is used.

---

# Author

Cynthia Kalu Okorie

Backend developer focused on AI systems, backend engineering, and intelligent APIs.
