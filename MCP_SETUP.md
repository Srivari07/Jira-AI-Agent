# MCP Server Configuration for VS Code / Cursor

To use the JIRA MCP Server with VS Code Copilot or Cursor:

## Setup

1. Make sure you have installed all dependencies:
```bash
pip install -e .
```

2. Configure your `.env` file with JIRA credentials:
```
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token
```

## VS Code Configuration

Add to your VS Code settings (`.vscode/settings.json` or user settings):

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "Use JIRA MCP tools to fetch and analyze historical tickets"
    }
  ]
}
```

## Cursor Configuration

Add to your Cursor MCP configuration (`~/.cursor/mcp.json` or workspace config):

```json
{
  "mcpServers": {
    "jira-ai-agent": {
      "command": "python",
      "args": ["c:/PythonWorkSpace/Jira-AI-Agent/src/mcp_server/jira_mcp_server.py"],
      "env": {
        "JIRA_URL": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "your-email@example.com",
        "JIRA_API_TOKEN": "your_api_token"
      }
    }
  }
}
```

## Available MCP Tools

1. **search_historical_tickets** - Search for historical JIRA tickets
2. **get_ticket_details** - Get detailed information about a specific ticket
3. **get_recent_resolved_tickets** - Get recently resolved tickets
4. **get_ticket_statistics** - Get ticket statistics for analytics

## Usage in Copilot Chat

Example prompts:
- "Search for tickets related to authentication errors"
- "Get details of ticket PROD-123"
- "Show me statistics for the last 30 days"
- "Find similar tickets to: API returning 500 errors"
