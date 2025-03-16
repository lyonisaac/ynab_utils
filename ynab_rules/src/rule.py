"""
Defines the Rule class for the YNAB Rules Engine.

Rules combine conditions and actions to define automated transaction processing logic.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
import uuid

from .condition import Condition
from .action import Action


class RuleLogicOperator(str, Enum):
    """Logic operators for combining multiple conditions."""
    AND = "and"  # All conditions must be true
    OR = "or"    # At least one condition must be true


@dataclass
class Rule:
    """
    A rule consists of conditions and actions for automated transaction processing.
    
    When a transaction matches the conditions, the actions will be applied.
    """
    name: str
    description: str
    conditions: List[Condition]
    actions: List[Action]
    enabled: bool = True
    priority: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    logic_operator: RuleLogicOperator = RuleLogicOperator.AND
    
    def evaluate(self, transaction: Dict[str, Any]) -> bool:
        """
        Evaluate if the rule's conditions match the given transaction.
        
        Args:
            transaction: Transaction data to evaluate against
            
        Returns:
            bool: True if the conditions match, False otherwise
        """
        # If there are no conditions, the rule does not match
        if not self.conditions:
            return False
        
        # For AND logic, all conditions must evaluate to True
        if self.logic_operator == RuleLogicOperator.AND:
            return all(condition.evaluate(transaction) for condition in self.conditions)
        
        # For OR logic, at least one condition must evaluate to True
        return any(condition.evaluate(transaction) for condition in self.conditions)
    
    def apply(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply the rule's actions to the given transaction if conditions match.
        
        Args:
            transaction: Transaction data to potentially modify
            
        Returns:
            Dict[str, Any]: Modified transaction data if conditions match,
                           otherwise the original transaction
        """
        # Only apply actions if conditions match
        if not self.evaluate(transaction):
            return transaction
        
        # Apply each action in sequence
        modified_transaction = transaction.copy()
        for action in self.actions:
            modified_transaction = action.apply(modified_transaction)
        
        return modified_transaction
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the rule to a dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the rule
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "conditions": [condition.to_dict() for condition in self.conditions],
            "actions": [action.to_dict() for action in self.actions],
            "enabled": self.enabled,
            "priority": self.priority,
            "logic_operator": self.logic_operator
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        """
        Create a Rule instance from a dictionary.
        
        Args:
            data: Dictionary containing rule data
            
        Returns:
            Rule: New Rule instance
        """
        conditions = [Condition.from_dict(c) for c in data["conditions"]]
        actions = [Action.from_dict(a) for a in data["actions"]]
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            description=data["description"],
            conditions=conditions,
            actions=actions,
            enabled=data.get("enabled", True),
            priority=data.get("priority", 0),
            logic_operator=data.get("logic_operator", RuleLogicOperator.AND)
        )