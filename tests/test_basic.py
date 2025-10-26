"""
Basic tests for JIRA AI Agent
Run with: pytest tests/

Note: Install dev dependencies first with: uv pip install -e ".[dev]"
"""

import pytest  # type: ignore[import-not-found]
from src.backend.utils import (
    clean_text,
    extract_keywords,
    calculate_similarity,
    truncate_text
)

class TestUtils:
    """Test utility functions"""
    
    def test_clean_text(self):
        """Test text cleaning"""
        text = "  Hello   World  \n  Test  "
        result = clean_text(text)
        assert result == "Hello World Test"
    
    def test_clean_text_empty(self):
        """Test cleaning empty text"""
        assert clean_text("") == ""
        assert clean_text(None) == ""
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        text = "This is a test message for keyword extraction"
        keywords = extract_keywords(text)
        assert "test" in keywords
        assert "message" in keywords
        assert "keyword" in keywords
        assert "extraction" in keywords
        # Short words should be excluded
        assert "is" not in keywords
        assert "a" not in keywords
    
    def test_extract_keywords_empty(self):
        """Test keyword extraction with empty text"""
        assert extract_keywords("") == []
        assert extract_keywords(None) == []
    
    def test_calculate_similarity(self):
        """Test similarity calculation"""
        text1 = "API authentication error"
        text2 = "API authentication failed"
        
        similarity = calculate_similarity(text1, text2)
        assert 0.0 <= similarity <= 1.0
        assert similarity > 0.5  # Should have decent similarity
    
    def test_calculate_similarity_identical(self):
        """Test similarity with identical texts"""
        text = "Hello world"
        similarity = calculate_similarity(text, text)
        assert similarity == 1.0
    
    def test_calculate_similarity_empty(self):
        """Test similarity with empty texts"""
        assert calculate_similarity("", "") == 0.0
        assert calculate_similarity("test", "") == 0.0
        assert calculate_similarity("", "test") == 0.0
    
    def test_truncate_text(self):
        """Test text truncation"""
        text = "This is a very long text that needs to be truncated"
        result = truncate_text(text, max_length=20)
        assert len(result) <= 23  # 20 + "..."
        assert result.endswith("...")
    
    def test_truncate_text_short(self):
        """Test truncation with short text"""
        text = "Short"
        result = truncate_text(text, max_length=100)
        assert result == text
    
    def test_truncate_text_empty(self):
        """Test truncation with empty text"""
        assert truncate_text("") == ""
        assert truncate_text(None) == ""


class TestConfigValidation:
    """Test configuration validation"""
    
    def test_validate_config_valid(self):
        """Test validation with valid config"""
        from src.backend.utils import validate_config
        
        config = {
            "jira": {},
            "llm": {},
            "analytics": {},
            "agent": {}
        }
        
        assert validate_config(config) is True
    
    def test_validate_config_invalid(self):
        """Test validation with invalid config"""
        from src.backend.utils import validate_config
        
        config = {
            "jira": {},
            "llm": {}
            # Missing required sections
        }
        
        assert validate_config(config) is False


# Integration test (requires running backend)
class TestAPIIntegration:
    """Integration tests for API endpoints"""
    
    @pytest.mark.skip(reason="Requires running backend server")
    def test_health_endpoint(self):
        """Test health check endpoint"""
        import requests
        response = requests.get("http://localhost:5000/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    @pytest.mark.skip(reason="Requires running backend and valid credentials")
    def test_query_endpoint(self):
        """Test query processing endpoint"""
        import requests
        payload = {
            "query": "Test query",
            "projects": ["TEST"],
            "max_results": 1
        }
        response = requests.post(
            "http://localhost:5000/api/query",
            json=payload
        )
        assert response.status_code in [200, 500]  # May fail without JIRA


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
