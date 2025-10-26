# 🏗️ JIRA AI Agent - System Architecture

Visual overview of the system architecture and data flow.

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │ Query Assistant│  │ Ticket Search  │  │ Analytics Dashboard│ │
│  └────────┬───────┘  └────────┬───────┘  └──────────┬─────────┘ │
│           │                   │                      │           │
│           └───────────────────┴──────────────────────┘           │
│                                │                                 │
│                    Streamlit Frontend (Port 8501)               │
└─────────────────────────────────┬───────────────────────────────┘
                                  │ HTTP Requests
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REST API LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                     Flask Backend (Port 5000)                   │
│                                                                 │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────────────┐ │
│  │ /api/query   │  │/api/tickets │  │ /api/analytics/insights│ │
│  └──────┬───────┘  └──────┬──────┘  └───────────┬────────────┘ │
│         │                 │                      │              │
│         └─────────────────┴──────────────────────┘              │
└─────────────┬───────────────────────────┬───────────────────────┘
              │                           │
    ┌─────────▼─────────┐       ┌────────▼──────────┐
    │                   │       │                   │
    │   LLM AGENT       │       │  JIRA MCP SERVER  │
    │  (llm_agent.py)   │       │(jira_mcp_server.py)│
    │                   │       │                   │
    └─────────┬─────────┘       └─────────┬─────────┘
              │                           │
    ┌─────────▼──────────┐      ┌─────────▼──────────┐
    │                    │      │                    │
    │  ChatGroq API      │      │    JIRA API        │
    │ (Llama 3.1 LLM)    │      │  (Cloud/Server)    │
    │                    │      │                    │
    └────────────────────┘      └────────────────────┘
```

## 🔄 Request Flow Diagram

### Query Processing Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Enters Query
     ▼
┌─────────────────┐
│ Streamlit UI    │
│ Query Assistant │
└────┬────────────┘
     │ 2. HTTP POST to /api/query
     ▼
┌─────────────────┐
│   Flask API     │
│   api.py        │
└────┬────────────┘
     │
     ├─── 3. Analyze Query ────────────┐
     │                                  ▼
     │                       ┌──────────────────┐
     │                       │   LLM Agent      │
     │                       │ (llm_agent.py)   │
     │                       │                  │
     │                       │ • Extract terms  │
     │                       │ • Identify type  │
     │                       │ • Assess priority│
     │                       └──────────────────┘
     │                                  │
     │◄──── 4. Query Analysis ──────────┘
     │
     ├─── 5. Fetch Historical Tickets ─┐
     │                                  ▼
     │                       ┌──────────────────┐
     │                       │  JIRA MCP Server │
     │                       │(jira_mcp_server) │
     │                       │                  │
     │                       │ • Search tickets │
     │                       │ • Filter by     │
     │                       │   projects      │
     │                       └────────┬─────────┘
     │                                │
     │                                ▼
     │                       ┌──────────────────┐
     │                       │    JIRA API      │
     │                       │                  │
     │                       │ • Fetch tickets  │
     │                       │ • Get comments   │
     │                       │ • Get metadata   │
     │                       └────────┬─────────┘
     │                                │
     │◄──── 6. Historical Tickets ────┘
     │
     ├─── 7. Match & Score ────────────┐
     │                                  ▼
     │                       ┌──────────────────┐
     │                       │   LLM Agent      │
     │                       │                  │
     │                       │ • Compare query  │
     │                       │   with tickets   │
     │                       │ • Calculate      │
     │                       │   relevance      │
     │                       │ • Rank results   │
     │                       └──────────────────┘
     │                                  │
     │◄──── 8. Matched Tickets ─────────┘
     │
     ├─── 9. Generate Resolution ──────┐
     │                                  ▼
     │                       ┌──────────────────┐
     │                       │   ChatGroq LLM   │
     │                       │                  │
     │                       │ • Synthesize     │
     │                       │   solution       │
     │                       │ • Reference      │
     │                       │   tickets        │
     │                       └──────────────────┘
     │                                  │
     │◄──── 10. AI Resolution ──────────┘
     │
     ▼
┌─────────────────┐
│   Flask API     │
│  (Aggregates)   │
└────┬────────────┘
     │ 11. JSON Response
     ▼
┌─────────────────┐
│ Streamlit UI    │
│  (Displays)     │
└────┬────────────┘
     │ 12. Rendered UI
     ▼
┌─────────┐
│  User   │
│ (Views) │
└─────────┘
```

## 📊 Component Interaction Matrix

```
┌──────────────┬──────────┬──────────┬────────────┬──────────┐
│ Component    │ Frontend │ Flask API│ LLM Agent  │ MCP Srvr │
├──────────────┼──────────┼──────────┼────────────┼──────────┤
│ Frontend     │    -     │   HTTP   │     -      │    -     │
│ Flask API    │  JSON    │    -     │  Function  │ Function │
│ LLM Agent    │    -     │  Return  │     -      │    -     │
│ MCP Server   │    -     │  Return  │     -      │    -     │
│ JIRA API     │    -     │    -     │     -      │   HTTP   │
│ Groq API     │    -     │    -     │    HTTP    │    -     │
└──────────────┴──────────┴──────────┴────────────┴──────────┘
```

## 🔐 Data Flow & Security

