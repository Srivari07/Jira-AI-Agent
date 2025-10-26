@echo off
REM Quick Deployment Preparation Script for Windows

echo ================================
echo JIRA AI Agent - Deployment Prep
echo ================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please create .env file with your credentials first.
    echo Copy .env.example to .env and fill in your values.
    pause
    exit /b 1
)

echo [1/5] Checking environment file...
echo ✓ .env file found

echo.
echo [2/5] Checking Git repository...
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo [INFO] Initializing Git repository...
    git init
    echo ✓ Git initialized
) else (
    echo ✓ Git repository exists
)

echo.
echo [3/5] Checking .gitignore...
if not exist .gitignore (
    echo [WARN] .gitignore not found
) else (
    findstr /C:".env" .gitignore >nul
    if errorlevel 1 (
        echo [WARN] .env not in .gitignore!
        echo .env >> .gitignore
        echo ✓ Added .env to .gitignore
    ) else (
        echo ✓ .env is properly ignored
    )
)

echo.
echo [4/5] Checking deployment files...
if exist render.yaml (echo ✓ render.yaml found) else (echo [WARN] render.yaml not found)
if exist Procfile (echo ✓ Procfile found) else (echo [WARN] Procfile not found)
if exist railway.json (echo ✓ railway.json found) else (echo [WARN] railway.json not found)

echo.
echo [5/5] Testing local setup...
echo Testing if virtual environment is activated...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
) else (
    python --version
    echo ✓ Python is available
)

echo.
echo ================================
echo Deployment Prep Complete! ✓
echo ================================
echo.
echo NEXT STEPS:
echo.
echo Choose your deployment platform:
echo.
echo 1. RENDER.COM (Recommended)
echo    - Go to https://render.com
echo    - Sign up / Log in
echo    - Click "New" ^> "Blueprint"
echo    - Connect your GitHub repository
echo    - Add environment variables in dashboard
echo    - Click "Apply"
echo.
echo 2. RAILWAY.APP
echo    - Install: npm install -g @railway/cli
echo    - Run: railway login
echo    - Run: railway init
echo    - Run: railway up
echo    - Add env vars: railway variables set KEY=value
echo.
echo 3. STREAMLIT CLOUD (Frontend only)
echo    - Go to https://share.streamlit.io
echo    - Connect GitHub
echo    - Select repo and src/frontend/app.py
echo    - Add API_URL in settings
echo.
echo IMPORTANT:
echo - Do NOT commit .env file!
echo - Add secrets via platform dashboard
echo - Update API_URL in frontend after backend deploys
echo.
echo Ready to commit? Run:
echo   git add .
echo   git commit -m "Ready for deployment"
echo   git push
echo.
pause
