# Scholariq-AI API Documentation

This document provides a quick overview of the available API endpoints.

Full interactive documentation is available when running the server:

http://localhost:8000/docs

---

# Base URL

Local development:

```
http://localhost:8000
```

---

# Authentication

Requests require an API key.

Example header:

```
Authorization: Bearer YOUR_API_KEY
```

---

# Generate Academic Writing

Endpoint:

```
POST /write
```

Description:

Generates structured academic content based on a prompt.

Example Request

```
POST /write
Content-Type: application/json

{
  "topic": "Impact of climate change on coastal cities",
  "style": "APA"
}
```

Example Response

```
{
  "title": "Impact of Climate Change on Coastal Cities",
  "sections": [
    "Introduction",
    "Rising Sea Levels",
    "Economic Impact",
    "Adaptation Strategies"
  ],
  "citations": [
    "IPCC, 2021"
  ]
}
```

---

# Health Check

Endpoint:

```
GET /health
```

Purpose:

Confirms that the API server is running.

Example Response

```
{
  "status": "ok"
}
```

---

# Interactive Documentation

FastAPI automatically generates documentation using Swagger UI.

Visit:

```
/docs
```

This interface allows developers to test API endpoints directly from the browser.
