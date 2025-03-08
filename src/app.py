"""YNAB Emoji Namer - Main application module."""
import re
import sys
from typing import List

from .config import Config, load_config
from .ynab_service import YNABService, Payee
from .groq_service import GroqService
from .ignored_payees import IgnoredPayeesManager

class EmojiNamer:
    """Main application class for YNAB Emoji Namer."""
    
    def __init__(self, config: Config):
        self.config = config
        self.ynab_service = YNABService(config.ynab_api_key, config.ynab_budget_id)
        self.groq_service = GroqService(config.groq_api_key, config.groq_model)
        self.ignored_payees = IgnoredPayeesManager(config.ignored_payees_file)

    def has_emoji(self, text: str) -> bool:
        """Check if text contains an emoji."""
        emoji_pattern = re.compile(
            "["
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+"
        )
        return bool(emoji_pattern.search(text))

    def get_payees_needing_emoji(self) -> List[Payee]:
        """Get list of payees that need emoji assignment."""
        all_payees = self.ynab_service.get_payees()
        return [
            p for p in all_payees 
            if not self.has_emoji(p.name)
            and not self.ignored_payees.is_ignored(p.id)
            and not p.deleted
            and p.name.strip()
        ]

    def process_payee(self, payee: Payee) -> None:
        """Process a single payee for emoji assignment."""
        print(f"\n{'='*40}")
        print(f"Processing: {payee.name}")
        
        emoji = self.groq_service.get_emoji_suggestion(payee.name)
        if not emoji:
            print(f"Couldn't get emoji for {payee.name}, skipping.")
            return
            
        suggested_name = f"{payee.name} {emoji}"
        print(f"Suggested name: {suggested_name}")
        
        while True:
            choice = input("Accept (y), Reject (n), or Ignore (i)? [y/n/i]: ").strip().lower()
            if choice in ('y', 'n', 'i'):
                break
            print("Invalid choice. Please enter y, n, or i.")
        
        if choice == 'y':
            if self.ynab_service.update_payee_name(payee.id, suggested_name):
                print(f"✅ Successfully updated {payee.name} to {suggested_name}")
            else:
                print(f"❌ Failed to update {payee.name}")
        elif choice == 'i':
            self.ignored_payees.add(payee.id, payee.name)
            print(f"Added {payee.name} to ignored payees")

    def run(self) -> None:
        """Run the emoji naming process."""
        print("🏦 YNAB Emoji Namer 🏦")
        print("="*40)
        
        payees = self.get_payees_needing_emoji()
        if not payees:
            print("No payees need emoji updates. Exiting.")
            return
            
        print(f"Found {len(payees)} payees that need emojis")
        
        processed = set()
        for payee in payees:
            if payee.id in processed:
                continue
            self.process_payee(payee)
            processed.add(payee.id)
        
        print("\n🎉 All done! Thank you for using YNAB Emoji Namer")