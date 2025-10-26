# 📦 JIRA AI Agent - Project Structure

Complete overview of the project organization and files.

## 📂 Root Directory

```
Jira-AI-Agent/
├── 📄 README.md                  # Main documentation
├── 📄 QUICKSTART.md              # 5-minute setup guide
├── 📄 REQUIREMENTS.md            # Detailed requirements & setup
├── 📄 API_DOCS.md                # Complete API reference
├── 📄 MCP_SETUP.md               # MCP Server integration guide
├── 📄 LICENSE                    # MIT License
├── 📄 .gitignore                 # Git ignore rules
├── 📄 .env.example               # Example environment variables
├── 📄 pyproject.toml             # Python project configuration
├── 📄 main.py                    # CLI entry point
├── 💻 start_backend.bat          # Windows: Start backend
├── 💻 start_frontend.bat         # Windows: Start frontend
├── 💻 start_mcp.bat              # Windows: Start MCP server
├── 📁 config/                    # Configuration files
├── 📁 src/                       # Source code
├── 📁 tests/                     # Test files
└── 📁 examples/                  # Usage examples
```

---

## 📁 config/ - Configuration

```
config/
└── 📄 config.yaml                # Application settings
    ├── jira:                     # JIRA project settings
    │   ├── projects              # Project keys to analyze
    │   ├── issue_types           # Issue types to include
    │   ├── resolved_statuses     # Statuses to consider
    │   └── fields                # Fields to fetch
    ├── llm:                      # LLM configuration
    │   ├── model                 # Model name
    │   ├── temperature           # Creativity level
    │   ├── max_tokens            # Response length
    │   ├── similarity_threshold  # Matching threshold
    │   └── top_k_results         # Number of results
    ├── analytics:                # Analytics settings
    │   ├── enabled               # Enable/disable
    │   ├── metrics               # Metrics to track
    │   └── time_ranges           # Time ranges to analyze
    └── agent:                    # Agent behavior
        ├── auto_suggest          # Auto-suggest resolutions
        ├── attach_documents      # Attach documents
        ├── confidence_threshold  # Confidence level
        └── max_suggestions       # Max suggestions
```

---

## 📁 src/ - Source Code

### src/backend/ - Backend Services

```
src/backend/
├── 📄 __init__.py                # Package initializer
├── 📄 api.py                     # Flask REST API
│   ├── /health                   # Health check endpoint
│   ├── /api/query                # Query processing
│   ├── /api/tickets/search       # Ticket search
│   ├── /api/tickets/<key>        # Get ticket details
│   ├── /api/analytics/statistics # Statistics endpoint
│   └── /api/insights             # AI insights
├── 📄 llm_agent.py               # LLM Integration
│   ├── JiraLLMAgent              # Main agent class
│   ├── analyze_query()           # Query analysis
│   ├── match_tickets()           # Ticket matching
│   ├── generate_resolution()    # Resolution generation
│   └── extract_key_insights()   # Insights extraction
├── 📄 config_manager.py          # Configuration Management
│   ├── ConfigManager             # Config handler
│   ├── _load_config()            # Load YAML config
│   ├── _load_env_vars()          # Load environment vars
│   └── validate()                # Validate config
└── 📄 utils.py                   # Utility Functions
    ├── clean_text()              # Text cleaning
    ├── extract_keywords()        # Keyword extraction
    ├── calculate_similarity()    # Similarity scoring
    ├── format_ticket_summary()   # Ticket formatting
    └── calculate_resolution_time() # Time calculation
```

### src/mcp_server/ - MCP Server

```
src/mcp_server/
├── 📄 __init__.py                # Package initializer
└── 📄 jira_mcp_server.py         # FastMCP JIRA Server
    ├── JiraClient                # JIRA client wrapper
    │   ├── search_tickets()      # Search functionality
    │   └── get_ticket_by_key()   # Get specific ticket
    ├── @mcp.tool()
    │   ├── search_historical_tickets()
    │   ├── get_ticket_details()
    │   ├── get_recent_resolved_tickets()
    │   └── get_ticket_statistics()
    └── if __name__ == "__main__":
        └── mcp.run()             # Start MCP server
```

### src/frontend/ - Streamlit UI

```
src/frontend/
├── 📄 __init__.py                # Package initializer
└── 📄 app.py                     # Streamlit Application
    ├── main()                    # Main entry point
    ├── query_assistant_page()    # Query assistant UI
    │   ├── Query input
    │   ├── Query analysis display
    │   ├── Matched tickets
    │   └── AI resolution
    ├── ticket_search_page()      # Ticket search UI
    │   ├── Search filters
    │   ├── Results table
    │   └── Ticket details
    ├── analytics_dashboard_page() # Analytics UI
    │   ├── Statistics metrics
    │   ├── Charts (status, priority, project)
    │   └── AI insights
    ├── settings_page()           # Settings UI
    │   ├── JIRA configuration
    │   ├── LLM settings
    │   └── Agent settings
    └── Helper functions
        ├── display_ticket_details()
        └── display_quick_stats()
```

---

## 📁 tests/ - Test Suite

