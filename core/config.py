"""Configuration management for YNAB projects."""
import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class ConfigError(Exception):
    """Configuration related exception."""
    pass


@dataclass
class BaseConfig:
    """Base configuration class with common settings."""
    ynab_api_key: str
    ynab_budget_id: str


@dataclass
class LLMConfig:
    """LLM-specific configuration."""
    provider: str
    api_key: str
    model: Optional[str] = None
    
    @classmethod
    def from_env(cls, prefix: str = ""):
        """Create LLM config from environment variables."""
        provider = os.getenv(f"{prefix}LLM_PROVIDER", "groq").lower()
        
        if provider == "groq":
            return cls(
                provider=provider,
                api_key=os.getenv(f"{prefix}GROQ_API_KEY", ""),
                model=os.getenv(f"{prefix}GROQ_MODEL", "llama3-70b-8192")
            )
        else:
            raise ConfigError(f"Unsupported LLM provider: {provider}")


def load_config(project_name: str = None) -> BaseConfig:
    """
    Load configuration from environment variables.
    
    Args:
        project_name: Optional name of the project to load specific config for
                     If provided, will look for PROJECT_NAME_* env vars
    
    Returns:
        BaseConfig: Configuration object with loaded values
    """
    load_dotenv()
    
    # Define prefix based on project name
    prefix = f"{project_name.upper()}_" if project_name else ""
    
    # Check for required config
    required_vars = {
        "YNAB_API_KEY": os.getenv(f"{prefix}YNAB_API_KEY"),
        "YNAB_BUDGET_ID": os.getenv(f"{prefix}YNAB_BUDGET_ID"),
    }
    
    missing = [key for key, value in required_vars.items() if not value]
    if missing:
        raise ConfigError(f"Missing required configuration: {', '.join(missing)}")
    
    return BaseConfig(
        ynab_api_key=required_vars["YNAB_API_KEY"],
        ynab_budget_id=required_vars["YNAB_BUDGET_ID"]
    )