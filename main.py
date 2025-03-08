#!/usr/bin/env python3
"""
YNAB Emoji Namer - Main entry point
Adds appropriate emojis to YNAB payees using the Groq AI API
"""
from src.config import load_config
from src.app import EmojiNamer

def main():
    """Main entry point."""
    try:
        config = load_config()
        app = EmojiNamer(config)
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())