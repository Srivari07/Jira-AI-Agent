# 🚀 Quick Deploy Guide - JIRA AI Agent

## ⚡ Fastest Way to Deploy (5 minutes)

### Option 1: Render.com (Recommended)

**Cost**: FREE (750 hours/month)

1. **Push to GitHub**:

   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Deploy**:

   - Go to [render.com](https://render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repo
   - Select repository
   - Add environment variables:
     - `JIRA_URL`
     - `JIRA_EMAIL`
     - `JIRA_API_TOKEN`
     - `GROQ_API_KEY`
   - Click "Apply"

3. **Done!** Your app will be live at:
   - Backend: `https://jira-ai-agent-backend.onrender.com`
   - Frontend: `https://jira-ai-agent-frontend.onrender.com`

---

### Option 2: Streamlit Cloud (Frontend) + Render (Backend)

**Cost**: FREE (Unlimited)

**Backend on Render**:

1. Same as Option 1, but only deploy backend service

**Frontend on Streamlit Cloud**:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect GitHub repository
4. Main file: `src/frontend/app.py`
5. Advanced Settings → Add:
   ```
   API_URL=https://your-backend.onrender.com
   ```
6. Click "Deploy"

---

### Option 3: Railway.app

**Cost**: $5 credit/month (FREE)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# Add environment variables
railway variables set JIRA_URL=your_url
railway variables set JIRA_EMAIL=your_email
railway variables set JIRA_API_TOKEN=your_token
railway variables set GROQ_API_KEY=your_key

# Generate public URL
railway domain
```

---

## 📋 Pre-Deployment Checklist

- [ ] `.env` file created with all credentials
- [ ] `.env` is in `.gitignore`
- [ ] All code committed to Git
- [ ] Pushed to GitHub
- [ ] Environment variables ready to paste
- [ ] Tested locally first

**Run this to prepare**:

```bash
deploy_prep.bat
```

---

## 🔑 Required Environment Variables

| Variable         | Description                 | Example                             |
| ---------------- | --------------------------- | ----------------------------------- |
| `JIRA_URL`       | Your JIRA instance URL      | `https://yourcompany.atlassian.net` |
| `JIRA_EMAIL`     | Your JIRA email             | `you@company.com`                   |
| `JIRA_API_TOKEN` | JIRA API token              | `ATBBxxxxx...`                      |
| `GROQ_API_KEY`   | Groq API key                | `gsk_xxxxx...`                      |
| `API_URL`        | Backend URL (frontend only) | `https://backend.onrender.com`      |

---

## 🎯 Recommended: Render.com

**Why?**

- ✅ Easy Blueprint deployment
- ✅ Free SSL certificates
- ✅ Auto-deploy on git push
- ✅ 750 free hours/month
- ✅ Custom domains
- ✅ Environment variables UI

**Limitation**: Services sleep after 15 min idle (first request takes ~30s)

**Solution**: Use [UptimeRobot](https://uptimerobot.com) (free) to ping every 5 minutes

---

## 🐛 Troubleshooting

### Port Issues

Ensure `api.py` uses environment variable:

```python
port = int(os.getenv('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Build Fails

Check deployment logs for specific error. Common fixes:

- Ensure Python 3.10+ in `render.yaml`
- Check all dependencies in `pyproject.toml`
- Verify `pip install -e .` works locally

### 503 Service Unavailable

Check environment variables are set correctly in platform dashboard.

### CORS Errors

Frontend can't reach backend - check `API_URL` environment variable.

---

## 📞 Need Help?

1. Check `DEPLOYMENT.md` for detailed guides
2. Check platform documentation:
   - [Render Docs](https://render.com/docs)
   - [Railway Docs](https://docs.railway.app)
   - [Streamlit Docs](https://docs.streamlit.io/streamlit-community-cloud)

---

## 🎉 After Deployment

1. Test all features on live URL
2. Monitor logs in platform dashboard
3. Set up uptime monitoring (UptimeRobot)
4. Share your app!

**Your app is now live! 🚀**
