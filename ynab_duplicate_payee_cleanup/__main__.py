#!/usr/bin/env python3
"""
YNAB Duplicate Payee Cleanup - Package entry point
This file allows the package to be executed directly with python -m ynab_duplicate_payee_cleanup
"""

from .main import main

if __name__ == "__main__":
    exit(main())