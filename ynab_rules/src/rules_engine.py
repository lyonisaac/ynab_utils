"""
Rules Engine for processing YNAB transactions using defined rules.

The Rules Engine applies rules to transactions based on priority and handles
the batch processing of transaction updates.
"""
from typing import Dict, List, Any, Optional, Tuple
import logging
from collections import defaultdict

from .rule import Rule
from .storage import RuleStorage


class RulesEngine:
    """
    Engine for applying rules to YNAB transactions.
    
    Processes transactions through rules and generates modifications.
    """
    
    def __init__(self, storage: RuleStorage):
        """
        Initialize the Rules Engine.
        
        Args:
            storage: Storage provider for rules
        """
        self.storage = storage
        self.logger = logging.getLogger(__name__)
    
    def load_rules(self) -> List[Rule]:
        """
        Load all rules from storage.
        
        Returns:
            List[Rule]: List of rules sorted by priority (highest first)
        """
        rules = self.storage.get_all_rules()
        # Sort rules by priority (highest to lowest)
        return sorted(rules, key=lambda r: r.priority, reverse=True)
    
    def process_transaction(self, transaction: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """
        Process a single transaction through all enabled rules.
        
        Args:
            transaction: Transaction data to process
            
        Returns:
            Tuple[Dict[str, Any], List[str]]: Modified transaction and list of applied rule names
        """
        rules = self.load_rules()
        modified_transaction = transaction.copy()
        applied_rules = []
        
        # Apply each enabled rule in priority order
        for rule in rules:
            if not rule.enabled:
                continue
                
            # Check if the rule's conditions match
            if rule.evaluate(modified_transaction):
                # Apply the rule's actions
                before_transaction = modified_transaction.copy()
                modified_transaction = rule.apply(modified_transaction)
                
                # If the transaction was modified, record the rule
                if modified_transaction != before_transaction:
                    applied_rules.append(rule.name)
                    self.logger.info(f"Applied rule '{rule.name}' to transaction")
        
        return modified_transaction, applied_rules
    
    def process_transactions(
        self, 
        transactions: List[Dict[str, Any]], 
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Process multiple transactions through the rules engine.
        
        Args:
            transactions: List of transactions to process
            dry_run: If True, generate a report without making actual changes
            
        Returns:
            Dict[str, Any]: Report of changes made or that would be made
        """
        results = {
            "total_transactions": len(transactions),
            "modified_transactions": 0,
            "rules_applied": defaultdict(int),
            "modifications": [],
            "dry_run": dry_run
        }
        
        for transaction in transactions:
            original = transaction.copy()
            modified, applied_rules = self.process_transaction(transaction)
            
            # Record the modifications if any rules were applied
            if applied_rules:
                results["modified_transactions"] += 1
                
                # Count rule applications
                for rule_name in applied_rules:
                    results["rules_applied"][rule_name] += 1
                
                # Record the specific changes
                changes = self._get_transaction_changes(original, modified)
                if changes:
                    results["modifications"].append({
                        "transaction_id": transaction.get("id", "unknown"),
                        "payee_name": transaction.get("payee_name", "unknown"),
                        "applied_rules": applied_rules,
                        "changes": changes
                    })
        
        # Convert defaultdict to regular dict for easier serialization
        results["rules_applied"] = dict(results["rules_applied"])
        return results
    
    def _get_transaction_changes(
        self, 
        original: Dict[str, Any], 
        modified: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify the fields that changed between original and modified transactions.
        
        Args:
            original: Original transaction data
            modified: Modified transaction data
            
        Returns:
            List[Dict[str, Any]]: List of changes with field, old value, and new value
        """
        changes = []
        
        # Check all keys in the modified transaction
        for key in modified:
            # If the key exists in both and values differ
            if key in original and original[key] != modified[key]:
                changes.append({
                    "field": key,
                    "old_value": original[key],
                    "new_value": modified[key]
                })
            # If the key only exists in the modified transaction
            elif key not in original:
                changes.append({
                    "field": key,
                    "old_value": None,
                    "new_value": modified[key]
                })
        
        # Check for keys that were removed
        for key in original:
            if key not in modified:
                changes.append({
                    "field": key,
                    "old_value": original[key],
                    "new_value": None
                })
        
        return changes