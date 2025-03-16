# YNAB Duplicate Payee Cleanup

## Overview

This tool identifies and merges duplicate payees in your YNAB budget by comparing names after removing whitespace and emojis. It helps keep your budget organized by consolidating multiple versions of the same payee into a single entity.

## Features

- Identifies payees that are duplicates based on normalized names (ignoring whitespace, case, and emojis)
- Prioritizes keeping payees that already have emojis
- Merges all transactions from duplicate payees to the selected target payee
- Marks merged payees as deleted in YNAB
- Supports dry-run mode for previewing changes without modifying your budget
- Interactive mode that lets you approve each group of duplicates before merging

## Usage

1. Create a `.env` file with your YNAB credentials:
```
YNAB_API_KEY=your_ynab_api_key
YNAB_BUDGET_ID=your_budget_id
```

2. Run the tool:
```
python -m ynab_duplicate_payee_cleanup
```

### Command-line Options

- `--dry-run`: Simulate merging without actually modifying data (default behavior)
- `--interactive`: Prompt for confirmation before merging each group of duplicates

### Examples

```bash
# Preview all potential changes without modifying anything
python -m ynab_duplicate_payee_cleanup --dry-run

# Interactively review and approve each group of duplicates before merging
python -m ynab_duplicate_payee_cleanup --interactive

# Interactively review in dry-run mode (no changes will be made)
python -m ynab_duplicate_payee_cleanup --dry-run --interactive

# Perform actual merges without prompting
python -m ynab_duplicate_payee_cleanup
```

You can also control the dry-run behavior through the `.env` file:
```
YNAB_DUPLICATE_CLEANUP_DRY_RUN=false
```

## How It Works

1. The tool fetches all payees from your YNAB budget
2. For each payee, it creates a normalized version of the name by:
   - Removing all emojis
   - Removing all whitespace
   - Converting to lowercase
3. Payees with the same normalized name are grouped together
4. For each group, a target payee is selected (prioritizing payees that already have emojis)
5. All transactions from duplicate payees are reassigned to the target payee
6. Duplicate payees are marked as deleted in YNAB

## Example

Given these payees:
- "🏠 Walmart"
- "Walmart "
- "walmart"

The tool will:
1. Identify all three as duplicates (normalized name: "walmart")
2. Select "🏠 Walmart" as the target payee (because it has an emoji)
3. Move all transactions from "Walmart " and "walmart" to "🏠 Walmart"
4. Mark "Walmart " and "walmart" as deleted

## Interactive Mode

In interactive mode, for each group of duplicates you'll be prompted with:
- List of all payees in the duplicate group
- The automatically selected target payee (which will be kept)
- Options to:
  - Accept (y): Merge the duplicates
  - Reject (n): Skip this group and continue to the next
  - Quit (q): Exit the program

## Disclaimer

Always run the tool in dry-run mode first to review the proposed changes before applying them to your budget.