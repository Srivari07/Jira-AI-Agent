# 🚀 Free Deployment Guide for JIRA AI Agent

This guide covers multiple free deployment options for your JIRA AI Agent project.

---

## 📋 Table of Contents

1. [Render.com (Recommended)](#1-rendercom-recommended)
2. [Railway.app](#2-railwayapp)
3. [Streamlit Cloud + Backend on Render](#3-streamlit-cloud--backend-on-render)
4. [Hugging Face Spaces](#4-hugging-face-spaces)
5. [PythonAnywhere](#5-pythonanywhere)

---

## 1. Render.com (Recommended)

**Free Tier**: 750 hours/month, automatic SSL, custom domains

### Step 1: Prepare Your Project

Create `render.yaml` in project root:

```yaml
services:
  # Backend API
  - type: web
    name: jira-ai-agent-backend
    env: python
    buildCommand: "pip install -e ."
    startCommand: "python src/backend/api.py"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: JIRA_URL
        sync: false
      - key: JIRA_EMAIL
        sync: false
      - key: JIRA_API_TOKEN
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: FLASK_HOST
        value: 0.0.0.0
      - key: FLASK_PORT
        value: 10000

  # Frontend Streamlit App
  - type: web
    name: jira-ai-agent-frontend
    env: python
    buildCommand: "pip install -e ."
    startCommand: "streamlit run src/frontend/app.py --server.port=10000 --server.address=0.0.0.0"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: API_URL
        value: https://jira-ai-agent-backend.onrender.com
```

### Step 2: Deploy on Render

1. **Create account**: Go to [render.com](https://render.com) and sign up (free)
2. **Connect GitHub**: Link your GitHub repository
3. **Create Blueprint**:
   - Click "New" → "Blueprint"
   - Select your repository
   - Render will detect `render.yaml` automatically
4. **Add Environment Variables**: In dashboard, add your secrets:
   - `JIRA_URL`
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN`
   - `GROQ_API_KEY`
5. **Deploy**: Click "Apply" and wait for deployment

**URLs will be**:

- Backend: `https://jira-ai-agent-backend.onrender.com`
- Frontend: `https://jira-ai-agent-frontend.onrender.com`

---

## 2. Railway.app

**Free Tier**: $5 credit/month, enough for hobby projects

### Step 1: Create `railway.json`

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python src/backend/api.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Create `Procfile` for Streamlit

```
web: streamlit run src/frontend/app.py --server.port=$PORT --server.address=0.0.0.0
api: python src/backend/api.py
```

### Step 3: Deploy

1. **Install Railway CLI**:

   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:

   ```bash
   railway login
   railway init
   railway up
   ```

3. **Add Environment Variables**:

   ```bash
   railway variables set JIRA_URL=your_url
   railway variables set JIRA_EMAIL=your_email
   railway variables set JIRA_API_TOKEN=your_token
   railway variables set GROQ_API_KEY=your_key
   ```

4. **Generate Domain**: In Railway dashboard, click "Generate Domain"

---

## 3. Streamlit Cloud + Backend on Render

**Best for**: Separating frontend and backend

### Frontend on Streamlit Cloud (FREE)

1. **Create `.streamlit/config.toml`**:

   ```toml
   [server]
   headless = true
   port = 8501

   [theme]
   primaryColor = "#0052CC"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F4F5F7"
   textColor = "#172B4D"
   ```

2. **Create `requirements_frontend.txt`**:

   ```
   streamlit>=1.31.0
   requests>=2.31.0
   pandas>=2.2.0
   plotly>=5.18.0
   python-dotenv>=1.0.0
   ```

3. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub
   - Select repository
   - Main file: `src/frontend/app.py`
   - Advanced: Add environment variable:
     ```
     API_URL=https://your-backend.onrender.com
     ```

### Backend on Render (FREE)

Follow **Method 1** above but only deploy the backend service.

---

## 4. Hugging Face Spaces

**Free Tier**: Persistent storage, GPU access (paid)

### Step 1: Create Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select "Streamlit" SDK
4. Make it public (required for free tier)

### Step 2: Configure `README.md` in HF Space

```yaml
---
title: JIRA AI Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.31.0
app_file: src/frontend/app.py
pinned: false
---
# JIRA AI Agent

AI-powered assistant for JIRA ticket analysis and resolution.
```

### Step 3: Deploy

1. **Clone the space**:

   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/jira-ai-agent
   cd jira-ai-agent
   ```

2. **Copy your project files**:

   ```bash
   # Copy all files to the space directory
   ```

3. **Add secrets** in Space Settings:

   - `JIRA_URL`
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN`
   - `GROQ_API_KEY`

4. **Push to Space**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push
   ```

**Note**: For backend, you might need to run it separately on Render or Railway.

---

## 5. PythonAnywhere

**Free Tier**: 1 web app, limited CPU

### Setup

1. **Sign up**: [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Upload code**: Use Files tab or git clone
3. **Create virtual environment**:

   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 jira-agent
   pip install -e .
   ```

4. **Configure Web App**:

   - Web tab → Add new web app
   - Choose Flask
   - Set WSGI file:

     ```python
     import sys
     sys.path.insert(0, '/home/yourusername/jira-ai-agent')

     from src.backend.api import app as application
     ```

5. **Set environment variables**: In web app config

**Limitation**: Free tier may struggle with AI workloads.

---

## 🎯 Recommended Setup for Free Deployment

### Option A: All-in-One (Render)

```
✅ Backend API on Render (Free Web Service)
✅ Frontend on Render (Free Web Service)
📦 Uses same repository
🔄 Auto-deploy on git push
⚡ ~750 hours/month free
```

### Option B: Split Services

```
✅ Backend API on Render (Free)
✅ Frontend on Streamlit Cloud (Free - unlimited)
🎨 Better for Streamlit apps
🔐 Separate secret management
```

---

## 📝 Pre-Deployment Checklist

### 1. Update Dependencies

Ensure `pyproject.toml` has all dependencies:

```toml
[project]
dependencies = [
    "fastmcp>=0.2.0",
    "langchain>=0.3.0",
    "langchain-groq>=0.2.0",
    "langchain-community>=0.3.0",
    "langchain-core>=0.3.0",
    "flask>=3.0.0",
    "flask-cors>=4.0.0",
    "streamlit>=1.31.0",
    # ... rest
]
```

### 2. Create `.gitignore`

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
*.log
.pytest_cache/
```

### 3. Add Production Configuration

Create `config/production.yaml`:

```yaml
jira:
  timeout: 30

llm:
  temperature: 0.7
  max_tokens: 2048

flask:
  debug: false
  host: 0.0.0.0
```

### 4. Update API URL in Frontend

In `src/frontend/app.py`, ensure:

```python
API_URL = os.getenv('API_URL', 'http://localhost:5000')
```

### 5. Test Locally First

```bash
# Test backend
.venv\Scripts\python.exe src\backend\api.py

# Test frontend
.venv\Scripts\python.exe -m streamlit run src\frontend\app.py
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file**
2. **Use environment variables** for all secrets
3. **Enable HTTPS** (automatic on Render/Railway)
4. **Rate limit API** (add Flask-Limiter):

   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)

   @app.route('/api/query', methods=['POST'])
   @limiter.limit("10 per minute")
   def process_query():
       # ...
   ```

5. **Add CORS restrictions** in production:
   ```python
   CORS(app, resources={r"/api/*": {"origins": ["https://your-frontend.com"]}})
   ```

---

## 🐛 Common Deployment Issues

### Issue 1: Port Binding

**Error**: `Address already in use`

**Fix**: Use environment variable for port:

```python
port = int(os.getenv('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Issue 2: Build Timeout

**Error**: Build takes too long

**Fix**: Use `requirements.txt` instead of full install:

```bash
pip install --no-cache-dir -r requirements.txt
```

### Issue 3: Memory Limits

**Error**: Out of memory

**Fix**: Reduce model size or use smaller embedding models:

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # Smaller model
)
```

### Issue 4: Cold Starts

**Problem**: First request is slow

**Solution**: Use Render's "Always On" (paid) or keep-alive service:

```python
# Add health check endpoint
@app.route('/ping')
def ping():
    return 'pong'
```

Then use UptimeRobot (free) to ping every 5 minutes.

---

## 📊 Cost Comparison

| Platform            | Free Tier    | Limitations              | Best For        |
| ------------------- | ------------ | ------------------------ | --------------- |
| **Render**          | 750 hrs/mo   | Sleeps after 15 min idle | Full stack apps |
| **Railway**         | $5 credit/mo | Limited resources        | Quick deploys   |
| **Streamlit Cloud** | Unlimited    | Frontend only            | Streamlit apps  |
| **HF Spaces**       | Unlimited    | Public repos only        | ML demos        |
| **PythonAnywhere**  | 1 web app    | CPU limits               | Simple APIs     |

---

## 🚀 Quick Deploy Commands

### For Render:

```bash
# 1. Create render.yaml (provided above)
# 2. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 3. Connect on Render.com dashboard
# Done!
```

### For Railway:

```bash
railway login
railway init
railway up
railway open
```

### For Streamlit Cloud:

```bash
# 1. Push to GitHub
# 2. Go to share.streamlit.io
# 3. Click "New app" → Select repo → Deploy
```

---

## 🎉 Next Steps After Deployment

1. **Test all endpoints**: Use the deployed URLs
2. **Monitor logs**: Check for errors in platform dashboards
3. **Set up monitoring**: Use UptimeRobot for uptime checks
4. **Add analytics**: Track usage with Google Analytics
5. **Share your app**: Get user feedback!

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Streamlit Cloud Guide](https://docs.streamlit.io/streamlit-community-cloud)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)

---

**Need Help?** Check deployment logs for specific error messages!