```
┌─────────────────────────────────────────────────────────┐
│                    CONFIGURATION                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────────────────┐   │
│  │   .env       │─────▶│  Environment Variables   │   │
│  │              │      │  • JIRA_URL              │   │
│  │  Credentials │      │  • JIRA_TOKEN            │   │
│  │  API Keys    │      │  • GROQ_API_KEY          │   │
│  └──────────────┘      └──────────────────────────┘   │
│                                                         │
│  ┌──────────────┐      ┌──────────────────────────┐   │
│  │ config.yaml  │─────▶│  Application Settings    │   │
│  │              │      │  • Projects              │   │
│  │  Settings    │      │  • LLM Parameters        │   │
│  │  Preferences │      │  • Analytics Config      │   │
│  └──────────────┘      └──────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │    Application Layer    │
              │   (Reads Config Once)   │
              └─────────────────────────┘
```

## 🎭 State Management

```
┌─────────────────────────────────────────────────────┐
│              STREAMLIT SESSION STATE                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  • User Queries (History)                          │
│  • Current Page State                              │
│  • Selected Filters                                │
│  • Cached Results (Temporary)                      │
│                                                     │
└─────────────────────────────────────────────────────┘
            │                           │
            ▼                           ▼
┌───────────────────┐         ┌──────────────────┐
│  Flask API        │         │   JIRA MCP       │
│  (Stateless)      │         │   (Stateless)    │
└───────────────────┘         └──────────────────┘
```

## 📈 Scalability Model

```
Current (v0.1.0):
┌────────┐    ┌────────┐    ┌─────────┐
│ Client │───▶│  API   │───▶│  JIRA   │
└────────┘    └────────┘    └─────────┘
                  │
                  ▼
              ┌────────┐
              │  LLM   │
              └────────┘

Future (Planned):
┌────────┐    ┌──────────┐    ┌─────────┐
│Client 1│───▶│          │    │  JIRA   │
├────────┤    │  Load    │───▶├─────────┤
│Client 2│───▶│ Balancer │    │  Cache  │
├────────┤    │          │    └─────────┘
│Client N│───▶│          │         │
└────────┘    └──────────┘         ▼
                  │            ┌─────────┐
                  │            │ Database│
                  ▼            └─────────┘
            ┌──────────┐
            │ LLM Pool │
            └──────────┘
```

## 🧩 Module Dependencies

```
┌──────────────────────────────────────────────────┐
│                  Application                     │
└──────────┬───────────────────────────────────────┘
           │
    ┌──────┴──────┬──────────────┬─────────────┐
    │             │              │             │
┌───▼────┐  ┌────▼─────┐  ┌─────▼──────┐  ┌──▼────┐
│Frontend│  │ Backend  │  │ MCP Server │  │Config │
│(Streamlit)│  (Flask)  │  │ (FastMCP)  │  │(YAML) │
└───┬────┘  └────┬─────┘  └─────┬──────┘  └──┬────┘
    │            │               │             │
    │       ┌────▼─────┐    ┌────▼────┐       │
    │       │LLM Agent │    │  JIRA   │       │
    │       │          │    │ Client  │       │
    │       └────┬─────┘    └────┬────┘       │
    │            │               │             │
    │       ┌────▼─────┐    ┌────▼────┐       │
    │       │ ChatGroq │    │  JIRA   │       │
    │       │   API    │    │   API   │       │
    │       └──────────┘    └─────────┘       │
    │                                          │
    └──────────────────┬───────────────────────┘
                       │
                  ┌────▼─────┐
                  │  Utils   │
                  │ (Shared) │
                  └──────────┘
```

## 🎯 Technology Stack Layers

```
┌─────────────────────────────────────────────┐
│         PRESENTATION LAYER                  │
│         Streamlit 1.31+                     │
│         HTML/CSS (Auto-generated)           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         APPLICATION LAYER                   │
│         Flask 3.0+ (REST API)               │
│         Business Logic                      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         INTEGRATION LAYER                   │
│         FastMCP 0.2+ (MCP Server)           │
│         Langchain 0.3+ (LLM Framework)      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         EXTERNAL SERVICES                   │
│  ┌─────────────┐      ┌─────────────────┐  │
│  │  JIRA API   │      │  ChatGroq API   │  │
│  │ (Atlassian) │      │    (Groq)       │  │
│  └─────────────┘      └─────────────────┘  │
└─────────────────────────────────────────────┘
```

## 🔍 Query Processing Pipeline

```
Query Input
    │
    ▼
[Preprocessing]
• Clean text
• Extract keywords
• Normalize
    │
    ▼
[Query Analysis]
• LLM analysis
• Issue type detection
• Priority assessment
    │
    ▼
[Ticket Retrieval]
• Search JIRA
• Apply filters
• Fetch metadata
    │
    ▼
[Matching]
• Calculate similarity
• Rank tickets
• Score relevance
    │
    ▼
[Resolution Generation]
• Synthesize from matches
• Format response
• Add references
    │
    ▼
[Response Formatting]
• Structure JSON
• Add metadata
• Prepare UI data
    │
    ▼
Display to User
```

## 📦 Deployment Architecture

```
Development:
┌─────────────────┐
│  Local Machine  │
│                 │
│  ┌───────────┐  │
│  │ Backend   │  │
│  │ (5000)    │  │
│  └───────────┘  │
│  ┌───────────┐  │
│  │ Frontend  │  │
│  │ (8501)    │  │
│  └───────────┘  │
└─────────────────┘

Production (Future):
┌─────────────────┐
│   Cloud Server  │
│                 │
│  ┌───────────┐  │
│  │  Nginx    │  │
│  │ (Reverse  │  │
│  │  Proxy)   │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │Gunicorn   │  │
│  │+ Flask    │  │
│  └───────────┘  │
│  ┌───────────┐  │
│  │ Streamlit │  │
│  └───────────┘  │
└─────────────────┘
```

---

For more details:
- See PROJECT_STRUCTURE.md for file organization
- See README.md for complete documentation
- See API_DOCS.md for API endpoints
