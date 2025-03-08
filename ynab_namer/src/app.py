"""YNAB Emoji Namer - Main application module."""
import sys
from typing import List

from core.config import BaseConfig
from core.services.ynab_service import YNABService, Payee
from core.services.llm_service import LLMService, get_llm_service
from core.utils.text_utils import has_emoji

from .ignored_payees import IgnoredPayeesManager

class EmojiNamer:
    """Main application class for YNAB Emoji Namer."""
    
    def __init__(self, config: BaseConfig, llm_config: dict, ignored_payees_file: str = "ignored_payees.json"):
        self.config = config
        self.ynab_service = YNABService(config.ynab_api_key, config.ynab_budget_id)
        self.llm_service = get_llm_service(**llm_config)
        self.ignored_payees = IgnoredPayeesManager(ignored_payees_file)

    def get_payees_needing_emoji(self) -> List[Payee]:
        """Get list of payees that need emoji assignment."""
        all_payees = self.ynab_service.get_payees()
        return [
            p for p in all_payees 
            if not has_emoji(p.name)
            and not self.ignored_payees.is_ignored(p.id)
            and not p.deleted
            and p.name.strip()
        ]

    def process_payee(self, payee: Payee) -> None:
        """Process a single payee for emoji assignment."""
        print(f"\n{'='*40}")
        print(f"Processing: {payee.name}")
        
        emoji = self.llm_service.get_emoji_suggestion(payee.name)
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