"""
YNAB Duplicate Payee Cleanup - Core application
"""
import re
from typing import Dict, List, Tuple, Set, Optional
from core.config import BaseConfig
from core.services.ynab_service import Payee, Transaction

from core.services.ynab_service import YNABService
from core.utils.text_utils import has_emoji, strip_emoji

class DuplicatePayeeCleanup:
    """
    Identifies and merges duplicate payees in YNAB by comparing names 
    without whitespace and emojis
    """
    
    def __init__(self, config: BaseConfig, dry_run: bool = True):
        """Initialize the duplicate payee cleanup tool.
        
        Args:
            config: Configuration object
            dry_run: If True, don't make any actual changes to YNAB
        """
        self.ynab_service = YNABService(
            api_key=config.ynab_api_key,
            budget_id=config.ynab_budget_id
        )
        self.dry_run = dry_run
        
    def _normalize_payee_name(self, name: str) -> str:
        """Normalize a payee name by removing whitespace and emojis.
        
        Args:
            name: The original payee name
            
        Returns:
            Normalized name (lowercase, no whitespace, no emojis)
        """
        # Strip emojis
        name = strip_emoji(name)
        # Remove whitespace
        name = re.sub(r'\s+', '', name)
        # Convert to lowercase
        return name.lower()
    
    def _find_duplicate_payees(self) -> Dict[str, List[Payee]]:
        """Find duplicate payees based on normalized names.
        
        Returns:
            Dictionary mapping normalized names to lists of payee objects
            that have the same normalized name
        """
        payees = self.ynab_service.get_payees()
        duplicates = {}
        
        # Group payees by normalized name
        for payee in payees:
            # Skip deleted payees
            if payee.deleted:
                continue
                
            normalized_name = self._normalize_payee_name(payee.name)
            if normalized_name:
                if normalized_name not in duplicates:
                    duplicates[normalized_name] = []
                duplicates[normalized_name].append(payee)
        
        # Keep only groups with more than one payee
        return {k: v for k, v in duplicates.items() if len(v) > 1}
    
    def _select_target_payee(self, duplicates: List[Payee]) -> Payee:
        """Select which payee to keep when merging duplicates.
        Prioritizes payees with emojis over those without.
        
        Args:
            duplicates: List of duplicate payee objects
            
        Returns:
            The payee to keep (target for merging)
        """
        # First, try to find a payee with an emoji
        for payee in duplicates:
            if has_emoji(payee.name):
                return payee
        
        # If no payee has an emoji, use the first one
        return duplicates[0]
    
    def _merge_payees(self, target_payee: Payee, duplicates: List[Payee]) -> int:
        """Merge duplicate payees by reassigning transactions and deleting duplicates.
        
        Args:
            target_payee: The payee to keep
            duplicates: List of all duplicate payees (including target)
            
        Returns:
            Number of payees that were merged
        """
        count = 0
        target_id = target_payee.id
        
        # Process each duplicate except the target
        for payee in duplicates:
            if payee.id == target_id:
                continue
            
            # Get all transactions for this payee
            transactions = self.ynab_service.get_transactions_by_payee_id(payee.id)
            
            if not self.dry_run:
                # Update each transaction to use the target payee
                for transaction in transactions:
                    self.ynab_service.update_transaction(
                        transaction_id=transaction.id,
                        payee_id=target_id
                    )
                
                # Delete the duplicate payee (set deleted flag)
                self.ynab_service.update_payee(
                    payee_id=payee.id,
                    deleted=True
                )
            
            count += 1
            print(f"Payee: {payee.name} → {target_payee.name} ({len(transactions)} transactions)")
        
        return count
    
    def run(self) -> None:
        """Run the duplicate payee cleanup process."""
        print(f"YNAB Duplicate Payee Cleanup {'(DRY RUN)' if self.dry_run else ''}")
        print("=" * 60)
        
        # Find duplicate payees
        duplicate_groups = self._find_duplicate_payees()
        
        if not duplicate_groups:
            print("No duplicate payees found!")
            return
        
        print(f"Found {len(duplicate_groups)} groups of duplicate payees:")
        print()
        
        total_merged = 0
        
        # Process each group of duplicates
        for norm_name, duplicates in duplicate_groups.items():
            print(f"Group '{norm_name}' ({len(duplicates)} payees):")
            
            # Display all duplicates in the group
            for idx, payee in enumerate(duplicates, 1):
                print(f"  {idx}. {payee.name}")
            
            # Select which payee to keep
            target_payee = self._select_target_payee(duplicates)
            print(f"  → Keeping: {target_payee.name}")
            
            # Merge the payees
            merged_count = self._merge_payees(target_payee, duplicates)
            total_merged += merged_count
            print()
        
        print(f"Complete! {total_merged} payees {'would be' if self.dry_run else 'were'} merged.")
        
        if self.dry_run:
            print("\nThis was a dry run. No changes were made to your YNAB budget.")
            print("To perform actual changes, set YNAB_DUPLICATE_CLEANUP_DRY_RUN=false in your .env file.")