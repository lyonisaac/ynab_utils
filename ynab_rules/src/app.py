"""
Main application for the YNAB Rules Engine.

Ties together the CLI, rules engine, and YNAB service.
"""
import os
import sys
import logging
from typing import Dict, List, Any, Optional, Tuple
import json
from pathlib import Path
from dotenv import load_dotenv

from core.services.ynab_service import YNABService, Transaction
from .rules_engine import RulesEngine
from .storage import RuleStorage
from .cli import YNABRulesCLI


class App:
    """
    Main application for the YNAB Rules Engine.
    
    Acts as a facade for the various components of the application.
    """
    
    def __init__(self, config_dir: str = None):
        """
        Initialize the application.
        
        Args:
            config_dir: Directory for configuration and rule storage
        """
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Set up configuration directory
        if config_dir is None:
            home_dir = Path.home()
            self.config_dir = os.path.join(home_dir, '.ynab_rules')
        else:
            self.config_dir = config_dir
            
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Initialize components
        self.rules_file = os.path.join(self.config_dir, 'rules.json')
        self.storage = RuleStorage(self.rules_file)
        self.rules_engine = RulesEngine(self.storage)
        
        # Initialize YNAB service if credentials are available
        self.ynab_service = None
        self._init_ynab_service()
    
    def run_cli(self):
        """Run the command-line interface."""
        cli = YNABRulesCLI(config_dir=self.config_dir)
        cli.run()
    
    def process_transactions(self, dry_run: bool = True) -> Dict[str, Any]:
        """
        Process transactions using the rules engine.
        
        Args:
            dry_run: If True, simulate changes without applying them
            
        Returns:
            Dict[str, Any]: Report of changes made or that would be made
        """
        if not self.ynab_service:
            raise RuntimeError("YNAB service not initialized. Please check your API credentials.")
        
        # Get all transactions from YNAB
        transactions = self._get_transaction_data()
        
        # Process transactions through rules engine
        results = self.rules_engine.process_transactions(transactions, dry_run=dry_run)
        
        # If not a dry run, apply the changes
        if not dry_run:
            applied_changes = self._apply_transaction_changes(results)
            results["changes_applied"] = applied_changes
        
        return results
    
    def _init_ynab_service(self):
        """Initialize the YNAB service with credentials from environment variables."""
        api_key = os.environ.get('YNAB_API_KEY')
        budget_id = os.environ.get('YNAB_BUDGET_ID')
        
        if api_key and budget_id:
            try:
                self.ynab_service = YNABService(api_key, budget_id)
                self.logger.info("YNAB service initialized successfully.")
            except Exception as e:
                self.logger.error(f"Failed to initialize YNAB service: {e}")
        else:
            self.logger.warning("YNAB credentials not found. Set YNAB_API_KEY and YNAB_BUDGET_ID environment variables.")
    
    def _get_transaction_data(self) -> List[Dict[str, Any]]:
        """
        Get transaction data from YNAB.
        
        Returns:
            List[Dict[str, Any]]: List of transaction data dictionaries
        """
        # Get raw transactions from the YNAB API
        raw_transactions = self.ynab_service.get_transactions()
        
        # Transform into the format expected by the rules engine
        transactions = []
        
        for transaction in raw_transactions:
            # TODO: Enhance this to include category name, account name, etc.
            # For now, we'll create a simple dictionary with the transaction ID
            transactions.append({
                "id": transaction.id,
                "payee_id": transaction.payee_id,
                # Additional fields would be added here
            })
        
        return transactions
    
    def _apply_transaction_changes(self, results: Dict[str, Any]) -> int:
        """
        Apply transaction changes to YNAB.
        
        Args:
            results: Results from the rules engine
            
        Returns:
            int: Number of changes successfully applied
        """
        applied_count = 0
        
        # Loop through the modifications
        for mod in results.get("modifications", []):
            transaction_id = mod.get("transaction_id")
            
            # Apply each change
            for change in mod.get("changes", []):
                field = change.get("field")
                new_value = change.get("new_value")
                
                # TODO: Implement actual API calls to update transactions
                # For now, we'll just log the changes
                self.logger.info(f"Would update transaction {transaction_id}: {field} = {new_value}")
                applied_count += 1
        
        return applied_count


def main():
    """Main entry point for the application."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run the application
    app = App()
    app.run_cli()


if __name__ == "__main__":
    main()