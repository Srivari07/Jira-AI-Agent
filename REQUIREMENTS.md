# JIRA AI Agent - Installation & Setup Requirements

## System Requirements

- Python 3.10 or higher
- uv (recommended) or pip (Python package manager)
- Git
- 4GB RAM minimum (8GB recommended)
- Internet connection for API calls

## Installing uv (Recommended)

uv is a fast Python package installer and resolver written in Rust. It's much faster than pip.

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or using pip:**
```bash
pip install uv
```

## Python Dependencies

Install all dependencies using:
```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### Core Dependencies
- **fastmcp>=0.2.0** - MCP server framework
- **langchain>=0.3.0** - LLM application framework
- **langchain-groq>=0.2.0** - Groq LLM integration
- **langchain-community>=0.3.0** - Community integrations
- **flask>=3.0.0** - Web framework for API
- **flask-cors>=4.0.0** - CORS support
- **streamlit>=1.31.0** - Frontend framework
- **python-dotenv>=1.0.0** - Environment variable management
- **jira>=3.8.0** - JIRA API client
- **requests>=2.31.0** - HTTP library
- **pandas>=2.2.0** - Data manipulation
- **plotly>=5.18.0** - Visualization
- **python-dateutil>=2.8.2** - Date utilities
- **pydantic>=2.5.0** - Data validation
- **pyyaml>=6.0.1** - YAML configuration

## External Services

### 1. JIRA Account
- Active JIRA Cloud or Server instance
- Admin or appropriate permissions to access tickets
- API token generation capability

**Setup:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create API token
3. Note your JIRA URL (e.g., https://yourcompany.atlassian.net)

### 2. Groq API Access
- Free or paid Groq account
- API key for Llama model access

**Setup:**
1. Visit https://console.groq.com/
2. Sign up for account
3. Generate API key from dashboard
4. Copy API key to .env file

## Environment Setup

Create a `.env` file in the project root with:

```env
# JIRA Configuration (Required)
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token

# Groq API Configuration (Required)
GROQ_API_KEY=your_groq_api_key

# LLM Configuration (Optional)
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048

# Flask Configuration (Optional)
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True

# Streamlit Configuration (Optional)
STREAMLIT_PORT=8501

# Application Settings (Optional)
MAX_HISTORICAL_TICKETS=100
SIMILARITY_THRESHOLD=0.7
```

## Troubleshooting Installation

### Issue: pip install fails
**Solution:**
```bash
# Using uv (recommended)
uv pip install -e . --refresh

# Or upgrade pip
python -m pip install --upgrade pip
pip install -e . --no-cache-dir
```

### Issue: Module not found errors
**Solution:**
```bash
# Ensure virtual environment is activated
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Reinstall with uv
uv pip install -e .
```

### Issue: JIRA connection fails
**Solution:**
- Verify JIRA_URL format (include https://)
- Check API token is not expired
- Verify email matches JIRA account
- Test connection: `curl -u email:token https://your-domain.atlassian.net/rest/api/3/myself`

### Issue: Groq API errors
**Solution:**
- Verify API key is valid
- Check Groq service status
- Ensure you have API credits/quota
- Try different model if rate limited

## Network Requirements

### Firewall/Proxy Settings
If behind corporate firewall, ensure access to:
- *.groq.com (Groq API)
- *.atlassian.net (JIRA API)
- huggingface.co (for embeddings model download)

### Ports
- 5000 (Flask Backend)
- 8501 (Streamlit Frontend)

### Optional: Development Tools

For development, consider installing:
```bash
# Using uv
uv pip install pytest black flake8 mypy

# Or using pip
pip install pytest black flake8 mypy
```

## Verification Steps

After installation:

1. **Check Python version:**
```bash
python --version  # Should be 3.10+
```

2. **Verify dependencies:**
```bash
uv pip list | grep -E "fastmcp|langchain|flask|streamlit"
# Or on Windows PowerShell:
uv pip list | Select-String "fastmcp|langchain|flask|streamlit"
```

3. **Test JIRA connection:**
```bash
python -c "from src.mcp_server.jira_mcp_server import JiraClient; client = JiraClient(); print('JIRA OK')"
```

4. **Test LLM connection:**
```bash
python -c "from src.backend.llm_agent import JiraLLMAgent; agent = JiraLLMAgent(); print('LLM OK')"
```

5. **Start services:**
```bash
# Terminal 1
python main.py backend

# Terminal 2
python main.py frontend
```

## Next Steps

After successful installation:
1. Configure `config/config.yaml` with your JIRA projects
2. Run the application using startup scripts
3. Access http://localhost:8501 for the UI
4. See MCP_SETUP.md for editor integration

## Support

If issues persist:
- Check the README.md for detailed documentation
- Review error logs in the console
- Ensure all prerequisites are met
- Contact support or open an issue on GitHub
