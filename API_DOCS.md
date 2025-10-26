# 🔌 JIRA AI Agent - API Documentation

Complete API reference for the Flask backend.

**Base URL:** `http://localhost:5000`

---

## Table of Contents
- [Authentication](#authentication)
- [Health Check](#health-check)
- [Query Processing](#query-processing)
- [Ticket Operations](#ticket-operations)
- [Analytics](#analytics)
- [Error Handling](#error-handling)

---

## Authentication

Currently, authentication is handled via environment variables (JIRA credentials). Future versions may include API key authentication.

---

## Health Check

### GET `/health`

Check if the API is running and components are initialized.

**Response:**
```json
{
  "status": "healthy",
  "llm_agent": true,
  "jira_client": true
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

## Query Processing

### POST `/api/query`

Process a user query and return matched tickets with AI-generated resolutions.

**Request Body:**
```json
{
  "query": "string (required) - User question or problem",
  "projects": ["array of project keys (optional)"],
  "max_results": "integer (optional, default: 5)"
}
```

**Response:**
```json
{
  "query": "original query text",
  "analysis": {
    "main_problem": "brief description",
    "key_terms": ["term1", "term2"],
    "issue_type": "bug|feature|question",
    "priority": "high|medium|low",
    "summary": "one-line summary"
  },
  "matched_tickets": [
    {
      "ticket_key": "PROD-123",
      "relevance_score": 9,
      "reasoning": "why it's relevant",
      "has_solution": true,
      "solution_summary": "brief solution",
      "ticket_data": {
        "key": "PROD-123",
        "summary": "ticket summary",
        "description": "full description",
        "status": "Done",
        "resolution": "Fixed",
        "priority": "High",
        "url": "https://jira.../PROD-123"
      }
    }
  ],
  "resolution": "AI-generated comprehensive resolution",
  "total_historical_tickets": 150
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "API returns 500 error on authentication",
    "projects": ["PROD", "TECH"],
    "max_results": 5
  }'
```

**Status Codes:**
- `200 OK` - Query processed successfully
- `400 Bad Request` - Missing or invalid query
- `500 Internal Server Error` - Processing error

---

## Ticket Operations

### POST `/api/tickets/search`

Search for JIRA tickets with filters.

**Request Body:**
```json
{
  "projects": ["array of project keys (optional)"],
  "statuses": ["array of statuses (optional)"],
  "days_back": "integer (optional, default: 30)",
  "max_results": "integer (optional, default: 50)"
}
```

**Response:**
```json
{
  "tickets": [
    {
      "key": "PROD-123",
      "summary": "ticket summary",
      "description": "full description",
      "status": "Done",
      "resolution": "Fixed",
      "created": "2025-10-01T10:00:00Z",
      "updated": "2025-10-15T15:30:00Z",
      "priority": "High",
      "assignee": "John Doe",
      "reporter": "Jane Smith",
      "labels": ["api", "authentication"],
      "url": "https://jira.../PROD-123",
      "comments": [
        {
          "author": "John Doe",
          "body": "comment text",
          "created": "2025-10-02T11:00:00Z"
        }
      ]
    }
  ],
  "count": 25
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/tickets/search \
  -H "Content-Type: application/json" \
  -d '{
    "projects": ["PROD"],
    "statuses": ["Done", "Resolved"],
    "days_back": 30,
    "max_results": 50
  }'
```

### GET `/api/tickets/<ticket_key>`

Get detailed information about a specific ticket.

**Parameters:**
- `ticket_key` (string, required) - JIRA ticket key (e.g., "PROD-123")

**Response:**
```json
{
  "key": "PROD-123",
  "summary": "ticket summary",
  "description": "full description",
  "status": "Done",
  "resolution": "Fixed",
  "created": "2025-10-01T10:00:00Z",
  "updated": "2025-10-15T15:30:00Z",
  "priority": "High",
  "assignee": "John Doe",
  "reporter": "Jane Smith",
  "labels": ["api", "authentication"],
  "url": "https://jira.../PROD-123",
  "comments": [...]
}
```

**Example:**
```bash
curl http://localhost:5000/api/tickets/PROD-123
```

**Status Codes:**
- `200 OK` - Ticket found
- `404 Not Found` - Ticket not found
- `500 Internal Server Error` - Fetch error

---

## Analytics

### POST `/api/analytics/statistics`

Get ticket statistics for analytics and visualization.

**Request Body:**
```json
{
  "projects": ["array of project keys (optional)"],
  "days_back": "integer (optional, default: 30)"
}
```

**Response:**
```json
{
  "total_tickets": 150,
  "by_status": {
    "Done": 80,
    "In Progress": 30,
    "Open": 40
  },
  "by_priority": {
    "High": 45,
    "Medium": 70,
    "Low": 35
  },
  "by_project": {
    "PROD": 90,
    "TECH": 60
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/analytics/statistics \
  -H "Content-Type: application/json" \
  -d '{
    "projects": ["PROD", "TECH"],
    "days_back": 30
  }'
```

### POST `/api/insights`

Extract AI-powered insights from historical tickets.

**Request Body:**
```json
{
  "projects": ["array of project keys (optional)"],
  "days_back": "integer (optional, default: 30)"
}
```

**Response:**
```json
{
  "insights": {
    "common_issues": [
      "Authentication failures",
      "API timeout errors",
      "Database connection issues"
    ],
    "common_resolutions": [
      "Restart service",
      "Update configuration",
      "Clear cache"
    ],
    "recommendations": [
      "Add better error logging for authentication",
      "Implement retry logic for API calls",
      "Document common solutions in wiki"
    ]
  },
  "analyzed_tickets": 100
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/insights \
  -H "Content-Type: application/json" \
  -d '{
    "projects": ["PROD"],
    "days_back": 90
  }'
```

---

## Error Handling

All endpoints return errors in the following format:

```json
{
  "error": "Human-readable error message"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server-side error

**Example Error Response:**
```json
{
  "error": "Query is required"
}
```

---

## Rate Limiting

Currently, there are no rate limits. In production, consider implementing:
- Rate limiting per IP/user
- Request throttling
- API key authentication

---

## Response Times

Typical response times:
- `/health`: < 100ms
- `/api/tickets/search`: 1-3 seconds
- `/api/query`: 5-15 seconds (includes LLM processing)
- `/api/insights`: 10-30 seconds (includes AI analysis)

---

## Data Formats

### Date Format
All dates are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

Example: `2025-10-26T15:30:00Z`

### Project Keys
Project keys are uppercase strings (e.g., `PROD`, `TECH`, `SUP`)

### Ticket Keys
Ticket keys follow format: `PROJECT-NUMBER` (e.g., `PROD-123`)

---

## Examples by Use Case

### Use Case 1: Resolve a Technical Issue

```bash
# 1. Search for query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Database connection timeout", "max_results": 3}'

# 2. Get specific ticket details
curl http://localhost:5000/api/tickets/PROD-456
```

### Use Case 2: Analyze Team Performance

```bash
# 1. Get statistics
curl -X POST http://localhost:5000/api/analytics/statistics \
  -H "Content-Type: application/json" \
  -d '{"projects": ["PROD"], "days_back": 30}'

# 2. Get insights
curl -X POST http://localhost:5000/api/insights \
  -H "Content-Type: application/json" \
  -d '{"projects": ["PROD"], "days_back": 30}'
```

### Use Case 3: Search Historical Tickets

```bash
# Search for resolved tickets in last 60 days
curl -X POST http://localhost:5000/api/tickets/search \
  -H "Content-Type: application/json" \
  -d '{
    "projects": ["PROD", "TECH"],
    "statuses": ["Done", "Resolved"],
    "days_back": 60,
    "max_results": 100
  }'
```

---

## SDK / Client Libraries

Currently, the API is accessed via HTTP requests. Future plans include:
- Python client library
- JavaScript/Node.js client
- CLI tool

---

## Postman Collection

Import this collection for easy testing:

```json
{
  "info": {
    "name": "JIRA AI Agent API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["health"]
        }
      }
    }
  ]
}
```

---

## Support

For API questions or issues:
- Check this documentation
- Review [README.md](README.md) for general help
- Open an issue on GitHub
- Check examples in `examples/demo.py`

---

**Last Updated:** October 2025  
**API Version:** 0.1.0
