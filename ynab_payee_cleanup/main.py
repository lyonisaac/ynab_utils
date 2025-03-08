#!/usr/bin/env python3
"""
YNAB Payee Cleanup - Main entry point
Filters and deletes payees without associated transactions from YNAB
"""
import os
import sys
from typing import List, Dict
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path so we can import core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import load_config, ConfigError
from core.services.ynab_service import YNABService, Payee

class PayeeCleanup:
    """Class to handle cleanup of unused payees in YNAB."""
    
    def __init__(self, ynab_service: YNABService):
        """Initialize with YNAB service."""
        self.ynab_service = ynab_service
        self.deleted_count = 0
        self.skipped_count = 0
    
    def get_unused_payees(self) -> List[Payee]:
        """
        Get list of payees that have no associated transactions.
        
        Returns:
            List[Payee]: List of unused payee objects
        """
        # Get all payees
        all_payees = self.ynab_service.get_payees()
        
        # Get all transactions
        transactions = self.ynab_service.get_transactions()
        
        # Create a set of payee IDs that are used in transactions
        used_payee_ids = {t.payee_id for t in transactions if t.payee_id}
        
        # Filter payees that aren't in the used set and aren't deleted
        # Also exclude payees that start with "Transfer"
        unused_payees = [
            p for p in all_payees 
            if p.id not in used_payee_ids 
            and not p.deleted 
            and p.name.strip()
            and not p.name.strip().startswith("Transfer")
        ]
        
        return unused_payees
    
    def delete_payee(self, payee: Payee, dry_run: bool = False) -> bool:
        """
        Delete a payee from YNAB.
        
        Args:
            payee: Payee object to delete
            dry_run: If True, don't actually delete, just simulate
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        if dry_run:
            print(f"Would delete payee: {payee.name}")
            return True
            
        success = self.ynab_service.delete_payee(payee.id)
        if success:
            print(f"✅ Deleted payee: {payee.name}")
        else:
            print(f"❌ Failed to delete payee: {payee.name}")
        return success
    
    def cleanup_payees(self, dry_run: bool = False, interactive: bool = False) -> Dict:
        """
        Find and delete unused payees.
        
        Args:
            dry_run: If True, don't actually delete, just show what would be deleted
            interactive: If True, prompt for confirmation before each deletion
            
        Returns:
            Dict: Statistics about the operation
        """
        print("🔍 Finding unused payees...")
        unused_payees = self.get_unused_payees()
        
        if not unused_payees:
            print("No unused payees found. Nothing to clean up.")
            return {
                "total_found": 0,
                "deleted": 0,
                "skipped": 0
            }
            
        print(f"Found {len(unused_payees)} unused payees")
        
        self.deleted_count = 0
        self.skipped_count = 0
        
        for payee in unused_payees:
            if interactive:
                choice = input(f"Delete '{payee.name}'? [y/n]: ").strip().lower()
                if choice != 'y':
                    print(f"Skipping payee: {payee.name}")
                    self.skipped_count += 1
                    continue
            
            if self.delete_payee(payee, dry_run):
                self.deleted_count += 1
            else:
                self.skipped_count += 1
        
        return {
            "total_found": len(unused_payees),
            "deleted": self.deleted_count,
            "skipped": self.skipped_count
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Clean up unused payees in YNAB')
    parser.add_argument('--dry-run', action='store_true', help='Simulate deletion without actually deleting')
    parser.add_argument('--interactive', action='store_true', help='Prompt for confirmation before each deletion')
    args = parser.parse_args()

    try:
        # Explicitly load the .env file from the current directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)
        
        # Load base configuration without project prefix
        config = load_config()
        
        # Create YNAB service
        ynab_service = YNABService(config.ynab_api_key, config.ynab_budget_id)
        
        # Create and run payee cleanup
        start_time = datetime.now()
        cleanup = PayeeCleanup(ynab_service)
        
        mode = "DRY RUN" if args.dry_run else "LIVE MODE"
        print(f"🧹 YNAB Payee Cleanup - {mode} 🧹")
        print("="*40)
        
        results = cleanup.cleanup_payees(
            dry_run=args.dry_run,
            interactive=args.interactive
        )
        
        print("\n" + "="*40)
        print(f"✨ Cleanup completed in {(datetime.now() - start_time).total_seconds():.2f} seconds")
        print(f"Total unused payees found: {results['total_found']}")
        print(f"Payees deleted: {results['deleted']}")
        print(f"Payees skipped: {results['skipped']}")
        
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())