#!/usr/bin/env python3
"""
YNAB Duplicate Payee Cleanup - Main entry point
Identifies and merges duplicate payees in YNAB by comparing names without whitespace and emojis
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path so we can import core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import load_config, ConfigError
from .src.app import DuplicatePayeeCleanup

def main():
    """Main entry point."""
    try:
        # Explicitly load the .env file from the current directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)
        
        # Load base configuration without project prefix
        config = load_config()
        
        # Create and run app
        app = DuplicatePayeeCleanup(
            config=config,
            dry_run=os.getenv("YNAB_DUPLICATE_CLEANUP_DRY_RUN", "true").lower() == "true"
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