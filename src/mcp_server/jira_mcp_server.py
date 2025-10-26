"""
JIRA MCP Server - FastMCP server for JIRA integration
Provides tools to fetch and analyze historical JIRA tickets
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import os
from jira import JIRA
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import yaml

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("JIRA AI Agent MCP Server")


class JiraClient:
    """JIRA client wrapper for ticket operations"""
    
    def __init__(self):
        self.jira_url = os.getenv("JIRA_URL")
        self.jira_email = os.getenv("JIRA_EMAIL")
        self.jira_token = os.getenv("JIRA_API_TOKEN")
        
        if not all([self.jira_url, self.jira_email, self.jira_token]):
            raise ValueError("JIRA credentials not configured. Check .env file.")
        
        # Assert types for type checker after validation
        assert self.jira_email is not None
        assert self.jira_token is not None
        
        self.client = JIRA(
            server=self.jira_url,
            basic_auth=(self.jira_email, self.jira_token)
        )
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), "../../config/config.yaml")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def search_tickets(
        self, 
        projects: Optional[List[str]] = None,
        issue_types: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
        max_results: int = 100,
        days_back: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search for JIRA tickets based on criteria"""
        
        # Build JQL query
        jql_parts = []
        
        if projects:
            project_filter = " OR ".join([f"project = {p}" for p in projects])
            jql_parts.append(f"({project_filter})")
        
        if issue_types:
            type_filter = " OR ".join([f"issuetype = '{t}'" for t in issue_types])
            jql_parts.append(f"({type_filter})")
        
        if statuses:
            status_filter = " OR ".join([f"status = '{s}'" for s in statuses])
            jql_parts.append(f"({status_filter})")
        
        if days_back:
            date_threshold = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            jql_parts.append(f"updated >= '{date_threshold}'")
        
        jql = " AND ".join(jql_parts) if jql_parts else "project is not EMPTY"
        jql += " ORDER BY updated DESC"
        
        # Execute search
        issues = self.client.search_issues(
            jql,
            maxResults=max_results,
            fields=self.config['jira']['fields']
        )
        
        # Format results
        tickets = []
        for issue in issues:
            ticket = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": getattr(issue.fields, 'description', ''),
                "status": issue.fields.status.name,
                "resolution": issue.fields.resolution.name if issue.fields.resolution else None,
                "created": str(issue.fields.created),
                "updated": str(issue.fields.updated),
                "priority": issue.fields.priority.name if issue.fields.priority else None,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
                "labels": issue.fields.labels,
                "url": f"{self.jira_url}/browse/{issue.key}"
            }
            
            # Get comments
            comments = []
            if hasattr(issue.fields, 'comment') and issue.fields.comment.comments:
                for comment in issue.fields.comment.comments:
                    comments.append({
                        "author": comment.author.displayName,
                        "body": comment.body,
                        "created": str(comment.created)
                    })
            ticket["comments"] = comments
            
            tickets.append(ticket)
        
        return tickets
    
    def get_ticket_by_key(self, key: str) -> Dict[str, Any]:
        """Get a specific ticket by its key"""
        try:
            issue = self.client.issue(key, fields=self.config['jira']['fields'])
            
            ticket = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": getattr(issue.fields, 'description', ''),
                "status": issue.fields.status.name,
                "resolution": issue.fields.resolution.name if issue.fields.resolution else None,
                "created": str(issue.fields.created),
                "updated": str(issue.fields.updated),
                "priority": issue.fields.priority.name if issue.fields.priority else None,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
                "labels": issue.fields.labels,
                "url": f"{self.jira_url}/browse/{issue.key}"
            }
            
            # Get comments
            comments = []
            if hasattr(issue.fields, 'comment') and issue.fields.comment.comments:
                for comment in issue.fields.comment.comments:
                    comments.append({
                        "author": comment.author.displayName,
                        "body": comment.body,
                        "created": str(comment.created)
                    })
            ticket["comments"] = comments
            
            return ticket
        except Exception as e:
            return {"error": f"Failed to fetch ticket {key}: {str(e)}"}


# Initialize JIRA client
jira_client = JiraClient()


@mcp.tool()
def search_historical_tickets(
    query: str,
    projects: Optional[List[str]] = None,
    max_results: int = 50,
    days_back: int = 90
) -> List[Dict[str, Any]]:
    """
    Search for historical JIRA tickets based on query text.
    
    Args:
        query: Search query text
        projects: List of JIRA project keys (e.g., ['PROD', 'TECH'])
        max_results: Maximum number of results to return
        days_back: Number of days to look back
    
    Returns:
        List of matching JIRA tickets with details
    """
    if not projects:
        projects = jira_client.config['jira']['projects']
    
    statuses = jira_client.config['jira']['resolved_statuses']
    
    tickets = jira_client.search_tickets(
        projects=projects,
        statuses=statuses,
        max_results=max_results,
        days_back=days_back
    )
    
    return tickets


@mcp.tool()
def get_ticket_details(ticket_key: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific JIRA ticket.
    
    Args:
        ticket_key: JIRA ticket key (e.g., 'PROD-123')
    
    Returns:
        Detailed ticket information including comments
    """
    return jira_client.get_ticket_by_key(ticket_key)


@mcp.tool()
def get_recent_resolved_tickets(
    projects: Optional[List[str]] = None,
    max_results: int = 30,
    days_back: int = 30
) -> List[Dict[str, Any]]:
    """
    Get recently resolved tickets for analysis.
    
    Args:
        projects: List of JIRA project keys
        max_results: Maximum number of results
        days_back: Number of days to look back
    
    Returns:
        List of recently resolved tickets
    """
    if not projects:
        projects = jira_client.config['jira']['projects']
    
    statuses = jira_client.config['jira']['resolved_statuses']
    
    tickets = jira_client.search_tickets(
        projects=projects,
        statuses=statuses,
        max_results=max_results,
        days_back=days_back
    )
    
    return tickets


@mcp.tool()
def get_ticket_statistics(
    projects: Optional[List[str]] = None,
    days_back: int = 30
) -> Dict[str, Any]:
    """
    Get statistics about JIRA tickets for analytics.
    
    Args:
        projects: List of JIRA project keys
        days_back: Number of days to analyze
    
    Returns:
        Statistics about tickets (counts, trends, etc.)
    """
    if not projects:
        projects = jira_client.config['jira']['projects']
    
    tickets = jira_client.search_tickets(
        projects=projects,
        max_results=1000,
        days_back=days_back
    )
    
    stats = {
        "total_tickets": len(tickets),
        "by_status": {},
        "by_priority": {},
        "by_project": {},
        "by_type": {},
        "resolution_rate": 0
    }
    
    resolved_count = 0
    
    for ticket in tickets:
        # Count by status
        status = ticket.get("status", "Unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        # Count by priority
        priority = ticket.get("priority", "Unknown")
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
        
        # Count by project
        project = ticket["key"].split("-")[0]
        stats["by_project"][project] = stats["by_project"].get(project, 0) + 1
        
        # Count resolved
        if ticket.get("resolution"):
            resolved_count += 1
    
    if stats["total_tickets"] > 0:
        stats["resolution_rate"] = round(resolved_count / stats["total_tickets"] * 100, 2)
    
    return stats


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
