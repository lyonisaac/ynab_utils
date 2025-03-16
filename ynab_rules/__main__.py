"""
Main entry point for the YNAB Rules Engine when run as a module.

Execute with: python -m ynab_rules
"""
import sys
import argparse
import logging
from pathlib import Path

from ynab_rules.src.app import App

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the YNAB Rules Engine."""
    parser = argparse.ArgumentParser(description='YNAB Rules Engine')
    
    parser.add_argument(
        '--config-dir',
        help='Directory for configuration and rule storage',
        default=None
    )
    
    parser.add_argument(
        '--process',
        action='store_true',
        help='Process transactions using existing rules'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate processing without making changes'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize the application
        app = App(config_dir=args.config_dir)
        
        if args.process:
            # Process transactions
            results = app.process_transactions(dry_run=args.dry_run)
            
            # Print summary of results
            print(f"\nProcessed {results['total_transactions']} transactions")
            print(f"Modified: {results['modified_transactions']}")
            
            if results['modified_transactions'] > 0:
                print("\nRules applied:")
                for rule_name, count in results['rules_applied'].items():
                    print(f"- {rule_name}: {count} transaction(s)")
                
                if args.dry_run:
                    print("\nThis was a dry run. No changes were applied.")
                else:
                    print(f"\nApplied {results.get('changes_applied', 0)} changes to YNAB.")
        else:
            # Start interactive CLI
            app.run_cli()
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()