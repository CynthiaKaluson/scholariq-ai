# Scholariq-AI
Project Summary

Scholariq-AI is an AI-powered backend API that generates structured academic and professional writing while detecting potential citation hallucinations produced by large language models.

The project explores how AI-generated research content can be made more reliable by adding a citation validation layer to the generation process.

Instead of relying solely on generated text, the system analyzes references and flags potentially fabricated citations before the content is used.

# The Problem

Large language models can produce fluent academic text, but they frequently generate incorrect or fabricated citations.

This creates several issues:
```
• Non-existent research papers
• Fake journal names
• Incorrect citation formatting
• Repeated fabricated sources
• Reduced trust in AI-generated academic writing
```
Many AI writing tools focus on generation but do not validate the reliability of references.

This makes AI-generated academic content risky to use without manual verification.

# The Goal

The goal of this project was to design a backend system that:
```
• Generates structured academic writing
• Supports long-form research outlines and chapters
• Detects potential citation hallucinations
• Provides a clean developer-friendly API
• Includes security features such as API keys and rate limiting
```
The focus was building a backend service that could realistically power an AI writing platform.

# System Design

The system follows a layered backend architecture.

Request flow:
```
Client Request
      ↓
FastAPI Router
      ↓
API Key Authentication
      ↓
Rate Limiter
      ↓
Writing Generation Service
      ↓
AI Model Integration
      ↓
Citation Validation
      ↓
JSON API Response
```
This separation of concerns keeps the application modular and easier to maintain.

# Core Components
API Layer

Built with FastAPI.

# Responsibilities:
```
• Define endpoints
• Validate requests using Pydantic schemas
• Route requests to services
```
# Authentication Layer

Simple API key authentication protects the endpoints.

This simulates how SaaS APIs restrict access to registered users.

# Rate Limiting

Rate limiting prevents abuse of the API and controls request frequency.

This is a common pattern used by production APIs.

# Writing Generation Service

This service is responsible for generating:
```
• research outlines
• academic chapters
• structured writing
```
It communicates with the AI model integration layer.

# AI Model Integration

The project integrates with Google Gemini to generate text responses.

Prompt engineering is used to produce structured academic output.

# Citation Validation

Generated text is analyzed for references.

The validation logic attempts to detect:
```
• suspicious citations
• unrealistic publication details
• potentially fabricated sources
```
This step introduces a verification layer before the response is returned to the user.

# Example API Request

Endpoint
```
POST /writing/quick-generate
```
Headers

Authorization: Bearer YOUR_API_KEY

Body
```
{
  "topic": "Impact of Artificial Intelligence on Healthcare"
}
```
Response
```
{
  "status": "success",
  "outline": [...]
}
```
Key Engineering Decisions
Modular Backend Architecture

The project separates logic into distinct layers:
```
• routes
• services
• models
• core utilities
```
This improves maintainability and scalability.

# API-First Design

The service was designed as a backend API rather than a full application.

This approach allows the system to be used by:
```
• web applications
• research tools
• automation workflows
```
Security Considerations

Two basic production patterns were implemented:
```
• API key authentication
• request rate limiting
```
These features simulate real SaaS backend behavior.

# Technology Stack
```
Backend Framework
FastAPI

Language
Python 3.11

AI Integration
Google Gemini

Validation
Pydantic

Server
Uvicorn

Containerization
Docker

Deployment
Render
```
# Challenges Encountered
Handling AI Output Structure

AI-generated text does not always follow consistent formatting.

Prompt engineering and schema validation were used to maintain structured output.

# Managing API Security

Even simple APIs require protection against abuse.

Adding API keys and rate limiting introduced realistic production constraints.

Designing for Modularity

Separating generation logic, validation, and API routing required careful project organization.

Future Improvements

Potential next steps for the system include:
```
• database-backed citation verification
• user API key management dashboard
• background task processing for long documents
• integration with academic citation databases
• request analytics and logging
```
Outcome

The final result is a modular backend service capable of generating structured academic writing while analyzing citations for potential hallucinations.

The project demonstrates practical backend engineering skills including:
```
• API design
• AI integration
• backend architecture
• authentication and rate limiting
• production-ready documentation
```
Project Repository

GitHub:
```
https://github.com/CynthiaKaluson/scholariq-ai
Author
```
```
Cynthia Kalu Okorie
Backend developer focused on AI systems, backend engineering, and intelligent APIs.
```