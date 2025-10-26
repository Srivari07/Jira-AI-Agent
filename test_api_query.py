"""
Debug script for /api/query endpoint
Run: python test_api_query.py

This script helps debug the /api/query endpoint locally by:
1. Checking if backend is running
2. Testing health endpoint
3. Testing various query scenarios
4. Showing detailed request/response data
"""

import requests
import json
import sys
import time

# API endpoint
BASE_URL = "http://localhost:5000"
HEALTH_URL = f"{BASE_URL}/health"
QUERY_URL = f"{BASE_URL}/api/query"

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def check_backend():
    """Check if backend is running"""
    print_header("Checking Backend Status")
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        print(f"✅ Backend is running on {BASE_URL}")
        print(f"Status Code: {response.status_code}")
        print(f"Health Data: {json.dumps(response.json(), indent=2)}")
        
        health_data = response.json()
        if not health_data.get('llm_agent'):
            print("\n⚠️  WARNING: LLM Agent not initialized!")
            print("   Check GROQ_API_KEY in .env file")
        if not health_data.get('jira_client'):
            print("\n⚠️  WARNING: JIRA Client not initialized!")
            print("   Check JIRA credentials in .env file")
        
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend is NOT running!")
        print("\nTo start the backend:")
        print("  1. Open a terminal")
        print("  2. cd c:\\PythonWorkSpace\\Jira-AI-Agent")
        print("  3. .venv\\Scripts\\python.exe src\\backend\\api.py")
        print("\nWaiting for backend to start...")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_query_basic():
    """Test basic query"""
    print_header("Test 1: Basic Query")
    
    payload = {
        "query": "How to fix API authentication error?",
        "max_results": 3
    }
    
    print(f"📤 Request Payload:\n{json.dumps(payload, indent=2)}")
    print("\n⏳ Sending request...")
    
    try:
        start_time = time.time()
        response = requests.post(QUERY_URL, json=payload, timeout=60)
        elapsed = time.time() - start_time
        
        print(f"\n✅ Response received in {elapsed:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📥 Response Summary:")
            print(f"   - Query: {data.get('query')}")
            print(f"   - Analysis: {data.get('analysis', 'N/A')[:100]}...")
            print(f"   - Matched Tickets: {len(data.get('matched_tickets', []))}")
            print(f"   - Total Historical: {data.get('total_historical_tickets')}")
            print(f"   - Resolution Length: {len(data.get('resolution', ''))} chars")
            
            if data.get('matched_tickets'):
                print(f"\n📋 Top Matched Tickets:")
                for i, ticket in enumerate(data['matched_tickets'][:3], 1):
                    print(f"   {i}. {ticket.get('key')} - {ticket.get('summary', 'N/A')[:60]}")
                    print(f"      Similarity: {ticket.get('similarity_score', 'N/A')}")
        else:
            print(f"\n❌ Error Response:\n{json.dumps(response.json(), indent=2)}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (60s)")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_query_with_projects():
    """Test query with project filter"""
    print_header("Test 2: Query with Project Filter")
    
    payload = {
        "query": "Database connection timeout",
        "projects": ["PROD", "TECH"],
        "max_results": 5
    }
    
    print(f"📤 Request Payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(QUERY_URL, json=payload, timeout=60)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data.get('matched_tickets', []))} matched tickets")
            print(f"   Total historical: {data.get('total_historical_tickets')}")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_query_missing_param():
    """Test with missing query parameter"""
    print_header("Test 3: Missing Query Parameter (Should Return 400)")
    
    payload = {
        "max_results": 3
    }
    
    print(f"📤 Request Payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(QUERY_URL, json=payload, timeout=10)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 400:
            print(f"✅ Correctly returned 400: {response.json()}")
        else:
            print(f"⚠️  Expected 400, got {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_query_verbose():
    """Test with detailed output"""
    print_header("Test 4: Detailed Debug Test")
    
    payload = {
        "query": "User login failure",
        "max_results": 2
    }
    
    print(f"📤 Request Payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(QUERY_URL, json=payload, timeout=60)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"\n📥 Full Response:\n{json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Error Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main debug function"""
    print("\n" + "🔍" * 35)
    print("  JIRA AI Agent - /api/query Debug Tool")
    print("🔍" * 35)
    
    # Check if backend is running
    max_retries = 3
    for attempt in range(max_retries):
        if check_backend():
            break
        if attempt < max_retries - 1:
            print(f"\nRetry {attempt + 1}/{max_retries - 1}...")
            time.sleep(2)
    else:
        print("\n❌ Cannot proceed without backend running.")
        print("\nDebug checklist:")
        print("  1. Is Python virtual environment activated?")
        print("  2. Are dependencies installed? (uv pip install -e .)")
        print("  3. Is .env file configured with valid credentials?")
        print("  4. Is backend running? (.venv\\Scripts\\python.exe src\\backend\\api.py)")
        sys.exit(1)
    
    # Run tests
    test_query_basic()
    
    input("\nPress Enter to continue to next test...")
    test_query_with_projects()
    
    input("\nPress Enter to continue to next test...")
    test_query_missing_param()
    
    input("\nPress Enter to see detailed debug output...")
    test_query_verbose()
    
    print_header("Debug Session Complete")
    print("\n💡 Tips:")
    print("  - Check terminal running api.py for detailed logs")
    print("  - Logs show each step: analyze → fetch → match → generate")
    print("  - Look for ERROR or WARNING messages in backend logs")
    print("  - Verify JIRA credentials if no tickets are found")
    print("  - Check GROQ_API_KEY if LLM operations fail")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Debug session cancelled by user")
        sys.exit(0)
