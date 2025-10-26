@echo off
REM Start MCP Server

echo Starting JIRA MCP Server...
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Start MCP Server
python src\mcp_server\jira_mcp_server.py

pause
