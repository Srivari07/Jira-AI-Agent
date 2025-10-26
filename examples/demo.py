"""
Example usage of JIRA AI Agent
Demonstrates API calls and basic functionality
"""

import requests
import json

# Configuration
API_URL = "http://localhost:5000"

def test_health():
    """Test API health"""
    print("\n🏥 Testing API Health...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def example_query():
    """Example: Process a technical query"""
    print("\n🔍 Example: Processing Technical Query...")
    
    query = "How do I fix authentication errors in the API?"
    
    payload = {
        "query": query,
        "projects": ["PROD", "TECH"],
        "max_results": 3
    }
    
    print(f"Query: {query}")
    print("Sending request...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/query",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n📋 Query Analysis:")
            analysis = data.get("analysis", {})
            print(f"  - Issue Type: {analysis.get('issue_type')}")
            print(f"  - Priority: {analysis.get('priority')}")
            print(f"  - Key Terms: {', '.join(analysis.get('key_terms', []))}")
            
            print(f"\n🎯 Found {len(data.get('matched_tickets', []))} matching tickets:")
            for i, match in enumerate(data.get("matched_tickets", []), 1):
                ticket = match.get("ticket_data", {})
                print(f"\n  {i}. [{ticket.get('key')}] {ticket.get('summary')}")
                print(f"     Relevance: {match.get('relevance_score')}/10")
                print(f"     Reasoning: {match.get('reasoning')}")
            
            print("\n💡 AI-Generated Resolution:")
            resolution = data.get("resolution", "")
            print(f"  {resolution[:300]}...")
        else:
            print(f"❌ Error: {response.json().get('error')}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running:")
        print("   python main.py backend")
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out. The query may be complex.")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_search_tickets():
    """Example: Search for tickets"""
    print("\n🎫 Example: Searching Tickets...")
    
    payload = {
        "projects": ["PROD"],
        "statuses": ["Done", "Resolved"],
        "days_back": 30,
        "max_results": 10
    }
    
    print(f"Searching for tickets in last 30 days...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/tickets/search",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            tickets = data.get("tickets", [])
            
            print(f"\n✅ Found {len(tickets)} tickets")
            
            for ticket in tickets[:5]:  # Show first 5
                print(f"\n  [{ticket.get('key')}] {ticket.get('summary')}")
                print(f"    Status: {ticket.get('status')} | Priority: {ticket.get('priority')}")
                print(f"    Updated: {ticket.get('updated', '')[:10]}")
        else:
            print(f"❌ Error: {response.json().get('error')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_statistics():
    """Example: Get ticket statistics"""
    print("\n📊 Example: Getting Statistics...")
    
    payload = {
        "projects": ["PROD", "TECH"],
        "days_back": 30
    }
    
    print("Analyzing tickets from last 30 days...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/analytics/statistics",
            json=payload
        )
        
        if response.status_code == 200:
            stats = response.json()
            
            print(f"\n✅ Statistics:")
            print(f"  Total Tickets: {stats.get('total_tickets')}")
            
            print(f"\n  By Status:")
            for status, count in stats.get("by_status", {}).items():
                print(f"    - {status}: {count}")
            
            print(f"\n  By Priority:")
            for priority, count in stats.get("by_priority", {}).items():
                print(f"    - {priority}: {count}")
            
            print(f"\n  By Project:")
            for project, count in stats.get("by_project", {}).items():
                print(f"    - {project}: {count}")
        else:
            print(f"❌ Error: {response.json().get('error')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_insights():
    """Example: Get AI insights"""
    print("\n💡 Example: Getting AI Insights...")
    
    payload = {
        "projects": ["PROD", "TECH"],
        "days_back": 30
    }
    
    print("Extracting insights from historical tickets...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/insights",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            insights = data.get("insights", {})
            
            print(f"\n✅ Analyzed {data.get('analyzed_tickets')} tickets")
            
            print(f"\n  Common Issues:")
            for issue in insights.get("common_issues", [])[:5]:
                print(f"    - {issue}")
            
            print(f"\n  Common Resolutions:")
            for resolution in insights.get("common_resolutions", [])[:5]:
                print(f"    - {resolution}")
            
            print(f"\n  Recommendations:")
            for rec in insights.get("recommendations", []):
                print(f"    - {rec}")
        else:
            print(f"❌ Error: {response.json().get('error')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all examples"""
    print("=" * 60)
    print("🤖 JIRA AI Agent - Usage Examples")
    print("=" * 60)
    
    # Check if API is running
    try:
        test_health()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("\nPlease start the backend server first:")
        print("  python main.py backend")
        print("\nOr use the batch file:")
        print("  start_backend.bat")
        return
    
    # Run examples
    examples = [
        ("Query Processing", example_query),
        ("Ticket Search", example_search_tickets),
        ("Statistics", example_get_statistics),
        ("AI Insights", example_get_insights)
    ]
    
    print("\n" + "=" * 60)
    print("Available Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  0. Run all examples")
    print("=" * 60)
    
    choice = input("\nSelect an example (0-4): ").strip()
    
    if choice == "0":
        for name, func in examples:
            func()
            input("\nPress Enter to continue...")
    elif choice in ["1", "2", "3", "4"]:
        idx = int(choice) - 1
        examples[idx][1]()
    else:
        print("Invalid choice")
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("\nNext steps:")
    print("  - Open http://localhost:8501 for the Streamlit UI")
    print("  - Read README.md for full documentation")
    print("  - Check MCP_SETUP.md for editor integration")
    print("=" * 60)

if __name__ == "__main__":
    main()
