# YNAB Payee Cleanup

## Overview

YNAB Payee Cleanup is a Python utility that helps you clean up unused payees in your You Need A Budget (YNAB) budget. It identifies payees with no associated transactions and properly deletes them from your budget, helping to keep your YNAB budget clean and organized.

## Features

- Identifies unused payees across your budget
- Properly deletes unused payees (sets deleted flag to true)
- Makes payees disappear from the YNAB UI
- Supports dry-run mode to preview potential deletions
- Interactive mode for manual review of each payee
- Skips system payees like transfers
- Provides detailed statistics about the cleanup process

## Prerequisites

- Python 3.7+
- YNAB API key
- A YNAB budget

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root
2. Add your YNAB credentials:
   ```
   YNAB_API_KEY=your_ynab_api_key
   YNAB_BUDGET_ID=your_budget_id
   ```

## Usage

### Basic Usage
```bash
python -m ynab_payee_cleanup
```

### Command-line Options
- `--dry-run`: Simulate deletion without modifying data
- `--interactive`: Prompt for confirmation before deleting each payee

### Examples
```bash
# Preview payees that would be deleted
python -m ynab_payee_cleanup --dry-run

# Interactively review and delete unused payees
python -m ynab_payee_cleanup --interactive
```

## How It Works

1. Retrieves all payees from your YNAB budget
2. Fetches all transactions
3. Identifies payees with no associated transactions
4. Sets the `deleted` flag to `true` for these payees
5. Provides a summary of the cleanup process

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit
- NonCommercial — You may not use the material for commercial purposes

Full license details: https://creativecommons.org/licenses/by-nc/4.0/

## Disclaimer

This tool interacts with your YNAB budget. Always use the `--dry-run` option first and review the potential changes carefully.