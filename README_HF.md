---
title: JIRA AI Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.31.0
app_file: src/frontend/app.py
pinned: false
license: mit
---

# JIRA AI Agent 🤖

AI-powered assistant that resolves Product and Technical Queries by analyzing historical JIRA tickets using Groq's Llama LLM.

## Features

- 🔍 Intelligent query analysis
- 🎯 Smart ticket matching using embeddings
- 💡 AI-generated resolutions based on historical data
- 📊 Analytics dashboard
- 🎫 Ticket search and browsing

## Setup

This app requires environment variables:

- `JIRA_URL`: Your JIRA instance URL
- `JIRA_EMAIL`: Your JIRA email
- `JIRA_API_TOKEN`: Your JIRA API token
- `GROQ_API_KEY`: Your Groq API key
- `API_URL`: Backend API URL

Set these in the Space Settings → Repository secrets.

## Tech Stack

- **LLM**: Groq's Llama 3.1-70b
- **Embeddings**: Sentence Transformers
- **Backend**: Flask + FastMCP
- **Frontend**: Streamlit
- **Integration**: JIRA REST API

---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
