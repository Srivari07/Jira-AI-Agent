"""
JIRA AI Agent - Main Entry Point
Provides CLI interface to start different components
"""

import sys
import os
import subprocess
from argparse import ArgumentParser

def start_backend():
    """Start Flask Backend API"""
    print("🚀 Starting Flask Backend API...")
    subprocess.run([sys.executable, "src/backend/api.py"])

def start_frontend():
    """Start Streamlit Frontend"""
    print("🎨 Starting Streamlit Frontend...")
    subprocess.run(["streamlit", "run", "src/frontend/app.py"])

def start_mcp():
    """Start MCP Server"""
    print("🔌 Starting JIRA MCP Server...")
    subprocess.run([sys.executable, "src/mcp_server/jira_mcp_server.py"])

def main():
    parser = ArgumentParser(description="JIRA AI Agent")
    parser.add_argument(
        "component",
        choices=["backend", "frontend", "mcp", "all"],
        help="Component to start"
    )
    
    args = parser.parse_args()
    
    if args.component == "backend":
        start_backend()
    elif args.component == "frontend":
        start_frontend()
    elif args.component == "mcp":
        start_mcp()
    elif args.component == "all":
        print("⚠️  To start all components, run them in separate terminals:")
        print("   Terminal 1: python main.py backend")
        print("   Terminal 2: python main.py frontend")
        print("   Terminal 3: python main.py mcp (optional)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
