"""
Defines the Condition class for the YNAB Rules Engine.

Conditions are used to evaluate if a transaction meets specific criteria.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class ConditionField(str, Enum):
    """Fields of a transaction that can be used in conditions."""
    PAYEE_NAME = "payee_name"
    ACCOUNT_NAME = "account_name"
    OUTFLOW = "outflow"
    INFLOW = "inflow"
    MEMO = "memo"
    CATEGORY_NAME = "category_name"


class ConditionOperator(str, Enum):
    """Operators used to compare values in conditions."""
    EQUALS = "equals"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    REGEX = "regex"


@dataclass
class Condition:
    """
    A condition defines a criterion for matching transactions.
    
    A condition consists of a field (what to check), an operator (how to compare),
    and a value (what to compare against).
    """
    field: ConditionField
    operator: ConditionOperator
    value: Any
    
    def evaluate(self, transaction: Dict[str, Any]) -> bool:
        """
        Evaluate if the condition is met for the given transaction.
        
        Args:
            transaction: Transaction data to evaluate against
            
        Returns:
            bool: True if the condition is met, False otherwise
        """
        # Get the value from the transaction based on the field
        transaction_value = transaction.get(self.field)
        
        # If the transaction doesn't have the field, condition fails
        if transaction_value is None:
            return False
        
        # Perform comparison based on the operator
        if self.operator == ConditionOperator.EQUALS:
            return str(transaction_value).lower() == str(self.value).lower()
            
        elif self.operator == ConditionOperator.CONTAINS:
            return str(self.value).lower() in str(transaction_value).lower()
            
        elif self.operator == ConditionOperator.STARTS_WITH:
            return str(transaction_value).lower().startswith(str(self.value).lower())
            
        elif self.operator == ConditionOperator.ENDS_WITH:
            return str(transaction_value).lower().endswith(str(self.value).lower())
            
        elif self.operator == ConditionOperator.GREATER_THAN:
            # For numeric comparisons
            try:
                return float(transaction_value) > float(self.value)
            except (ValueError, TypeError):
                return False
                
        elif self.operator == ConditionOperator.LESS_THAN:
            # For numeric comparisons
            try:
                return float(transaction_value) < float(self.value)
            except (ValueError, TypeError):
                return False
                
        elif self.operator == ConditionOperator.REGEX:
            # For regex pattern matching
            import re
            try:
                pattern = re.compile(self.value, re.IGNORECASE)
                return bool(pattern.search(str(transaction_value)))
            except re.error:
                return False
                
        # Default case if operator is not recognized
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the condition to a dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the condition
        """
        return {
            "field": self.field,
            "operator": self.operator,
            "value": self.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Condition':
        """
        Create a Condition instance from a dictionary.
        
        Args:
            data: Dictionary containing condition data
            
        Returns:
            Condition: New Condition instance
        """
        return cls(
            field=data["field"],
            operator=data["operator"],
            value=data["value"]
        )