```
tests/
├── 📄 __init__.py                # Package initializer
└── 📄 test_basic.py              # Basic tests
    ├── TestUtils                 # Utility function tests
    │   ├── test_clean_text()
    │   ├── test_extract_keywords()
    │   ├── test_calculate_similarity()
    │   └── test_truncate_text()
    ├── TestConfigValidation      # Config validation tests
    │   ├── test_validate_config_valid()
    │   └── test_validate_config_invalid()
    └── TestAPIIntegration        # Integration tests
        ├── test_health_endpoint()
        └── test_query_endpoint()
```

---

## 📁 examples/ - Usage Examples

```
examples/
└── 📄 demo.py                    # Interactive demo
    ├── test_health()             # Health check example
    ├── example_query()           # Query processing
    ├── example_search_tickets()  # Ticket search
    ├── example_get_statistics()  # Statistics example
    ├── example_get_insights()    # Insights example
    └── main()                    # Interactive menu
```

---

## 📄 Key Files Explained

### pyproject.toml
Python project configuration with all dependencies:
- FastMCP, Langchain, ChatGroq
- Flask, Streamlit
- JIRA client, Pandas, Plotly
- All required packages

### .env.example
Template for environment variables:
- JIRA credentials (URL, email, token)
- Groq API key
- LLM configuration
- Flask/Streamlit ports

### main.py
CLI entry point to start components:
```bash
python main.py backend   # Start Flask API
python main.py frontend  # Start Streamlit UI
python main.py mcp       # Start MCP Server
```

### Batch Files (Windows)
Quick start scripts:
- `start_backend.bat` - Start Flask API
- `start_frontend.bat` - Start Streamlit UI
- `start_mcp.bat` - Start MCP Server

---

## 🔄 Data Flow

```
User Input (Query)
    ↓
Streamlit UI (app.py)
    ↓
Flask API (api.py)
    ↓
    ├─→ LLM Agent (llm_agent.py)
    │   ├─→ ChatGroq API
    │   └─→ Query Analysis & Resolution
    │
    └─→ JIRA MCP Server (jira_mcp_server.py)
        └─→ JIRA API
            └─→ Historical Tickets
```

---

## 🎯 Component Responsibilities

### Backend (Flask API)
- **Purpose**: REST API layer
- **Responsibilities**:
  - Handle HTTP requests
  - Coordinate between LLM and JIRA
  - Provide data to frontend
- **Port**: 5000

### Frontend (Streamlit)
- **Purpose**: User interface
- **Responsibilities**:
  - Display query results
  - Show analytics
  - Provide settings interface
- **Port**: 8501

### MCP Server (FastMCP)
- **Purpose**: JIRA integration
- **Responsibilities**:
  - Fetch historical tickets
  - Search JIRA API
  - Provide MCP tools for editors
- **Usage**: Can run standalone or via API

### LLM Agent (ChatGroq)
- **Purpose**: AI processing
- **Responsibilities**:
  - Analyze queries
  - Match tickets
  - Generate resolutions
  - Extract insights

---

## 📊 File Statistics

- **Python Files**: 11
- **Configuration Files**: 2
- **Documentation Files**: 5
- **Batch Scripts**: 3
- **Test Files**: 1
- **Total Lines of Code**: ~3,500+

---

## 🔧 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Flask + Python | REST API |
| Frontend | Streamlit | Web UI |
| LLM | ChatGroq (Llama 3.1) | AI Processing |
| Integration | FastMCP | JIRA MCP Server |
| Data Source | JIRA API | Ticket Data |
| Config | YAML + .env | Settings |
| Analytics | Pandas + Plotly | Data Visualization |

---

## 🚀 Getting Started Paths

### Path 1: Web Application
1. Start backend: `start_backend.bat`
2. Start frontend: `start_frontend.bat`
3. Access: http://localhost:8501

### Path 2: API Only
1. Start backend: `python main.py backend`
2. Use API: See API_DOCS.md

### Path 3: MCP Integration
1. Configure MCP: See MCP_SETUP.md
2. Start MCP: `python main.py mcp`
3. Use in VS Code/Cursor

---

## 📚 Documentation Index

1. **README.md** - Overview, features, full setup
2. **QUICKSTART.md** - 5-minute setup guide
3. **API_DOCS.md** - Complete API reference
4. **MCP_SETUP.md** - Editor integration
5. **REQUIREMENTS.md** - Detailed requirements
6. **This File** - Project structure

---

## 🎓 Learning Path

1. **Beginner**: Start with QUICKSTART.md
2. **User**: Read README.md
3. **Developer**: Review this file + source code
4. **API User**: Check API_DOCS.md
5. **Integrator**: See MCP_SETUP.md

---

## 🔮 Future Additions

Potential new files/directories:
- `docker/` - Docker configuration
- `ci/` - CI/CD pipelines
- `docs/` - Extended documentation
- `migrations/` - Database migrations
- `scripts/` - Utility scripts
- `benchmarks/` - Performance tests

---

**Project Status**: ✅ Complete & Ready for Use

For questions about specific files or components, refer to the inline code documentation or the relevant documentation files.
