"""
Command Line Interface for the YNAB Rules Engine.

Provides interactive commands for managing rules and processing transactions.
"""
import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional, Tuple, Callable
import argparse
from pathlib import Path
from enum import Enum

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.validation import Validator, ValidationError
except ImportError:
    print("prompt_toolkit is required for the CLI. Install with: pip install prompt-toolkit")
    sys.exit(1)

from .rule import Rule, RuleLogicOperator
from .condition import Condition, ConditionField, ConditionOperator
from .action import Action, ActionField, ActionOperation
from .rules_engine import RulesEngine
from .storage import RuleStorage


class CLIMode(Enum):
    """Modes for the CLI interface."""
    MAIN = "main"
    CREATE_RULE = "create_rule"
    EDIT_RULE = "edit_rule"
    DELETE_RULE = "delete_rule"
    LIST_RULES = "list_rules"
    PROCESS_TRANSACTIONS = "process_transactions"
    EXIT = "exit"


class YNABRulesCLI:
    """
    Command Line Interface for interacting with the YNAB Rules Engine.
    """

    def __init__(self, config_dir: str = None):
        """
        Initialize the CLI with the given configuration.
        
        Args:
            config_dir: Directory for configuration and rule storage
        """
        self.logger = logging.getLogger(__name__)
        
        # Set up config directory
        if config_dir is None:
            home_dir = Path.home()
            self.config_dir = os.path.join(home_dir, '.ynab_rules')
        else:
            self.config_dir = config_dir
            
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Initialize storage
        self.rules_file = os.path.join(self.config_dir, 'rules.json')
        self.storage = RuleStorage(self.rules_file)
        self.rules_engine = RulesEngine(self.storage)
        
        # Command handlers
        self.commands = {
            'create': self.create_rule,
            'edit': self.edit_rule,
            'delete': self.delete_rule,
            'list': self.list_rules,
            'process': self.process_transactions,
            'exit': self.exit_cli,
            'help': self.show_help
        }
        
        # For storing temporary rule data during creation/editing
        self.current_rule_data = {}
        
    def run(self):
        """Run the CLI interface."""
        self._print_welcome()
        
        mode = CLIMode.MAIN
        current_rule = None
        
        while mode != CLIMode.EXIT:
            if mode == CLIMode.MAIN:
                command = self._prompt_command()
                
                if command in self.commands:
                    self.commands[command]()
                else:
                    print(f"Unknown command: {command}")
                    self.show_help()
            
            elif mode == CLIMode.CREATE_RULE:
                current_rule = self._create_rule_interactive()
                if current_rule:
                    self.storage.save_rule(current_rule)
                    print(f"Rule '{current_rule.name}' created successfully!")
                mode = CLIMode.MAIN
                
            elif mode == CLIMode.EDIT_RULE:
                rule_id = self._prompt_rule_selection()
                if rule_id:
                    current_rule = self.storage.get_rule_by_id(rule_id)
                    if current_rule:
                        updated_rule = self._edit_rule_interactive(current_rule)
                        if updated_rule:
                            self.storage.save_rule(updated_rule)
                            print(f"Rule '{updated_rule.name}' updated successfully!")
                    else:
                        print(f"Rule with ID {rule_id} not found.")
                mode = CLIMode.MAIN
                
            elif mode == CLIMode.DELETE_RULE:
                rule_id = self._prompt_rule_selection()
                if rule_id and self._confirm(f"Are you sure you want to delete this rule?"):
                    if self.storage.delete_rule(rule_id):
                        print("Rule deleted successfully!")
                    else:
                        print("Failed to delete rule.")
                mode = CLIMode.MAIN
    
    def create_rule(self):
        """Create a new rule interactively."""
        rule = self._create_rule_interactive()
        if rule:
            self.storage.save_rule(rule)
            print(f"Rule '{rule.name}' created successfully!")

    def edit_rule(self):
        """Edit an existing rule interactively."""
        rule_id = self._prompt_rule_selection()
        if rule_id:
            current_rule = self.storage.get_rule_by_id(rule_id)
            if current_rule:
                updated_rule = self._edit_rule_interactive(current_rule)
                if updated_rule:
                    self.storage.save_rule(updated_rule)
                    print(f"Rule '{updated_rule.name}' updated successfully!")
            else:
                print(f"Rule with ID {rule_id} not found.")
    
    def delete_rule(self):
        """Delete a rule interactively."""
        rule_id = self._prompt_rule_selection()
        if rule_id and self._confirm(f"Are you sure you want to delete this rule?"):
            if self.storage.delete_rule(rule_id):
                print("Rule deleted successfully!")
            else:
                print("Failed to delete rule.")
    
    def list_rules(self):
        """List all available rules."""
        rules = self.storage.get_all_rules()
        
        if not rules:
            print("No rules found.")
            return
            
        print("\nAvailable Rules:")
        print("-" * 60)
        for rule in sorted(rules, key=lambda r: r.priority, reverse=True):
            enabled_status = "✓" if rule.enabled else "✗"
            print(f"{enabled_status} [{rule.priority}] {rule.name}: {rule.description}")
            
            # Show conditions
            print("  Conditions:")
            if rule.conditions:
                for condition in rule.conditions:
                    print(f"    - {condition.field} {condition.operator} '{condition.value}'")
            else:
                print("    (No conditions)")
                
            # Show actions
            print("  Actions:")
            if rule.actions:
                for action in rule.actions:
                    print(f"    - {action.field} {action.operation} '{action.value}'")
            else:
                print("    (No actions)")
                
            print("-" * 60)
    
    def process_transactions(self):
        """Process transactions using the rules engine."""
        # In a real implementation, this would load transactions from YNAB
        # For now, we'll use a demo transaction for illustration
        print("\nProcessing transactions feature will be fully implemented with YNAB integration.")
        
        if self._confirm("Would you like to test with a sample transaction?"):
            # Create a sample transaction for testing
            sample_transaction = {
                "id": "sample-transaction-id",
                "payee_name": "Sample Payee",
                "account_name": "Checking Account",
                "outflow": 42.50,
                "inflow": 0,
                "memo": "",
                "category_name": "Uncategorized"
            }
            
            print("\nSample Transaction:")
            print(f"Payee: {sample_transaction['payee_name']}")
            print(f"Account: {sample_transaction['account_name']}")
            print(f"Amount: ${sample_transaction['outflow']}")
            print(f"Category: {sample_transaction['category_name']}")
            print(f"Memo: {sample_transaction['memo'] or '(empty)'}")
            
            # Process the transaction
            print("\nApplying rules...")
            modified, applied_rules = self.rules_engine.process_transaction(sample_transaction)
            
            if not applied_rules:
                print("No rules matched this transaction.")
            else:
                print(f"\nApplied {len(applied_rules)} rule(s):")
                for rule_name in applied_rules:
                    print(f"- {rule_name}")
                
                print("\nModified Transaction:")
                print(f"Payee: {modified['payee_name']}")
                print(f"Account: {modified['account_name']}")
                print(f"Amount: ${modified['outflow']}")
                print(f"Category: {modified['category_name']}")
                print(f"Memo: {modified['memo'] or '(empty)'}")
    
    def exit_cli(self):
        """Exit the CLI."""
        print("Goodbye!")
        sys.exit(0)
    
    def show_help(self):
        """Show help information."""
        print("\nAvailable commands:")
        print("  create  - Create a new rule")
        print("  edit    - Edit an existing rule")
        print("  delete  - Delete a rule")
        print("  list    - List all rules")
        print("  process - Process transactions using rules")
        print("  help    - Show this help information")
        print("  exit    - Exit the program")
    
    def _print_welcome(self):
        """Print welcome message."""
        print("\n========================================")
        print("       YNAB Rules Engine CLI")
        print("========================================")
        print("Type 'help' for available commands.")
        print("Rules storage path:", self.rules_file)
        print("========================================\n")
    
    def _prompt_command(self) -> str:
        """Prompt for a command."""
        command_completer = WordCompleter(list(self.commands.keys()))
        return prompt("\nEnter command: ", completer=command_completer).strip().lower()
    
    def _prompt_rule_selection(self) -> Optional[str]:
        """Prompt for rule selection."""
        rules = self.storage.get_all_rules()
        
        if not rules:
            print("No rules available.")
            return None
            
        print("\nAvailable Rules:")
        for i, rule in enumerate(rules, 1):
            enabled_status = "✓" if rule.enabled else "✗"
            print(f"{i}. {enabled_status} [{rule.priority}] {rule.name}")
        
        try:
            selection = int(prompt("Enter rule number (0 to cancel): "))
            if selection == 0:
                return None
            if 1 <= selection <= len(rules):
                return rules[selection-1].id
            else:
                print("Invalid selection.")
                return None
        except ValueError:
            print("Please enter a number.")
            return None
    
    def _create_rule_interactive(self) -> Optional[Rule]:
        """Create a rule interactively."""
        print("\nCreating a new rule:")
        
        # Get basic rule information
        name = self._prompt_with_validation("Rule name: ", lambda x: bool(x.strip()), 
                                           "Name cannot be empty")
        description = prompt("Description: ")
        priority = self._prompt_integer("Priority (higher numbers run first): ", default=0)
        enabled = self._confirm("Enable this rule?", default=True)
        
        # Get logic operator
        logic_options = [op.value for op in RuleLogicOperator]
        logic_completer = WordCompleter(logic_options)
        logic_operator = prompt(
            "Logic operator (and/or): ",
            completer=logic_completer,
            default=RuleLogicOperator.AND.value
        )
        
        # Create conditions
        conditions = []
        while self._confirm("Add a condition?"):
            condition = self._create_condition_interactive()
            if condition:
                conditions.append(condition)
        
        if not conditions:
            print("Warning: Rule has no conditions. It will not match any transactions.")
            if not self._confirm("Continue anyway?"):
                return None
        
        # Create actions
        actions = []
        while self._confirm("Add an action?"):
            action = self._create_action_interactive()
            if action:
                actions.append(action)
        
        if not actions:
            print("Warning: Rule has no actions. It will not modify transactions.")
            if not self._confirm("Continue anyway?"):
                return None
        
        # Create and return the rule
        return Rule(
            name=name,
            description=description,
            conditions=conditions,
            actions=actions,
            priority=priority,
            enabled=enabled,
            logic_operator=RuleLogicOperator(logic_operator)
        )
    
    def _edit_rule_interactive(self, rule: Rule) -> Optional[Rule]:
        """Edit a rule interactively."""
        print(f"\nEditing rule: {rule.name}")
        
        # Edit basic information
        name = prompt("Rule name: ", default=rule.name)
        description = prompt("Description: ", default=rule.description)
        priority = self._prompt_integer("Priority: ", default=rule.priority)
        enabled = self._confirm("Enable this rule?", default=rule.enabled)
        
        # Edit logic operator
        logic_options = [op.value for op in RuleLogicOperator]
        logic_completer = WordCompleter(logic_options)
        logic_operator = prompt(
            "Logic operator (and/or): ",
            completer=logic_completer,
            default=rule.logic_operator.value
        )
        
        # Edit conditions
        print("\nCurrent conditions:")
        if rule.conditions:
            for i, condition in enumerate(rule.conditions, 1):
                print(f"{i}. {condition.field} {condition.operator} '{condition.value}'")
        else:
            print("(No conditions)")
        
        conditions = rule.conditions.copy()
        while self._confirm("Edit conditions?"):
            action = prompt("Action (add/remove/quit): ").lower()
            
            if action == 'add':
                condition = self._create_condition_interactive()
                if condition:
                    conditions.append(condition)
            elif action == 'remove':
                if conditions:
                    try:
                        idx = int(prompt("Enter condition number to remove: "))
                        if 1 <= idx <= len(conditions):
                            removed = conditions.pop(idx - 1)
                            print(f"Removed: {removed.field} {removed.operator} '{removed.value}'")
                        else:
                            print("Invalid index.")
                    except ValueError:
                        print("Please enter a number.")
                else:
                    print("No conditions to remove.")
            elif action == 'quit':
                break
            else:
                print("Invalid action.")
        
        # Edit actions
        print("\nCurrent actions:")
        if rule.actions:
            for i, action in enumerate(rule.actions, 1):
                print(f"{i}. {action.field} {action.operation} '{action.value}'")
        else:
            print("(No actions)")
        
        actions = rule.actions.copy()
        while self._confirm("Edit actions?"):
            action = prompt("Action (add/remove/quit): ").lower()
            
            if action == 'add':
                act = self._create_action_interactive()
                if act:
                    actions.append(act)
            elif action == 'remove':
                if actions:
                    try:
                        idx = int(prompt("Enter action number to remove: "))
                        if 1 <= idx <= len(actions):
                            removed = actions.pop(idx - 1)
                            print(f"Removed: {removed.field} {removed.operation} '{removed.value}'")
                        else:
                            print("Invalid index.")
                    except ValueError:
                        print("Please enter a number.")
                else:
                    print("No actions to remove.")
            elif action == 'quit':
                break
            else:
                print("Invalid action.")
        
        # Validate the updated rule
        if not conditions:
            print("Warning: Rule has no conditions. It will not match any transactions.")
            if not self._confirm("Continue anyway?"):
                return None
                
        if not actions:
            print("Warning: Rule has no actions. It will not modify transactions.")
            if not self._confirm("Continue anyway?"):
                return None
        
        # Create and return the updated rule
        return Rule(
            id=rule.id,
            name=name,
            description=description,
            conditions=conditions,
            actions=actions,
            priority=priority,
            enabled=enabled,
            logic_operator=RuleLogicOperator(logic_operator)
        )
    
    def _create_condition_interactive(self) -> Optional[Condition]:
        """Create a condition interactively."""
        print("\nAdding a condition:")
        
        # Select field
        field_options = [f.value for f in ConditionField]
        field_completer = WordCompleter(field_options)
        field = prompt(
            "Field: ",
            completer=field_completer
        )
        
        if field not in field_options:
            print(f"Invalid field. Choose from: {', '.join(field_options)}")
            return None
        
        # Select operator
        operator_options = [op.value for op in ConditionOperator]
        operator_completer = WordCompleter(operator_options)
        operator = prompt(
            "Operator: ",
            completer=operator_completer
        )
        
        if operator not in operator_options:
            print(f"Invalid operator. Choose from: {', '.join(operator_options)}")
            return None
        
        # Enter value
        value = prompt("Value: ")
        
        return Condition(
            field=ConditionField(field),
            operator=ConditionOperator(operator),
            value=value
        )
    
    def _create_action_interactive(self) -> Optional[Action]:
        """Create an action interactively."""
        print("\nAdding an action:")
        
        # Select field
        field_options = [f.value for f in ActionField]
        field_completer = WordCompleter(field_options)
        field = prompt(
            "Field: ",
            completer=field_completer
        )
        
        if field not in field_options:
            print(f"Invalid field. Choose from: {', '.join(field_options)}")
            return None
        
        # Select operation
        operation_options = [op.value for op in ActionOperation]
        operation_completer = WordCompleter(operation_options)
        operation = prompt(
            "Operation: ",
            completer=operation_completer
        )
        
        if operation not in operation_options:
            print(f"Invalid operation. Choose from: {', '.join(operation_options)}")
            return None
        
        # Enter value (not required for CLEAR operation)
        value = ""
        if operation != ActionOperation.CLEAR.value:
            value = prompt("Value: ")
        
        return Action(
            field=ActionField(field),
            operation=ActionOperation(operation),
            value=value
        )
    
    def _prompt_with_validation(
        self, 
        message: str, 
        validator_func: Callable[[str], bool], 
        error_message: str
    ) -> str:
        """Prompt for input with custom validation."""
        class CustomValidator(Validator):
            def validate(self, document):
                text = document.text
                if not validator_func(text):
                    raise ValidationError(
                        message=error_message,
                        cursor_position=len(text)
                    )
        
        return prompt(message, validator=CustomValidator())
    
    def _prompt_integer(self, message: str, default: int = 0) -> int:
        """Prompt for an integer value."""
        while True:
            try:
                value = prompt(message, default=str(default))
                return int(value)
            except ValueError:
                print("Please enter a valid number.")
    
    def _confirm(self, message: str, default: bool = False) -> bool:
        """Prompt for confirmation."""
        default_str = "Y/n" if default else "y/N"
        response = prompt(f"{message} [{default_str}]: ").lower()
        
        if not response:
            return default
        
        return response.startswith('y')


def main():
    """Main entry point for the CLI."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='YNAB Rules Engine')
    parser.add_argument(
        '--config-dir',
        help='Directory for configuration and rule storage',
        default=None
    )
    
    args = parser.parse_args()
    
    # Run the CLI
    cli = YNABRulesCLI(config_dir=args.config_dir)
    cli.run()


if __name__ == "__main__":
    main()