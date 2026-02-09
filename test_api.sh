#!/bin/bash

echo "🧪 Testing Scholariq API Endpoints..."
echo "========================================"

# Test 1: Health Check
echo "1. Testing /api/status..."
curl -s http://127.0.0.1:8000/api/status | python -m json.tool
echo ""

# Test 2: Try chapter endpoint (might also fail but let's see)
echo "2. Testing /writing/chapter..."
curl -X POST http://127.0.0.1:8000/writing/chapter \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI in Healthcare",
    "category": "academic",
    "writing_type": "research paper",
    "chapter_title": "Introduction to AI in Healthcare",
    "outline_points": ["Background", "Current State", "Future Trends"],
    "citation_style": "APA",
    "word_count": 1000,
    "long_form_mode": "chapters",
    "allow_old_citations": false
  }' 2>/dev/null | head -100
echo ""
echo "========================================"
