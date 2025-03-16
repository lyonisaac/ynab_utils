# Project Overview

This repository contains a collection of Python utilities for enhancing the You Need A Budget (YNAB) experience through automation. The codebase follows a domain-driven design with a shared core module and separate tool implementations.

## Repository Structure

```
Copy.
├── core/                      # Shared functionality
│   ├── services/              # API integrations 
│   │   ├── ynab_service.py    # YNAB API client
│   │   ├── llm_service.py     # LLM service abstraction
│   │   └── validation_service.py  # New validation service
│   ├── models/                # Domain models (new)
│   │   └── transaction_models.py  # Transaction-related models
│   └── utils/                 # Utility functions
│       ├── text_utils.py      # Text processing helpers
│       └── validation_utils.py  # Input validation utilities (new)
├── ynab_payee_cleanup/        # Payee cleanup tool
├── ynab_namer/                # Emoji naming tool
├── ynab_duplicate_payee_cleanup/  # Duplicate payee cleanup tool
├── ynab_rules/                # Rules engine (new)
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   ├── .env
│   ├── README.md
│   └── src/
│       ├── __init__.py
│       ├── app.py             # Main application logic
│       ├── rules_engine.py    # Rules processing engine
│       ├── rule.py            # Rule definition and validation
│       ├── condition.py       # Condition components
│       ├── action.py          # Action components
│       ├── cli.py             # CLI interface with validation
│       └── storage.py         # Rule persistence
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

### YNAB Rules Engine (Proposed)

A flexible rules engine for automating transaction modifications based on user-defined conditions

**Features:**
- Define rules with conditions and actions
- Match transaction attributes (Payee, Account, Outflow, Inflow) 
- Modify transaction properties (Payee, Category, Memo)
- Interactive CLI with data validation and autocompletion
- Rule persistence and management
- Dry-run mode for testing rules
- Batch processing for transaction updates

#### Domain Model

```
Rule
├── name: str
├── description: str
├── conditions: List[Condition]
├── actions: List[Action]
├── enabled: bool
├── priority: int
└── methods:
    ├── evaluate(transaction) -> bool
    └── apply(transaction) -> Transaction

Condition
├── field: str (payee_name, account_name, outflow, inflow)
├── operator: str (equals, contains, starts_with, ends_with, greater_than, less_than)
├── value: Any
└── methods:
    └── evaluate(transaction) -> bool

Action
├── field: str (payee_name, category_name, memo)
├── operation: str (set, append, prepend)
├── value: str
└── methods:
    └── apply(transaction) -> Transaction
```

## Core Components

### Services

- **YNABService:** Handles YNAB API interactions (payees, transactions)
- **LLMService:** Abstract base class for LLM providers
    - Current implementation: GroqService
- **ValidationService:** New service for YNAB entity validation (payees, categories, accounts)

### Configuration

- Environment-based configuration with dotenv support
- Shared configuration structure for all tools

### Models (New)

- **TransactionModels:** Domain models for working with transactions

## YNAB Rules Engine - Implementation Plan

### Phase 1: Core Framework

1. **Domain Models**
   - Define Rule, Condition, and Action classes
   - Implement evaluation and application logic
   - Build validation interfaces

2. **Data Access**
   - Extend YNABService with required transaction operations
   - Implement ValidationService for runtime data validation
   - Add rule storage and persistence mechanisms

3. **Rules Engine**
   - Develop rule execution pipeline
   - Implement condition evaluation logic
   - Create action application system

### Phase 2: CLI Interface

1. **Interactive CLI**
   - Build command-line interface with rich prompts
   - Implement autocompletion for YNAB entities
   - Add validation feedback for user inputs

2. **Rule Management**
   - Create commands for rule CRUD operations
   - Implement rule testing functionality
   - Add rule import/export capabilities

### Phase 3: Integration

1. **Transaction Processing**
   - Implement batch processing of transactions
   - Add dry-run simulation mode
   - Develop conflict resolution strategies

2. **Reporting**
   - Create rule execution reports
   - Implement change tracking and auditing
   - Add performance metrics

### Technical Considerations

1. **Data Caching**
   - Cache YNAB entities (payees, categories, accounts) for validation
   - Implement efficient refresh strategies
   - Optimize for performance with large budgets

2. **Validation**
   - Support fuzzy matching for entity names
   - Handle non-existent entities gracefully
   - Provide helpful error messages and suggestions

3. **Rule Complexity**
   - Support rule chaining and prioritization
   - Allow complex condition groups (AND/OR logic)
   - Enable conditional actions

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
- Need for comprehensive validation in rules engine
- Handling of large YNAB datasets efficiently

## Next Steps

- Add unit and integration tests
- Implement additional LLM providers (OpenAI, Anthropic)
- Add batch mode for emoji namer
- Create a unified CLI interface for all tools
- Consider refactoring to use async/await for API calls
- Add logging functionality
- Develop the YNAB Rules Engine according to the implementation plan

## Dependencies

- Python 3.7+
- requests: API communication
- python-dotenv: Environment configuration
- groq: LLM integration
- prompt_toolkit: Interactive CLI (new)
- pydantic: Data validation (new)
- jsonschema: Rule schema validation (new)
