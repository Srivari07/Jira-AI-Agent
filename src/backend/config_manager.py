"""
Configuration loader and manager
"""

import os
import yaml
from typing import Dict, Any, Optional, Union
from dotenv import load_dotenv

load_dotenv()


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                "../../config/config.yaml"
            )
        
        self.config_path = config_path
        self.config = self._load_config()
        self.env_vars = self._load_env_vars()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {self.config_path}")
            return self._default_config()
    
    def _load_env_vars(self) -> Dict[str, Union[str, float, int]]:
        """Load environment variables"""
        return {
            'jira_url': os.getenv('JIRA_URL', ''),
            'jira_email': os.getenv('JIRA_EMAIL', ''),
            'jira_token': os.getenv('JIRA_API_TOKEN', ''),
            'groq_api_key': os.getenv('GROQ_API_KEY', ''),
            'llm_model': os.getenv('LLM_MODEL', 'llama-3.1-70b-versatile'),
            'llm_temperature': float(os.getenv('LLM_TEMPERATURE', '0.7')),
            'llm_max_tokens': int(os.getenv('LLM_MAX_TOKENS', '2048')),
        }
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'jira': {
                'projects': ['PROD', 'TECH'],
                'issue_types': ['Bug', 'Task', 'Story'],
                'resolved_statuses': ['Done', 'Resolved', 'Closed'],
                'fields': ['summary', 'description', 'status', 'resolution']
            },
            'llm': {
                'model': 'llama-3.1-70b-versatile',
                'temperature': 0.7,
                'max_tokens': 2048,
                'similarity_threshold': 0.7,
                'top_k_results': 5
            },
            'analytics': {
                'enabled': True,
                'metrics': ['resolution_time', 'ticket_volume'],
                'time_ranges': ['7d', '30d', '90d']
            },
            'agent': {
                'auto_suggest': True,
                'attach_documents': True,
                'confidence_threshold': 0.8,
                'max_suggestions': 3
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def get_env(self, key: str, default: Union[str, float, int] = '') -> Union[str, float, int]:
        """Get environment variable"""
        return self.env_vars.get(key, default)
    
    def validate(self) -> bool:
        """Validate configuration"""
        required_sections = ['jira', 'llm', 'analytics', 'agent']
        
        for section in required_sections:
            if section not in self.config:
                print(f"Warning: Missing config section: {section}")
                return False
        
        return True
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration"""
        self.config.update(updates)
    
    def save(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config: {e}")


# Global config instance
config = ConfigManager()
