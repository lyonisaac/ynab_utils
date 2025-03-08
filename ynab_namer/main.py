#!/usr/bin/env python3
"""
YNAB Emoji Namer - Main entry point
Adds appropriate emojis to YNAB payees using LLM services
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path so we can import core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import load_config, ConfigError
from src.app import EmojiNamer

def main():
    """Main entry point."""
    try:
        # Explicitly load the .env file from the current directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)
        
        # Load base configuration without project prefix
        config = load_config()
        
        # Load LLM configuration
        llm_config = {
            "provider": os.getenv("LLM_PROVIDER", "groq"),
            "api_key": os.getenv("GROQ_API_KEY", ""),
            "model": os.getenv("GROQ_MODEL", "llama3-70b-8192")
        }
        
        # Create and run app
        app = EmojiNamer(
            config=config,
            llm_config=llm_config,
            ignored_payees_file=os.getenv("YNAB_NAMER_IGNORED_PAYEES_FILE", "ignored_payees.json")
        )
        app.run()
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())