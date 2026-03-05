# Scholariq-AI

Scholariq-AI is a backend API that generates structured long-form academic and professional content using Large Language Models, while actively checking citations for possible hallucinations.

The project was built after noticing a recurring issue with many AI writing tools: they generate impressive text, but frequently invent references, ignore citation standards, or produce poorly structured long-form writing.

Scholariq-AI attempts to solve that problem by combining AI generation with a validation layer that checks citations and flags suspicious references.

---

# The Problem

Many AI writing systems today are excellent at producing fluent text, but they struggle with academic reliability.

Common issues include:

• Fake or non-existent citations  
• Broken citation formatting  
• Poorly structured research writing  
• Lack of transparency about source reliability  

For students, researchers, and professionals, this makes AI output difficult to trust.

Scholariq-AI introduces an additional validation layer that analyzes citations and highlights possible hallucinations.

---

# What Scholariq-AI Does

The API focuses on three major capabilities.

## 1. Structured Writing Generation

The system supports multiple writing contexts such as:

• Academic papers  
• Research chapters  
• Technical documentation  
• Professional reports  
• Blog content  

It also supports different **long-form generation modes**:

• Single document  
• Chapter-based writing  
• Multi-part series

This helps maintain structure across longer documents instead of generating disconnected paragraphs.

---

## 2. Citation Validation Layer

After the AI generates text, the system analyzes citations and checks them for possible hallucinations.

Supported citation styles include:

• APA  
• Harvard  
• MLA  
• Chicago  
• Vancouver

The validator looks for suspicious patterns such as:

• Placeholder author names  
• Fake publishers  
• Impossible publication years  
• Repeated fabricated sources  
• Citation formatting errors  

Each result produces a **hallucination score** that indicates how trustworthy the references appear.

---

## 3. Clean API Architecture

Scholariq-AI was built as a modular backend service using FastAPI.

The system is designed so that generation logic, validation logic, and API routing are separated into independent components.

This makes the project easier to test, maintain, and extend.

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


scholariq-ai/
│
├── app/
│ ├── main.py
│ ├── routes/
│ ├── services/
│ ├── models/
│ ├── tests/
│ └── core/
│
├── docs/
│ └── swagger.png
│
├── requirements.txt
├── .env.example
├── Dockerfile
├── README.md
└── .gitignore


The architecture separates responsibilities clearly:

• `routes/` handles API endpoints  
• `services/` contains AI and validation logic  
• `models/` defines request/response schemas  
• `tests/` contains validation tests  

---

# Running the Project Locally

Clone the repository.


git clone https://github.com/CynthiaKaluson/scholariq-ai.git

cd scholariq-ai


Create a virtual environment.


python -m venv venv


Activate the environment.

Linux / Mac


source venv/bin/activate


Windows


venv\Scripts\activate


Install dependencies.


pip install -r requirements.txt


Start the server.


uvicorn main:app --reload


The API will be available at:


http://localhost:8000


---

# API Documentation

FastAPI automatically generates interactive API documentation.

Once the server is running, open:


http://localhost:8000/docs


This Swagger interface allows you to test endpoints directly from the browser.

![Swagger UI](docs/swagger.png)

---

# Environment Variables

Create a `.env` file in the project root.

Example:


GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview


The `.env` file should **never be committed to GitHub**.

Use `.env.example` to document required variables.

---

# Deployment

The project is configured for cloud deployment.

Example start command used for platforms like Render:


uvicorn main:app --host 0.0.0.0 --port 10000


Environment variables should be configured in the hosting platform dashboard.

---

# Why This Project Matters

Large language models are powerful writing tools, but reliability remains a challenge.

Scholariq-AI explores a practical approach:

AI generation combined with post-generation validation.

Instead of blindly trusting generated text, the system analyzes citations and highlights potential issues before the content is used.

---

# Author

Cynthia Kalu Okorie

Backend developer focused on AI systems, backend engineering, and intelligent APIs.