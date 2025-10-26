"""
Standalone debug script for process_query function
This runs the query processing logic outside of Flask for easier debugging

Usage:
    python debug_process_query.py
"""

import os
import sys
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Load environment
load_dotenv()

def debug_process_query(query: str, projects: Optional[List[str]] = None, max_results: int = 5):
    """
    Debug version of process_query function with detailed logging and breakpoints
    """
    logger.info("=" * 70)
    logger.info("DEBUG: Starting process_query")
    logger.info("=" * 70)
    
    # Import components
    logger.info("Step 0: Importing components...")
    try:
        from backend.llm_agent import JiraLLMAgent
        from mcp_server.jira_mcp_server import JiraClient
        logger.info("✅ Imports successful")
    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        return
    
    # Initialize components
    logger.info("\nStep 0.1: Initializing LLM Agent...")
    try:
        llm_agent = JiraLLMAgent()
        logger.info("✅ LLM Agent initialized")
    except Exception as e:
        logger.error(f"❌ LLM Agent initialization failed: {e}")
        logger.exception("Full traceback:")
        return
    
    logger.info("\nStep 0.2: Initializing JIRA Client...")
    try:
        jira_client = JiraClient()
        logger.info("✅ JIRA Client initialized")
    except Exception as e:
        logger.error(f"❌ JIRA Client initialization failed: {e}")
        logger.exception("Full traceback:")
        return
    
    # Process query
    logger.info("\n" + "=" * 70)
    logger.info(f"Processing Query: '{query}'")
    logger.info(f"Projects: {projects}")
    logger.info(f"Max Results: {max_results}")
    logger.info("=" * 70)
    
    try:
        # Step 1: Analyze query
        logger.info("\n📍 STEP 1: Analyzing query with LLM...")
        logger.info(f"   Input: {query}")
        
        query_analysis = llm_agent.analyze_query(query)
        
        logger.info(f"   Output: {query_analysis}")
        logger.info("   ✅ Query analysis complete")
        
        # Breakpoint 1 - Uncomment to pause here
        # import pdb; pdb.set_trace()
        
        # Step 2: Fetch historical tickets
        logger.info("\n📍 STEP 2: Fetching historical tickets from JIRA...")
        logger.info(f"   Parameters:")
        logger.info(f"     - projects: {projects}")
        logger.info(f"     - max_results: 100")
        logger.info(f"     - days_back: 90")
        
        historical_tickets = jira_client.search_tickets(
            projects=projects,
            max_results=100,
            days_back=90
        )
        
        logger.info(f"   Found {len(historical_tickets)} historical tickets")
        if historical_tickets:
            logger.info(f"   Sample ticket keys: {[t.get('key') for t in historical_tickets[:5]]}")
        logger.info("   ✅ Historical tickets fetched")
        
        # Breakpoint 2 - Uncomment to pause here
        # import pdb; pdb.set_trace()
        
        # Step 3: Match tickets with query
        logger.info("\n📍 STEP 3: Matching tickets with query...")
        logger.info(f"   Input tickets: {len(historical_tickets)}")
        logger.info(f"   Top K: {max_results}")
        
        matched_tickets = llm_agent.match_tickets(
            query=query,
            historical_tickets=historical_tickets,
            top_k=max_results
        )
        
        logger.info(f"   Matched {len(matched_tickets)} tickets")
        if matched_tickets:
            logger.info(f"   Top matches:")
            for i, ticket in enumerate(matched_tickets, 1):
                logger.info(f"     {i}. {ticket.get('key')} - Score: {ticket.get('similarity_score', 'N/A')}")
                logger.info(f"        Summary: {ticket.get('summary', 'N/A')[:60]}...")
        logger.info("   ✅ Ticket matching complete")
        
        # Breakpoint 3 - Uncomment to pause here
        # import pdb; pdb.set_trace()
        
        # Step 4: Generate resolution
        logger.info("\n📍 STEP 4: Generating resolution...")
        resolution = ""
        
        if matched_tickets:
            logger.info(f"   Generating resolution for {len(matched_tickets)} matched tickets...")
            resolution = llm_agent.generate_resolution(query, matched_tickets)
            logger.info(f"   Resolution generated ({len(resolution)} characters)")
            logger.info(f"   Preview: {resolution[:200]}...")
        else:
            logger.warning("   No matched tickets - skipping resolution generation")
        
        logger.info("   ✅ Resolution generation complete")
        
        # Breakpoint 4 - Uncomment to pause here
        # import pdb; pdb.set_trace()
        
        # Final results
        logger.info("\n" + "=" * 70)
        logger.info("FINAL RESULTS")
        logger.info("=" * 70)
        logger.info(f"✅ Query: {query}")
        logger.info(f"✅ Analysis: {query_analysis}")
        logger.info(f"✅ Total Historical Tickets: {len(historical_tickets)}")
        logger.info(f"✅ Matched Tickets: {len(matched_tickets)}")
        logger.info(f"✅ Resolution Length: {len(resolution)} chars")
        
        # Print full resolution
        logger.info("\n" + "-" * 70)
        logger.info("FULL RESOLUTION:")
        logger.info("-" * 70)
        print(resolution)
        logger.info("-" * 70)
        
        # Return result
        result = {
            "query": query,
            "analysis": query_analysis,
            "matched_tickets": matched_tickets,
            "resolution": resolution,
            "total_historical_tickets": len(historical_tickets)
        }
        
        return result
        
    except Exception as e:
        logger.error(f"\n❌ ERROR during processing: {e}")
        logger.exception("Full traceback:")
        raise


def main():
    """Main function with multiple test scenarios"""
    
    print("\n" + "🔍" * 35)
    print("  Process Query Debug Tool")
    print("🔍" * 35 + "\n")
    
    # Test scenarios
    test_cases = [
        {
            "name": "Test 1: Basic Authentication Query",
            "query": "How to fix API authentication error?",
            "projects": None,
            "max_results": 3
        },
        {
            "name": "Test 2: Database Query with Projects",
            "query": "Database connection timeout issue",
            "projects": ["PROD", "TECH"],
            "max_results": 5
        },
        {
            "name": "Test 3: Simple Query",
            "query": "User login failure",
            "projects": None,
            "max_results": 2
        }
    ]
    
    # Let user select test case
    print("Available test cases:")
    for i, test in enumerate(test_cases, 1):
        print(f"  {i}. {test['name']}")
        print(f"     Query: \"{test['query']}\"")
        print(f"     Projects: {test['projects']}, Max Results: {test['max_results']}")
    
    print(f"  {len(test_cases) + 1}. Custom query (manual input)")
    print()
    
    try:
        choice = input(f"Select test case (1-{len(test_cases) + 1}): ").strip()
        choice_idx = int(choice) - 1
        
        if choice_idx == len(test_cases):
            # Custom query
            query = input("Enter query: ").strip()
            projects_input = input("Enter projects (comma-separated, or leave blank): ").strip()
            projects = [p.strip() for p in projects_input.split(",")] if projects_input else None
            max_results = int(input("Enter max results (default 5): ").strip() or "5")
            
            debug_process_query(query, projects, max_results)
        elif 0 <= choice_idx < len(test_cases):
            # Pre-defined test case
            test = test_cases[choice_idx]
            print(f"\n🚀 Running: {test['name']}\n")
            debug_process_query(test['query'], test['projects'], test['max_results'])
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n👋 Debug cancelled by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.exception("Full traceback:")


if __name__ == "__main__":
    main()
