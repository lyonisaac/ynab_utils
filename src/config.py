"""Configuration management for YNAB Emoji Namer."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Config:
    """Application configuration."""
    ynab_api_key: str
    ynab_budget_id: str
    groq_api_key: str
    groq_model: str
    ignored_payees_file: str = "ignored_payees.json"

def load_config() -> Config:
    """Load configuration from environment variables."""
    load_dotenv()
    
    required_vars = {
        "YNAB_API_KEY": os.getenv("YNAB_API_KEY"),
        "YNAB_BUDGET_ID": os.getenv("YNAB_BUDGET_ID"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    }
    
    missing = [key for key, value in required_vars.items() if not value]
    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}")
    
    return Config(
        ynab_api_key=required_vars["YNAB_API_KEY"],
        ynab_budget_id=required_vars["YNAB_BUDGET_ID"],
        groq_api_key=required_vars["GROQ_API_KEY"],
        groq_model=os.getenv("GROQ_MODEL", "llama3-70b-8192")
    )