# 🚀 Quick Start Guide - JIRA AI Agent

Get up and running in 5 minutes!

## Prerequisites Checklist
- [ ] Python 3.10+ installed
- [ ] JIRA account with API access
- [ ] Groq API key
- [ ] Git installed

## Step-by-Step Setup

### 1️⃣ Get the Code (1 minute)

```bash
git clone https://github.com/yourusername/Jira-AI-Agent.git
cd Jira-AI-Agent
```

### 2️⃣ Setup Python Environment (1 minute)

```bash
# Create virtual environment with uv (recommended - much faster!)
uv venv

# Activate it
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies with uv
uv pip install -e .

# Or use pip if you prefer
pip install -e .
```

### 3️⃣ Configure Credentials (2 minutes)

Copy the example environment file:
```bash
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac
```

Edit `.env` and add your credentials:
```env
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your_jira_token_here
GROQ_API_KEY=your_groq_key_here
```

**Getting Credentials:**
- **JIRA Token**: https://id.atlassian.com/manage-profile/security/api-tokens
- **Groq Key**: https://console.groq.com/ (free signup)

### 4️⃣ Start the Application (1 minute)

**Option A: Windows (Easy)**
```bash
# Terminal 1 - Start Backend
start_backend.bat

# Terminal 2 - Start Frontend  
start_frontend.bat
```

**Option B: Any OS (Command Line)**
```bash
# Terminal 1 - Start Backend
python main.py backend

# Terminal 2 - Start Frontend
python main.py frontend
```

### 5️⃣ Use the Application

Open your browser to: **http://localhost:8501**

You should see the JIRA AI Agent interface! 🎉

## First Query Test

1. Go to the "Query Assistant" page
2. Enter a test query: "How do I fix authentication errors?"
3. Click "Search & Analyze"
4. View matched tickets and AI-generated resolution

## Troubleshooting

### ❌ "Cannot connect to JIRA"
- Check your JIRA URL format (must include https://)
- Verify API token is correct
- Test with: `curl -u email:token https://your-jira-url/rest/api/3/myself`

### ❌ "Groq API error"
- Check API key is valid
- Visit https://console.groq.com/ to verify account
- Ensure you have API quota remaining

### ❌ "Module not found"
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -e . --force-reinstall
```

### ❌ "Port already in use"
```bash
# Change ports in .env
FLASK_PORT=5001
STREAMLIT_PORT=8502
```

## Next Steps

✅ You're ready! Now you can:

1. **Configure your projects** - Edit `config/config.yaml`
2. **Explore the UI** - Try different features
3. **Check analytics** - View ticket statistics
4. **Read full docs** - See README.md for advanced features
5. **Integrate with editor** - See MCP_SETUP.md for VS Code/Cursor

## Quick Demo

Want to see it in action without setting up JIRA? Run the demo:

```bash
# Make sure backend is running
python examples/demo.py
```

This will show example API calls and responses.

## Architecture Overview

```
You → Streamlit UI → Flask API → ChatGroq LLM
                            ↓
                      JIRA MCP Server → JIRA API
```

## Common Use Cases

### 🔍 Search Historical Tickets
Navigate to "Ticket Search" → Filter by project/status → Browse results

### 💡 Get AI Resolution
"Query Assistant" → Enter your problem → Get matched tickets + solution

### 📊 View Analytics
"Analytics Dashboard" → Select time range → View trends and insights

### ⚙️ Configure Settings
"Settings" → Update JIRA projects → Adjust LLM parameters

## Support & Resources

- 📖 **Full Documentation**: [README.md](README.md)
- 🔌 **Editor Integration**: [MCP_SETUP.md](MCP_SETUP.md)
- 🐛 **Issues**: Open on GitHub
- 💬 **Questions**: Check documentation first

## What's Next?

Now that you have the basics working:

1. Add your real JIRA projects to `config/config.yaml`
2. Try different types of queries
3. Explore the analytics features
4. Integrate with your IDE (see MCP_SETUP.md)
5. Share with your team!

---

**🎉 Congratulations! You're now using JIRA AI Agent!**

For advanced configuration and features, see the full [README.md](README.md).
