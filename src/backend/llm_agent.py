"""
LLM Integration with ChatGroq and Langchain
Handles query analysis and ticket matching using Llama LLM
"""

from typing import List, Dict, Any, Optional
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from pydantic import SecretStr
from dotenv import load_dotenv
import yaml
import json

load_dotenv()


class JiraLLMAgent:
    """LLM Agent for analyzing queries and matching tickets"""
    def __init__(self):
        # Initialize Groq LLM
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            api_key=SecretStr(api_key) if api_key else None,
            model=os.getenv("LLM_MODEL", "llama-3.1-70b-versatile"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048"))
        )
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), "../../config/config.yaml")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize embeddings for similarity matching
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Setup prompt templates for different tasks"""
        
        # Query analysis prompt
        self.query_analysis_prompt = PromptTemplate(
            input_variables=["query"],
            template="""You are an expert technical support analyst. Analyze the following user query and extract:
1. The main problem or question
2. Key technical terms and concepts
3. The type of issue (bug, feature request, question, etc.)
4. Priority level (high, medium, low)

User Query: {query}

Provide your analysis in JSON format:
{{
    "main_problem": "brief description",
    "key_terms": ["term1", "term2", ...],
    "issue_type": "type",
    "priority": "level",
    "summary": "one-line summary"
}}
"""
        )
        
        # Ticket matching prompt
        self.ticket_matching_prompt = PromptTemplate(
            input_variables=["query", "tickets"],
            template="""You are an expert at matching user queries with historical JIRA tickets.

User Query: {query}

Historical Tickets:
{tickets}

Analyze the tickets and rank them by relevance to the user query. For each relevant ticket:
1. Explain why it's relevant
2. Give a relevance score (0-10)
3. Identify if it contains a solution or useful information

Return your analysis in JSON format:
{{
    "matches": [
        {{
            "ticket_key": "KEY-123",
            "relevance_score": 9,
            "reasoning": "explanation",
            "has_solution": true,
            "solution_summary": "brief summary of solution"
        }}
    ]
}}

Only include tickets with relevance_score >= 6. Sort by relevance_score descending.
"""
        )
        
        # Resolution generation prompt
        self.resolution_prompt = PromptTemplate(
            input_variables=["query", "matched_tickets"],
            template="""You are a technical support expert. Based on the user query and similar historical tickets, provide a comprehensive resolution.

User Query: {query}

Similar Historical Tickets:
{matched_tickets}

Provide a detailed resolution that includes:
1. Direct answer to the query
2. Step-by-step solution if applicable
3. References to similar tickets
4. Additional recommendations or best practices

