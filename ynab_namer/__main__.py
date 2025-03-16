# Try one of these import statements:
try:
    # If main.py is in the same directory as __main__.py
    from .main import main
except ImportError:
    try:
        # Alternative import if the above fails
        from ynab_namer.main import main
    except ImportError:
        # Direct import as last resort
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from main import main

if __name__ == "__main__":
    main()