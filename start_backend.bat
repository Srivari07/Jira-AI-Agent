@echo off
REM Start Flask Backend Server

echo Starting JIRA AI Agent Backend...
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Start Flask API
python src\backend\api.py

pause
