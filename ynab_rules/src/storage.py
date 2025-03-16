"""
Storage implementation for persisting rules to disk.

Provides functionality for saving, loading, and managing rules in a JSON file.
"""
import json
import os
from typing import Dict, List, Any, Optional
import logging

from .rule import Rule


class RuleStorage:
    """
    Storage provider for rules persistence.
    
    Handles saving and loading rules from disk using JSON serialization.
    """
    
    def __init__(self, storage_path: str):
        """
        Initialize the rule storage.
        
        Args:
            storage_path: Path to the rules storage file
        """
        self.storage_path = storage_path
        self.logger = logging.getLogger(__name__)
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(storage_path)), exist_ok=True)
    
    def get_all_rules(self) -> List[Rule]:
        """
        Load all rules from storage.
        
        Returns:
            List[Rule]: List of all stored rules
        """
        rules_data = self._load_storage()
        return [Rule.from_dict(rule_data) for rule_data in rules_data]
    
    def get_rule_by_id(self, rule_id: str) -> Optional[Rule]:
        """
        Get a specific rule by ID.
        
        Args:
            rule_id: ID of the rule to retrieve
            
        Returns:
            Optional[Rule]: The rule if found, None otherwise
        """
        rules_data = self._load_storage()
        
        for rule_data in rules_data:
            if rule_data.get("id") == rule_id:
                return Rule.from_dict(rule_data)
        
        return None
    
    def save_rule(self, rule: Rule) -> bool:
        """
        Save a rule to storage.
        
        If a rule with the same ID already exists, it will be updated.
        Otherwise, a new rule will be added.
        
        Args:
            rule: The rule to save
            
        Returns:
            bool: True if the operation was successful, False otherwise
        """
        try:
            rules_data = self._load_storage()
            
            # Check if rule already exists
            updated = False
            for i, existing_rule in enumerate(rules_data):
                if existing_rule.get("id") == rule.id:
                    # Update existing rule
                    rules_data[i] = rule.to_dict()
                    updated = True
                    break
            
            # If not updated, add as new rule
            if not updated:
                rules_data.append(rule.to_dict())
            
            # Save to disk
            self._save_storage(rules_data)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save rule: {e}")
            return False
    
    def delete_rule(self, rule_id: str) -> bool:
        """
        Delete a rule from storage.
        
        Args:
            rule_id: ID of the rule to delete
            
        Returns:
            bool: True if the rule was deleted, False otherwise
        """
        try:
            rules_data = self._load_storage()
            
            # Filter out the rule to delete
            initial_count = len(rules_data)
            rules_data = [r for r in rules_data if r.get("id") != rule_id]
            
            # Only save if a rule was actually removed
            if len(rules_data) < initial_count:
                self._save_storage(rules_data)
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to delete rule: {e}")
            return False
    
    def _load_storage(self) -> List[Dict[str, Any]]:
        """
        Load rules data from the storage file.
        
        Returns:
            List[Dict[str, Any]]: List of rule data dictionaries
        """
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            else:
                # Return empty list if file doesn't exist yet
                return []
        except Exception as e:
            self.logger.error(f"Error loading rules from storage: {e}")
            # Return empty list on error
            return []
    
    def _save_storage(self, rules_data: List[Dict[str, Any]]) -> None:
        """
        Save rules data to the storage file.
        
        Args:
            rules_data: List of rule data dictionaries to save
        """
        with open(self.storage_path, 'w') as f:
            json.dump(rules_data, f, indent=2)