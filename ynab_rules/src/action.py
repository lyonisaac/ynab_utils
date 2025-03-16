"""
Defines the Action class for the YNAB Rules Engine.

Actions specify the modifications to apply to transactions that match conditions.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class ActionField(str, Enum):
    """Fields of a transaction that can be modified by actions."""
    PAYEE_NAME = "payee_name"
    CATEGORY_NAME = "category_name" 
    MEMO = "memo"


class ActionOperation(str, Enum):
    """Operations that can be performed on transaction fields."""
    SET = "set"
    APPEND = "append"
    PREPEND = "prepend"
    CLEAR = "clear"


@dataclass
class Action:
    """
    An action defines a modification to apply to a transaction.
    
    An action consists of a field (what to modify), an operation (how to modify),
    and a value (what to apply).
    """
    field: ActionField
    operation: ActionOperation
    value: str = ""  # Empty string for CLEAR operation
    
    def apply(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply the action to the given transaction.
        
        Args:
            transaction: Transaction data to modify
            
        Returns:
            Dict[str, Any]: Modified transaction data
        """
        # Make a copy to avoid modifying the original
        modified_transaction = transaction.copy()
        
        # Get the current value (default to empty string if not present)
        current_value = str(modified_transaction.get(self.field, ""))
        
        # Apply the operation
        if self.operation == ActionOperation.SET:
            modified_transaction[self.field] = self.value
            
        elif self.operation == ActionOperation.APPEND:
            # Append value with a space if current value is not empty
            if current_value:
                modified_transaction[self.field] = f"{current_value} {self.value}"
            else:
                modified_transaction[self.field] = self.value
                
        elif self.operation == ActionOperation.PREPEND:
            # Prepend value with a space if current value is not empty
            if current_value:
                modified_transaction[self.field] = f"{self.value} {current_value}"
            else:
                modified_transaction[self.field] = self.value
                
        elif self.operation == ActionOperation.CLEAR:
            modified_transaction[self.field] = ""
        
        return modified_transaction
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the action to a dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the action
        """
        return {
            "field": self.field,
            "operation": self.operation,
            "value": self.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Action':
        """
        Create an Action instance from a dictionary.
        
        Args:
            data: Dictionary containing action data
            
        Returns:
            Action: New Action instance
        """
        return cls(
            field=data["field"],
            operation=data["operation"],
            value=data.get("value", "")  # Value might be optional for CLEAR operation
        )