"""
Utility functions for JIRA AI Agent
"""

from typing import List, Dict, Any, Optional
import re
from datetime import datetime


def clean_text(text: Optional[str]) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?]', '', text)
    
    return text.strip()


def extract_keywords(text: Optional[str], min_length: int = 3) -> List[str]:
    """Extract keywords from text"""
    if not text:
        return []
    
    # Simple keyword extraction
    words = text.lower().split()
    keywords = [w for w in words if len(w) >= min_length and w.isalnum()]
    
    return list(set(keywords))


def calculate_similarity(text1: Optional[str], text2: Optional[str]) -> float:
    """Calculate simple text similarity score"""
    if not text1 or not text2:
        return 0.0
    
    words1 = set(extract_keywords(text1))
    words2 = set(extract_keywords(text2))
    
    if not words1 or not words2:
        return 0.0
    
    # Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0


def format_ticket_summary(ticket: Dict[str, Any]) -> str:
    """Format ticket information for display"""
    summary = f"[{ticket.get('key', 'N/A')}] {ticket.get('summary', 'N/A')}\n"
    summary += f"Status: {ticket.get('status', 'N/A')} | "
    summary += f"Priority: {ticket.get('priority', 'N/A')} | "
    summary += f"Updated: {ticket.get('updated', 'N/A')[:10]}\n"
    
    return summary


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object"""
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return datetime.now()


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration structure"""
    required_keys = ['jira', 'llm', 'analytics', 'agent']
    
    for key in required_keys:
        if key not in config:
            return False
    
    return True


def truncate_text(text: Optional[str], max_length: int = 200) -> str:
    """Truncate text to specified length"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def calculate_resolution_time(created: str, updated: str) -> float:
    """Calculate resolution time in days"""
    try:
        created_dt = parse_date(created)
        updated_dt = parse_date(updated)
        delta = updated_dt - created_dt
        return round(delta.total_seconds() / 86400, 2)  # Convert to days
    except:
        return 0.0