Format your response clearly and professionally.
"""
        )
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze user query to extract key information
        
        Args:
            query: User's question or problem description
            
        Returns:
            Analysis results with main problem, key terms, etc.
        """
        try:
            chain = self.query_analysis_prompt | self.llm
            response = chain.invoke({"query": query}).content
            # Parse JSON response
            response_str = response if isinstance(response, str) else str(response)
            analysis = json.loads(response_str)
            return analysis
        except Exception as e:
            # Fallback to simple analysis
            return {
                "main_problem": query,
                "key_terms": [],
                "issue_type": "unknown",
                "priority": "medium",
                "summary": query[:100]
            }
    
    def match_tickets(
        self,
        query: str,
        historical_tickets: List[Dict[str, Any]],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Match user query with historical tickets
        
        Args:
            query: User's question or problem
            historical_tickets: List of historical JIRA tickets
            top_k: Number of top matches to return
            
        Returns:
            Ranked list of matching tickets with relevance scores
        """
        if not historical_tickets:
            return []
        
        if top_k is None:
            top_k = self.config['llm']['top_k_results']
        
        # Ensure top_k is an int for type safety
        top_k = int(top_k) if top_k is not None else 5
        
        # Format tickets for LLM
        tickets_text = ""
        for i, ticket in enumerate(historical_tickets[:20], 1):  # Limit to 20 for context
            tickets_text += f"\n{i}. [{ticket['key']}] {ticket['summary']}\n"
            description = (ticket.get('description') or 'N/A')[:200]
            tickets_text += f"   Description: {description}...\n"
            tickets_text += f"   Status: {ticket['status']} | Resolution: {ticket.get('resolution') or 'N/A'}\n"
        
        try:
            chain = self.ticket_matching_prompt | self.llm
            response = chain.invoke({"query": query, "tickets": tickets_text}).content
            # Parse JSON response
            response_str = response if isinstance(response, str) else str(response)
            result = json.loads(response_str)
            matches = result.get("matches", [])
            
            # Enhance matches with full ticket data
            enhanced_matches = []
            for match in matches[:top_k]:
                ticket_key = match["ticket_key"]
                full_ticket = next((t for t in historical_tickets if t["key"] == ticket_key), None)
                if full_ticket:
                    enhanced_match = {
                        **match,
                        "ticket_data": full_ticket
                    }
                    enhanced_matches.append(enhanced_match)
            
            return enhanced_matches
        except Exception as e:
            # Fallback to simple keyword matching
            return self._simple_keyword_match(query, historical_tickets, top_k)
    
    def _simple_keyword_match(
        self,
        query: str,
        tickets: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Simple fallback keyword matching"""
        query_lower = query.lower()
        matches = []
        
        for ticket in tickets:
            score = 0
            summary = (ticket.get('summary') or '').lower()
            description = (ticket.get('description') or '').lower()
            
            # Simple keyword scoring
            for word in query_lower.split():
                if len(word) > 3:  # Only consider meaningful words
                    if word in summary:
                        score += 2
                    if word in description:
                        score += 1
            
            if score > 0:
                matches.append({
                    "ticket_key": ticket["key"],
                    "relevance_score": min(score, 10),
                    "reasoning": "Keyword match",
                    "has_solution": bool(ticket.get("resolution")),
                    "solution_summary": ticket.get("resolution") or "",
                    "ticket_data": ticket
                })
        
        # Sort by score and return top_k
        matches.sort(key=lambda x: x["relevance_score"], reverse=True)
        return matches[:top_k]
    
    def generate_resolution(
        self,
        query: str,
        matched_tickets: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a comprehensive resolution based on matched tickets
        
        Args:
            query: User's question or problem
            matched_tickets: List of matched tickets with relevance scores
            
        Returns:
            Generated resolution text
        """
        if not matched_tickets:
            return "No similar historical tickets found. Please provide more details or consult the team."
        
        # Format matched tickets for prompt
        tickets_text = ""
        for i, match in enumerate(matched_tickets, 1):
            ticket = match.get("ticket_data", {})
            tickets_text += f"\n{i}. [{ticket.get('key', 'N/A')}] {ticket.get('summary', 'N/A')}\n"
            tickets_text += f"   Relevance Score: {match.get('relevance_score', 0)}/10\n"
            tickets_text += f"   Resolution: {ticket.get('resolution', 'N/A')}\n"
            
            # Add relevant comments if available
            comments = ticket.get('comments', [])
            if comments:
                tickets_text += f"   Key Comments:\n"
                for comment in comments[:2]:  # Top 2 comments
                    tickets_text += f"     - {comment.get('body', '')[:150]}...\n"
        
        try:
            chain = self.resolution_prompt | self.llm
            response = chain.invoke({"query": query, "matched_tickets": tickets_text})
            resolution = response.content if hasattr(response, 'content') else str(response)
            return str(resolution) if not isinstance(resolution, str) else resolution
        except Exception as e:
            # Fallback to basic response
            top_ticket = matched_tickets[0].get("ticket_data", {})
            return f"""Based on similar ticket {top_ticket.get('key', 'N/A')}:

Summary: {top_ticket.get('summary', 'N/A')}
Resolution: {top_ticket.get('resolution', 'No resolution documented')}

Please refer to the ticket for more details: {top_ticket.get('url', 'N/A')}
"""
    
    def extract_key_insights(
        self,
        tickets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Extract key insights and patterns from tickets
        
        Args:
            tickets: List of JIRA tickets
            
        Returns:
            Insights about common issues, resolutions, etc.
        """
        if not tickets:
            return {"insights": []}
        
        insights_prompt = PromptTemplate(
            input_variables=["tickets_summary"],
            template="""Analyze these JIRA tickets and identify:
1. Common issues and patterns
2. Frequently used resolutions
3. Recurring technical problems
4. Recommendations for knowledge base

Tickets Summary:
{tickets_summary}

Provide insights in JSON format:
{{
    "common_issues": ["issue1", "issue2", ...],
    "common_resolutions": ["resolution1", "resolution2", ...],
    "recommendations": ["recommendation1", "recommendation2", ...]
}}
"""
        )
        
        # Summarize tickets
        summary = ""
        for ticket in tickets[:30]:  # Analyze top 30
            summary += f"- {ticket.get('summary', 'N/A')} ({ticket.get('status', 'N/A')})\n"
        
        try:
            chain = insights_prompt | self.llm
            response = chain.invoke({"tickets_summary": summary}).content
            response_str = response if isinstance(response, str) else str(response)
            insights = json.loads(response_str)
            return insights
        except Exception as e:
            return {
                "common_issues": [],
                "common_resolutions": [],
                "recommendations": ["Unable to generate insights at this time"]
            }
