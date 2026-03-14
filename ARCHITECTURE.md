# Scholariq-AI Architecture

This document explains the technical architecture behind Scholariq-AI.

The system is designed as an API-first backend that provides AI-assisted academic writing tools with citation validation and rate-limited access.

---

# System Overview

Scholariq-AI follows a modular backend architecture built around a REST API.

The API receives writing requests, processes them through an AI service, validates citations, and returns structured responses.

The service is designed to be consumed by web apps, research tools, or education platforms.

---

# High Level Architecture

Client Applications interact with the backend through HTTP requests.

Typical flow:

Client → API → AI Generation → Validation → Response

Example:

```
Client Application
        |
        v
   FastAPI Server
        |
        v
   Rate Limiter
        |
        v
   API Key Authentication
        |
        v
   Writing Service
        |
        v
   Gemini AI Model
        |
        v
Citation Validation
        |
        v
Structured API Response
```

---

# Core Components

## FastAPI API Layer

The API is built using FastAPI.

Responsibilities:

* handle HTTP requests
* validate request data
* route requests to services
* return structured JSON responses
* expose OpenAPI documentation

---

## API Key Authentication

Each user request includes an API key.

Example:

```
Authorization: Bearer user_api_key
```

This allows the backend to identify and control usage per client.

---

## Rate Limiting

Rate limiting prevents abuse of the API.

Each API key is limited to a defined number of requests within a time window.

Example:

```
20 requests per minute
```

This protects the service from spam or automated scraping.

---

## Writing Generation Service

This service handles the interaction with the AI model.

Responsibilities:

* receive prompt input
* structure the request
* call the AI model
* format the response

---

## AI Model Integration

Scholariq-AI integrates with the Gemini API to generate structured academic content such as:

* research outlines
* structured essay drafts
* topic breakdowns

The AI output is processed before returning it to the client.

---

## Citation Validation Layer

One of the key goals of the system is improving reliability in AI-generated academic writing.

The validation layer attempts to:

* identify possible citations
* verify formatting
* flag missing references

This reduces the risk of fabricated sources.

---

# Deployment Architecture

The API is designed for simple cloud deployment.

Current deployment target:

Render cloud platform.

Deployment flow:

```
GitHub Repository
        |
        v
Render Deployment
        |
        v
Docker Container
        |
        v
FastAPI Server
```

Environment variables store sensitive values such as API keys.

---

# Security Considerations

Several mechanisms are used to improve security:

* API key authentication
* request rate limiting
* environment variable protection
* server-side AI API key storage

These measures prevent misuse and protect external AI resources.

---

# Future Improvements

Potential upgrades to the system include:

* user usage dashboards
* persistent request logs
* caching AI responses
* improved citation verification
* academic database integrations

---

# Design Goals

The system was designed with the following priorities:

* clear modular architecture
* simple API interface
* scalability for SaaS usage
* maintainable backend structure
* safe AI integration


## System Architecture Diagram

```mermaid
flowchart TD

A[Client Application] --> B[FastAPI Server]

B --> C[API Key Authentication]
C --> D[Rate Limiter]

D --> E[Writing Service]

E --> F[Gemini AI Model]

F --> G[Citation Validation]

G --> H[Structured API Response]

## System Architecture Diagram

```mermaid
flowchart TD

A[Client Application] --> B[FastAPI Server]

B --> C[API Key Authentication]
C --> D[Rate Limiter]

D --> E[Writing Service]

E --> F[Gemini AI Model]

F --> G[Citation Validation]

G --> H[Structured API Response]