"""
Flask Backend API for JIRA AI Agent
Provides REST endpoints for query processing and ticket matching
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.llm_agent import JiraLLMAgent
from mcp_server.jira_mcp_server import JiraClient

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
try:
    llm_agent = JiraLLMAgent()
    jira_client = JiraClient()
except Exception as e:
    print(f"Error initializing components: {e}")
    llm_agent = None
    jira_client = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "llm_agent": llm_agent is not None,
        "jira_client": jira_client is not None
    })


@app.route('/api/query', methods=['POST'])
def process_query():
    """
    Process user query and return matched tickets with resolutions
    
    Request body:
    {
        "query": "user question or problem description",
        "projects": ["PROD", "TECH"],  # optional
        "max_results": 5  # optional
    }
    """
    # logger.info("=== /api/query endpoint called ===")
    
    if llm_agent is None or jira_client is None:
        #logger.error("Components not initialized - llm_agent: %s, jira_client: %s", 
        #            llm_agent is not None, jira_client is not None)
        return jsonify({"error": "Service unavailable. Components not initialized."}), 503
    
    try:
        data = request.get_json()
        #logger.debug("Request data: %s", data)
        
        query = data.get('query')
        projects = data.get('projects')
        max_results = data.get('max_results', 5)
        
        if not query:
            #logger.warning("Query parameter missing")
            return jsonify({"error": "Query is required"}), 400

        #logger.info("Processing query: '%s'", query)

        # Step 1: Analyze query
        #logger.debug("Step 1: Analyzing query...")
        query_analysis = llm_agent.analyze_query(query)
        #logger.debug("Query analysis result: %s", query_analysis)

        # Step 2: Fetch historical tickets
        #logger.debug("Step 2: Fetching historical tickets (projects=%s, max_results=100, days_back=90)...", projects)
        historical_tickets = jira_client.search_tickets(
            projects=projects,
            max_results=100,
            days_back=90
        )
        #logger.info("Found %d historical tickets", len(historical_tickets))
        
        # Step 3: Match tickets with query
        #logger.debug("Step 3: Matching tickets (top_k=%d)...", max_results)
        matched_tickets = llm_agent.match_tickets(
            query=query,
            historical_tickets=historical_tickets,
            top_k=max_results
        )
        #logger.info("Matched %d tickets", len(matched_tickets))
        
        # Step 4: Generate resolution
        #logger.debug("Step 4: Generating resolution...")
        resolution = ""
        if matched_tickets:
            resolution = llm_agent.generate_resolution(query, matched_tickets)
            #logger.debug("Resolution generated (length: %d chars)", len(resolution))
        else:
            #logger.warning("No matched tickets - skipping resolution generation")
            resolution = "No relevant tickets found."

        response_data = {
            "query": query,
            "analysis": query_analysis,
            "matched_tickets": matched_tickets,
            "resolution": resolution,
            "total_historical_tickets": len(historical_tickets)
        }
        #logger.info("Successfully processed query - returning %d matched tickets", len(matched_tickets))
        return jsonify(response_data)
    
    except Exception as e:
        #logger.exception("Error processing query: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/tickets/search', methods=['POST'])
def search_tickets():
    """
    Search JIRA tickets with filters
    
    Request body:
    {
        "projects": ["PROD", "TECH"],  # optional
        "statuses": ["Done", "Resolved"],  # optional
        "days_back": 30,  # optional
        "max_results": 50  # optional
    }
    """
    if jira_client is None:
        return jsonify({"error": "Service unavailable. JIRA client not initialized."}), 503
    
    try:
        data = request.get_json()
        
        tickets = jira_client.search_tickets(
            projects=data.get('projects'),
            statuses=data.get('statuses'),
            max_results=data.get('max_results', 50),
            days_back=data.get('days_back', 30)
        )
        
        return jsonify({
            "tickets": tickets,
            "count": len(tickets)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/tickets/<ticket_key>', methods=['GET'])
def get_ticket(ticket_key: str):
    """Get detailed information about a specific ticket"""
    if jira_client is None:
        return jsonify({"error": "Service unavailable. JIRA client not initialized."}), 503
    
    try:
        ticket = jira_client.get_ticket_by_key(ticket_key)
        
        if "error" in ticket:
            return jsonify(ticket), 404
        
        return jsonify(ticket)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analytics/statistics', methods=['POST'])
def get_statistics():
    """
    Get ticket statistics for analytics
    
    Request body:
    {
        "projects": ["PROD", "TECH"],  # optional
        "days_back": 30  # optional
    }
    """
    if jira_client is None:
        return jsonify({"error": "Service unavailable. JIRA client not initialized."}), 503
    
    try:
        data = request.get_json() or {}
        
        stats = jira_client.search_tickets(
            projects=data.get('projects'),
            max_results=1000,
            days_back=data.get('days_back', 30)
        )
        
        # Calculate statistics
        statistics = {
            "total_tickets": len(stats),
            "by_status": {},
            "by_priority": {},
            "by_project": {}
        }
        
        for ticket in stats:
            # Count by status
            status = ticket.get("status", "Unknown")
            statistics["by_status"][status] = statistics["by_status"].get(status, 0) + 1
            
            # Count by priority
            priority = ticket.get("priority", "Unknown")
            statistics["by_priority"][priority] = statistics["by_priority"].get(priority, 0) + 1
            
            # Count by project
            project = ticket["key"].split("-")[0]
            statistics["by_project"][project] = statistics["by_project"].get(project, 0) + 1
        
        return jsonify(statistics)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/insights', methods=['POST'])
def get_insights():
    """
    Extract insights from historical tickets
    
    Request body:
    {
        "projects": ["PROD", "TECH"],  # optional
        "days_back": 30  # optional
    }
    """
    if llm_agent is None or jira_client is None:
        return jsonify({"error": "Service unavailable. Components not initialized."}), 503
    
    try:
        data = request.get_json() or {}
        
        # Fetch tickets
        tickets = jira_client.search_tickets(
            projects=data.get('projects'),
            max_results=100,
            days_back=data.get('days_back', 30)
        )
        
        # Extract insights using LLM
        insights = llm_agent.extract_key_insights(tickets)
        
        return jsonify({
            "insights": insights,
            "analyzed_tickets": len(tickets)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
