# 🤖 JIRA AI Agent

> **Intelligent Technical Support Assistant** - Resolves Product and Technical Queries by analyzing historical JIRA tickets using AI-powered matching and resolution generation.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-Latest-green)](https://github.com/jlowin/fastmcp)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🌟 Overview

In the fast-paced world of technical support, repetitive issues consume valuable time for developers and support engineers. **JIRA AI Agent** solves this problem by leveraging historical data to efficiently resolve queries, enabling teams to focus on critical and high-priority tasks.

The agent uses advanced AI (Groq's Llama LLM) to analyze incoming queries, match them with similar historical JIRA tickets, and automatically suggest resolutions based on past solutions.

## ✨ Features

### Core Capabilities
- 🎯 **Smart Query Matching** - Matches incoming queries with historical JIRA tickets using semantic search
- 💡 **AI-Powered Resolutions** - Suggests resolutions or attaches relevant documents automatically
- 📊 **Analytics Dashboard** - Visualizes ticket trends, patterns, and resolution metrics
- 🔄 **Real-time JIRA Integration** - Integrates JIRA MCP seamlessly with VS Code Copilot and Cursor
- ⚙️ **Customizable Configuration** - Team-specific JIRA projects and settings
- 🚀 **Easy Frontend Integration** - Works with Streamlit or any frontend technology

### Advanced Features
- Query analysis with issue type and priority detection
- Multi-project support with filtering
- Historical ticket search with customizable time ranges
- Relevance scoring for ticket matches
- Automated insights extraction from ticket patterns
- Real-time statistics and analytics

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │ ◄── User Interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │ ◄── REST API Layer
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ ChatGroq│ │  JIRA MCP    │
│  LLM    │ │   Server     │
└─────────┘ └──────┬───────┘
                   │
                   ▼
            ┌──────────────┐
            │  JIRA API    │
            └──────────────┘
```

## 🛠️ Tech Stack

- **Backend**: Python, Flask, FastMCP, Langchain
- **LLM**: ChatGroq (Llama 3.1-70b-versatile)
- **Frontend**: Streamlit
- **Integration**: JIRA API via MCP Server
- **Data Processing**: Pandas, Plotly
- **Embeddings**: HuggingFace Sentence Transformers

## 📋 Prerequisites

- Python 3.10 or higher
- JIRA account with API access
- Groq API key (for Llama LLM)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Jira-AI-Agent.git
cd Jira-AI-Agent
```

### 2. Create Virtual Environment

```bash
# Using uv (recommended - much faster)
uv venv

# Activate virtual environment
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### 4. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac
```

Edit `.env` with your credentials:

```env
# JIRA Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key

# LLM Configuration (Optional - defaults provided)
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
```

#### Getting JIRA API Token
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label and copy the token

#### Getting Groq API Key
1. Visit https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

### 5. Configure Projects

Edit `config/config.yaml` to specify your JIRA projects and preferences:

```yaml
jira:
  projects:
    - "PROD"  # Your project keys
    - "TECH"
    - "SUP"
  
  issue_types:
    - "Bug"
    - "Task"
    - "Story"
  
  resolved_statuses:
    - "Done"
    - "Resolved"
    - "Closed"
```

### 6. Start the Application

#### Option A: Start All Components (Recommended for Development)

**Terminal 1 - Backend API:**
```bash
# Windows
start_backend.bat

# Linux/Mac
python src/backend/api.py
```

**Terminal 2 - Frontend UI:**
```bash
# Windows
start_frontend.bat

# Linux/Mac
streamlit run src/frontend/app.py
```

#### Option B: MCP Server Only (For VS Code/Cursor Integration)

```bash
# Windows
start_mcp.bat

# Linux/Mac
python src/mcp_server/jira_mcp_server.py
```

### 7. Access the Application

- **Streamlit Frontend**: http://localhost:8501
- **Flask API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## 📖 Usage Guide

### Using the Web Interface

1. **Query Assistant**
   - Enter your technical question or problem description
   - Select relevant projects
   - Click "Search & Analyze"
   - View matched tickets and AI-generated resolution

2. **Ticket Search**
   - Filter by status, time range, and project
   - Browse historical tickets
   - View detailed ticket information

3. **Analytics Dashboard**
   - View ticket statistics and trends
   - Analyze common issues and resolutions
   - Get AI-generated insights

### Using the API

#### Process a Query

```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I fix authentication errors?",
    "projects": ["PROD", "TECH"],
    "max_results": 5
  }'
```

#### Search Tickets

```bash
curl -X POST http://localhost:5000/api/tickets/search \
  -H "Content-Type: application/json" \
  -d '{
    "projects": ["PROD"],
    "days_back": 30,
    "max_results": 50
  }'
```

#### Get Statistics

```bash
curl -X POST http://localhost:5000/api/analytics/statistics \
  -H "Content-Type: application/json" \
  -d '{
    "projects": ["PROD", "TECH"],
    "days_back": 30
  }'
```

### Using MCP with VS Code Copilot / Cursor

See [MCP_SETUP.md](MCP_SETUP.md) for detailed instructions on integrating with:
- VS Code Copilot Chat
- Cursor AI Editor
- Other MCP-compatible tools

## 🔧 Configuration

### Application Settings

Edit `config/config.yaml` to customize:

- **JIRA Projects**: Which projects to analyze
- **Issue Types**: Bug, Task, Story, etc.
- **LLM Settings**: Temperature, max tokens, similarity threshold
- **Analytics**: Metrics to track, time ranges
- **Agent Behavior**: Auto-suggest, confidence thresholds

### Environment Variables

Key environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `JIRA_URL` | Your JIRA instance URL | Required |
| `JIRA_EMAIL` | JIRA account email | Required |
| `JIRA_API_TOKEN` | JIRA API token | Required |
| `GROQ_API_KEY` | Groq API key for LLM | Required |
| `LLM_MODEL` | Llama model to use | `llama-3.1-70b-versatile` |
| `LLM_TEMPERATURE` | LLM creativity (0-1) | `0.7` |
| `FLASK_PORT` | Backend API port | `5000` |
| `STREAMLIT_PORT` | Frontend UI port | `8501` |

## 📁 Project Structure

```
Jira-AI-Agent/
├── config/
│   └── config.yaml           # Application configuration
├── src/
│   ├── backend/
│   │   ├── api.py            # Flask REST API
│   │   ├── llm_agent.py      # LLM integration & query matching
│   │   ├── config_manager.py # Configuration loader
│   │   └── utils.py          # Utility functions
│   ├── mcp_server/
│   │   └── jira_mcp_server.py # FastMCP JIRA server
│   └── frontend/
│       └── app.py            # Streamlit UI
├── .env.example              # Example environment file
├── .gitignore               # Git ignore rules
├── pyproject.toml           # Project dependencies
├── README.md                # This file
├── MCP_SETUP.md            # MCP integration guide
├── start_backend.bat       # Start backend (Windows)
├── start_frontend.bat      # Start frontend (Windows)
└── start_mcp.bat           # Start MCP server (Windows)
```

## 🎯 Use Cases

1. **Technical Support Teams**
   - Quickly resolve recurring customer issues
   - Reduce response time for common problems
   - Build knowledge base from historical data

2. **Development Teams**
   - Find solutions to known bugs
   - Reference past implementations
   - Identify patterns in technical issues

3. **Product Teams**
   - Analyze product-related queries
   - Track feature requests and issues
   - Understand common user pain points

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP Server framework
- [Groq](https://groq.com/) - Lightning-fast LLM inference
- [Langchain](https://www.langchain.com/) - LLM application framework
- [Streamlit](https://streamlit.io/) - Web UI framework
- [Atlassian JIRA](https://www.atlassian.com/software/jira) - Issue tracking

## 📧 Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Contact the maintainers
- Check the documentation

## 🔮 Roadmap

- [ ] Support for multiple LLM providers (OpenAI, Anthropic, etc.)
- [ ] Advanced caching for faster responses
- [ ] Integration with Slack/Teams for notifications
- [ ] Custom fine-tuning on team-specific data
- [ ] Export functionality for reports
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

**Made with ❤️ for better technical support workflows**
