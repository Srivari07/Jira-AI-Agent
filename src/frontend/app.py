"""
Streamlit Frontend for JIRA AI Agent
Interactive UI for query processing and analytics
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.getenv('API_URL', 'http://localhost:5000')

# Page configuration
st.set_page_config(
    page_title="JIRA AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #0052CC;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #6B778C;
        text-align: center;
        padding-bottom: 2rem;
    }
    .ticket-card {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #0052CC;
        color: #172B4D;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .resolution-box {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #36B37E;
        margin: 1rem 0;
        color: #172B4D;
        line-height: 1.6;
        font-size: 1rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">🤖 JIRA AI Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Resolve Product & Technical Queries with AI-Powered Analysis</div>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.freepnglogos.com/uploads/virus-png/virus-icon-infectious-agent-viral-vector-graphic-7.png", width=80)
        st.title("Navigation")
        
        page = st.radio(
            "Select a page",
            ["Query Assistant", "Ticket Search", "Analytics Dashboard", "Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Project filter
        st.subheader("🎯 Project Filters")
        projects = st.multiselect(
            "Select Projects",
            ["PROD", "TECH", "SUP", "DEV"],
            default=["PROD", "TECH"]
        )
        
        st.divider()
        
        # Quick stats
        st.subheader("📊 Quick Stats")
        if st.button("🔄 Refresh Stats"):
            display_quick_stats()
    
    # Main content based on selected page
    if page == "Query Assistant":
        query_assistant_page(projects)
    elif page == "Ticket Search":
        ticket_search_page(projects)
    elif page == "Analytics Dashboard":
        analytics_dashboard_page(projects)
    elif page == "Settings":
        settings_page()


def query_assistant_page(projects):
    """Main query assistant page"""
    
    st.header("🔍 Query Assistant")
    st.write("Ask a question or describe your problem, and I'll find similar tickets and suggest solutions.")
    
    # Query input
    query = st.text_area(
        "Enter your query:",
        placeholder="Example: How do I fix authentication errors in the API?",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        max_results = st.number_input("Max Results", min_value=1, max_value=10, value=5)
    with col2:
        search_button = st.button("🔍 Search & Analyze", type="primary", use_container_width=True)
    
    if search_button and query:
        with st.spinner("🤖 Analyzing your query and searching historical tickets..."):
            try:
                # Call API
                response = requests.post(
                    f"{API_URL}/api/query",
                    json={
                        "query": query,
                        "projects": projects,
                        "max_results": max_results
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display query analysis
                    st.subheader("📋 Query Analysis")
                    analysis = data.get("analysis", {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Issue Type", analysis.get("issue_type", "Unknown"))
                    with col2:
                        st.metric("Priority", analysis.get("priority", "Medium"))
                    with col3:
                        st.metric("Historical Tickets", data.get("total_historical_tickets", 0))
                    
                    # Display matched tickets
                    st.subheader("🎯 Matched Tickets")
                    matched_tickets = data.get("matched_tickets", [])
                    
                    if matched_tickets:
                        for i, match in enumerate(matched_tickets, 1):
                            ticket_data = match.get("ticket_data", {})
                            
                            with st.expander(
                                f"#{i} [{ticket_data.get('key', 'N/A')}] {ticket_data.get('summary', 'N/A')} "
                                f"(Relevance: {match.get('relevance_score', 0)}/10)",
                                expanded=(i == 1)
                            ):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write("**Description:**")
                                    st.write(ticket_data.get('description', 'No description')[:500] + "...")
                                    
                                    st.write("**Why it's relevant:**")
                                    st.info(match.get('reasoning', 'Similar content'))
                                    
                                    if match.get('has_solution'):
                                        st.write("**Solution:**")
                                        st.success(match.get('solution_summary', ticket_data.get('resolution', 'N/A')))
                                
                                with col2:
                                    st.metric("Status", ticket_data.get('status', 'N/A'))
                                    st.metric("Priority", ticket_data.get('priority', 'N/A'))
                                    if ticket_data.get('url'):
                                        st.link_button("View in JIRA", ticket_data['url'])
                    else:
                        st.warning("No matching tickets found.")
                    
                    # Display AI-generated resolution
                    st.subheader("💡 AI-Generated Resolution")
                    resolution = data.get("resolution", "")
                    
                    if resolution:
                        # Format resolution text for better readability
                        formatted_resolution = resolution.replace('\n', '<br>')
                        st.markdown(
                            f'<div class="resolution-box">{formatted_resolution}</div>', 
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("No resolution could be generated. Try refining your query.")
                
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


def ticket_search_page(projects):
    """Ticket search and browsing page"""
    
    st.header("🎫 Ticket Search")
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        statuses = st.multiselect(
            "Status",
            ["Done", "Resolved", "Closed", "In Progress", "Open"],
            default=["Done", "Resolved"]
        )
    
    with col2:
        days_back = st.selectbox("Time Range", [7, 30, 60, 90], index=1)
    
    with col3:
        max_results = st.number_input("Max Results", min_value=10, max_value=200, value=50)
    
    if st.button("🔍 Search Tickets", type="primary"):
        with st.spinner("Searching tickets..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/tickets/search",
                    json={
                        "projects": projects,
                        "statuses": statuses,
                        "days_back": days_back,
                        "max_results": max_results
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    tickets = data.get("tickets", [])
                    
                    st.success(f"Found {len(tickets)} tickets")
                    
                    # Convert to DataFrame for better display
                    if tickets:
                        df = pd.DataFrame([{
                            "Key": t.get("key"),
                            "Summary": t.get("summary", "")[:80] + "...",
                            "Status": t.get("status"),
                            "Priority": t.get("priority"),
                            "Updated": t.get("updated", "")[:10]
                        } for t in tickets])
                        
                        st.dataframe(df, use_container_width=True)
                        
                        # Ticket details
                        selected_key = st.selectbox("Select a ticket to view details:", [t["key"] for t in tickets])
                        
                        if selected_key:
                            ticket = next((t for t in tickets if t["key"] == selected_key), None)
                            if ticket:
                                display_ticket_details(ticket)
                
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


def analytics_dashboard_page(projects):
    """Analytics and insights dashboard"""
    
    st.header("📊 Analytics Dashboard")
    
    # Time range selector
    col1, col2 = st.columns([1, 3])
    with col1:
        days_back = st.selectbox("Time Range", [7, 30, 60, 90], index=1, key="analytics_days")
    
    if st.button("📈 Generate Analytics", type="primary"):
        with st.spinner("Analyzing data..."):
            try:
                # Get statistics
                stats_response = requests.post(
                    f"{API_URL}/api/analytics/statistics",
                    json={"projects": projects, "days_back": days_back}
                )
                
                # Get insights
                insights_response = requests.post(
                    f"{API_URL}/api/insights",
                    json={"projects": projects, "days_back": days_back}
                )
                
                if stats_response.status_code == 200 and insights_response.status_code == 200:
                    stats = stats_response.json()
                    insights_data = insights_response.json()
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Tickets", stats.get("total_tickets", 0))
                    with col2:
                        st.metric("Projects Analyzed", len(projects))
                    with col3:
                        st.metric("Days Analyzed", days_back)
                    
                    st.divider()
                    
                    # Charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Status distribution
                        st.subheader("📊 Status Distribution")
                        status_data = stats.get("by_status", {})
                        if status_data:
                            fig = px.pie(
                                names=list(status_data.keys()),
                                values=list(status_data.values()),
                                title="Tickets by Status"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Priority distribution
                        st.subheader("⚡ Priority Distribution")
                        priority_data = stats.get("by_priority", {})
                        if priority_data:
                            fig = px.bar(
                                x=list(priority_data.keys()),
                                y=list(priority_data.values()),
                                title="Tickets by Priority",
                                labels={"x": "Priority", "y": "Count"}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Project distribution
                    st.subheader("📁 Project Distribution")
                    project_data = stats.get("by_project", {})
                    if project_data:
                        fig = px.bar(
                            x=list(project_data.keys()),
                            y=list(project_data.values()),
                            title="Tickets by Project",
                            labels={"x": "Project", "y": "Count"},
                            color=list(project_data.keys())
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Insights
                    st.divider()
                    st.subheader("💡 Key Insights")
                    
                    insights = insights_data.get("insights", {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Common Issues:**")
                        common_issues = insights.get("common_issues", [])
                        for issue in common_issues[:5]:
                            st.write(f"• {issue}")
                    
                    with col2:
                        st.write("**Common Resolutions:**")
                        common_resolutions = insights.get("common_resolutions", [])
                        for resolution in common_resolutions[:5]:
                            st.write(f"• {resolution}")
                    
                    st.write("**Recommendations:**")
                    recommendations = insights.get("recommendations", [])
                    for rec in recommendations:
                        st.info(f"💡 {rec}")
                
                else:
                    st.error("Failed to fetch analytics data")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


def settings_page():
    """Settings and configuration page"""
    
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Configuration")
    
    # JIRA settings
    with st.expander("JIRA Configuration", expanded=True):
        jira_url = st.text_input("JIRA URL", value=os.getenv("JIRA_URL", ""))
        jira_email = st.text_input("JIRA Email", value=os.getenv("JIRA_EMAIL", ""))
        jira_token = st.text_input("JIRA API Token", type="password")
    
    # LLM settings
    with st.expander("LLM Configuration"):
        groq_key = st.text_input("Groq API Key", type="password")
        llm_model = st.selectbox(
            "LLM Model",
            ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    
    # Agent settings
    with st.expander("Agent Settings"):
        similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)
        top_k_results = st.number_input("Top K Results", min_value=1, max_value=10, value=5)
        auto_suggest = st.checkbox("Auto-suggest resolutions", value=True)
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
        st.info("Please restart the application for changes to take effect.")
    
    st.divider()
    
    # About section
    st.subheader("ℹ️ About")
    st.write("""
    **JIRA AI Agent v0.1.0**
    
    An intelligent agent that resolves Product and Technical Queries by analyzing 
    historical JIRA tickets using AI-powered matching and resolution generation.
    
    **Features:**
    - 🎯 Smart query matching with historical tickets
    - 💡 AI-generated resolutions and recommendations
    - 📊 Analytics and insights dashboard
    - 🔄 Real-time JIRA integration via MCP
    - 🚀 Powered by Groq Llama LLM and Langchain
    
    **Tech Stack:**
    - Backend: Python, Flask, FastMCP
    - LLM: ChatGroq (Llama 3.1)
    - Frontend: Streamlit
    - Integration: JIRA API via MCP Server
    """)


def display_ticket_details(ticket):
    """Display detailed ticket information"""
    
    st.divider()
    st.subheader(f"🎫 {ticket['key']}: {ticket['summary']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", ticket.get('status', 'N/A'))
    with col2:
        st.metric("Priority", ticket.get('priority', 'N/A'))
    with col3:
        st.metric("Resolution", ticket.get('resolution', 'Unresolved'))
    
    st.write("**Description:**")
    st.write(ticket.get('description', 'No description available'))
    
    st.write("**Details:**")
    st.write(f"- **Reporter:** {ticket.get('reporter', 'N/A')}")
    st.write(f"- **Assignee:** {ticket.get('assignee', 'N/A')}")
    st.write(f"- **Created:** {ticket.get('created', 'N/A')[:10]}")
    st.write(f"- **Updated:** {ticket.get('updated', 'N/A')[:10]}")
    
    if ticket.get('labels'):
        st.write(f"- **Labels:** {', '.join(ticket['labels'])}")
    
    # Comments
    comments = ticket.get('comments', [])
    if comments:
        st.write("**Comments:**")
        for comment in comments:
            with st.expander(f"{comment.get('author', 'Unknown')} - {comment.get('created', '')[:10]}"):
                st.write(comment.get('body', ''))
    
    if ticket.get('url'):
        st.link_button("🔗 View in JIRA", ticket['url'], use_container_width=True)


def display_quick_stats():
    """Display quick statistics in sidebar"""
    try:
        response = requests.post(
            f"{API_URL}/api/analytics/statistics",
            json={"days_back": 7}
        )
        
        if response.status_code == 200:
            stats = response.json()
            st.metric("Total Tickets (7d)", stats.get("total_tickets", 0))
    except:
        st.write("Stats unavailable")


if __name__ == "__main__":
    main()
