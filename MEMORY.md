# Project Overview

This repository contains a collection of Python utilities for enhancing the You Need A Budget (YNAB) experience through automation. The codebase follows a domain-driven design with a shared core module and separate tool implementations.

## Repository Structure

```
Copy.
├── core/                      # Shared functionality
│   ├── services/              # API integrations 
│   │   ├── ynab_service.py    # YNAB API client
│   │   └── llm_service.py     # LLM service abstraction
│   └── utils/                 # Utility functions
│       └── text_utils.py      # Text processing helpers
├── ynab_payee_cleanup/        # Payee cleanup tool
├── ynab_namer/                # Emoji naming tool
├── ynab_duplicate_payee_cleanup/  # Duplicate payee cleanup tool
├── setup.py                   # Core package setup
└── requirements.txt           # Project dependencies
```

## Tools

### YNAB Payee Cleanup (v1.0.0)

Identifies and properly deletes unused payees by setting the deleted flag to true

**Features:**
- Dry-run mode for previewing changes
- Interactive confirmation
- Skip logic for system payees

### YNAB Emoji Namer (v1.0.0)

Adds emojis to payee names using AI suggestions

**Features:**
- AI-powered emoji suggestions via Groq API
- Interactive approval process
- Persistent ignored payees list

### YNAB Duplicate Payee Cleanup (v1.0.0)

Identifies and merges duplicate payees based on normalized names (removing whitespace and emojis)

**Features:**
- Identifies duplicate payees by comparing normalized names
- Prioritizes keeping payees that already have emojis
- Reassigns transactions from duplicates to a target payee
- Supports dry-run mode for safe testing

## Core Components

### Services

- **YNABService:** Handles YNAB API interactions (payees, transactions)
- **LLMService:** Abstract base class for LLM providers
    - Current implementation: GroqService

### Configuration

- Environment-based configuration with dotenv support
- Shared configuration structure for all tools

## Recent Progress

- Implemented base functionality for both tools
- Established shared core library for code reuse
- Added LLM integration with Groq for emoji suggestions
- Improved YNAB Payee Cleanup to properly delete unused payees
- Added YNAB Duplicate Payee Cleanup to consolidate duplicate payees

## Current Challenges

- Limited LLM provider options (currently only Groq)
- No batch processing mode for emoji naming
- No testing infrastructure implemented yet

## Next Steps

- Add unit and integration tests
- Implement additional LLM providers (OpenAI, Anthropic)
- Add batch mode for emoji namer
- Create a unified CLI interface for all tools
- Consider refactoring to use async/await for API calls
- Add logging functionality

## Dependencies

- Python 3.7+
- requests: API communication
- python-dotenv: Environment configuration
- groq: LLM integration
