@echo off
REM Start Streamlit Frontend

echo Starting JIRA AI Agent Frontend...
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Start Streamlit
streamlit run src\frontend\app.py

pause
