"""YNAB Emoji Namer - Main application module."""
import sys
import os
from typing import List, Set

from core.config import BaseConfig
from core.services.ynab_service import YNABService, Payee
from core.services.llm_service import LLMService, get_llm_service
from core.utils.text_utils import has_emoji

from .ignored_payees import IgnoredPayeesManager

class EmojiNamer:
    """Main application class for YNAB Emoji Namer."""
    
    def __init__(self, config: BaseConfig, llm_config: dict, ignored_payees_file: str = None):
        self.config = config
        self.ynab_service = YNABService(config.ynab_api_key, config.ynab_budget_id)
        self.llm_service = get_llm_service(**llm_config)
        
        # Use a default path relative to the ynab_namer directory if none provided
        if ignored_payees_file is None:
            # Get the directory where the ynab_namer package is located
            ynab_namer_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ignored_payees_file = os.path.join(ynab_namer_dir, "ignored_payees.json")
            
        self.ignored_payees = IgnoredPayeesManager(ignored_payees_file)

    def get_payees_needing_emoji(self) -> List[Payee]:
        """Get list of payees that need emoji assignment."""
        all_payees = self.ynab_service.get_payees()
        
        # Debug which payees with potential emojis are being included
        for p in all_payees:
            if not self.ignored_payees.is_ignored(p.id) and not p.deleted and p.name.strip():
                if "⏳" in p.name or "⌛" in p.name or "⏱" in p.name or "⏰" in p.name:
                    print(f"Payee with time symbol not detected as emoji: {p.name}")
        
        return [
            p for p in all_payees 
            if not has_emoji(p.name)
            and not self.ignored_payees.is_ignored(p.id)
            and not p.deleted
            and p.name.strip()
        ]

    def process_payee(self, payee: Payee) -> None:
        """Process a single payee for emoji assignment with retry option."""
        print(f"\n{'='*40}")
        print(f"Processing: {payee.name}")
        
        # Track previously suggested emojis to avoid duplicates
        suggested_emojis: Set[str] = set()
        retry_count = 0
        
        while True:  # Continue until user makes a decision (not retry)
            # Add retry count context to the prompt if this isn't the first attempt
            retry_context = ""
            if retry_count > 0:
                retry_context = f" This is retry #{retry_count + 1}. Previously suggested: {', '.join(suggested_emojis)}"
                
            emoji = self.llm_service.get_emoji_suggestion(payee.name + retry_context)
            if not emoji:
                print(f"Couldn't get emoji for {payee.name}, skipping.")
                return
                
            # Track this suggestion
            suggested_emojis.add(emoji)
            retry_count += 1
                
            suggested_name = f"{payee.name} {emoji}"
            print(f"Suggested name: {suggested_name}")
            
            while True:
                choice = input("Accept (y), Reject (n), Ignore (i), or Retry (r)? [y/n/i/r]: ").strip().lower()
                if choice in ('y', 'n', 'i', 'r'):
                    break
                print("Invalid choice. Please enter y, n, i, or r.")
            
            if choice == 'y':
                if self.ynab_service.update_payee_name(payee.id, suggested_name):
                    print(f"✅ Successfully updated {payee.name} to {suggested_name}")
                else:
                    print(f"❌ Failed to update {payee.name}")
                return  # Exit after updating
            elif choice == 'i':
                self.ignored_payees.add(payee.id, payee.name)
                print(f"Added {payee.name} to ignored payees")
                return  # Exit after ignoring
            elif choice == 'n':
                return  # Exit without changes
            elif choice == 'r':
                print("Retrying with a different emoji suggestion...")
                # Continue the outer loop to get a new suggestion

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