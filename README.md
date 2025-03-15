# YNAB Tools

## Overview

A collection of Python utilities for managing and improving your You Need A Budget (YNAB) experience.

## Projects

### 1. YNAB Emoji Namer

Automatically adds emojis to your YNAB payees, making your budget more visually engaging and easier to navigate.

#### Features
- Identifies payees without emojis
- Uses AI to suggest appropriate emojis
- Interactive approval process
- Ignore specific payees

#### Prerequisites
- Python 3.7+
- YNAB API key
- Groq API key (or alternative LLM provider)

#### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your credentials
4. Run: `python -m ynab_namer`

### 2. YNAB Payee Cleanup

Helps clean up unused payees in your YNAB budget by identifying and marking payees with no associated transactions.

#### Features
- Identifies unused payees
- Supports dry-run mode
- Interactive review option
- Skips system payees

#### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your credentials
4. Run: `python -m ynab_payee_cleanup`

### 3. YNAB Duplicate Payee Cleanup

Identifies and merges duplicate payees in your YNAB budget by comparing names after removing whitespace and emojis.

#### Features
- Identifies payees that are duplicates based on normalized names
- Prioritizes keeping payees that already have emojis
- Merges all transactions from duplicate payees to the selected target
- Supports dry-run mode for previewing changes

#### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your credentials
4. Run: `python -m ynab_duplicate_payee_cleanup`

## Configuration

For all tools, create a `.env` file with:
```
YNAB_API_KEY=your_ynab_api_key
YNAB_BUDGET_ID=your_budget_id
GROQ_API_KEY=your_groq_api_key
```

Tool-specific configuration:
```
# For YNAB Duplicate Payee Cleanup
YNAB_DUPLICATE_CLEANUP_DRY_RUN=true
```

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

These tools interact with your YNAB budget. Always review changes carefully and use dry-run modes when available.