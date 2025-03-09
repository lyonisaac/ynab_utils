# YNAB Emoji Namer

## Overview

YNAB Emoji Namer is a Python utility that automatically adds emojis to your YNAB payees, making your budget more visually engaging and easier to navigate.

## Features

- Identifies payees without emojis
- Uses AI to suggest appropriate emojis
- Interactive approval process with retry option
- Ignore specific payees
- Persists ignored payee list
- Avoids duplicate emoji suggestions during retries

## Prerequisites

- Python 3.7+
- YNAB API key
- Groq API key (or alternative LLM provider)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root
2. Add your credentials:
   ```
   YNAB_API_KEY=your_ynab_api_key
   YNAB_BUDGET_ID=your_budget_id
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=llama3-70b-8192
   ```

## Usage

### Basic Usage
```bash
python -m ynab_namer
```

### Workflow
- Scans your YNAB payees
- Suggests emojis for payees without them
- Interactively approve, reject, retry, or ignore suggestions
- Option to ignore specific payees

### Interactive Options
- `y` - Accept the suggested emoji and update payee name
- `n` - Reject the suggestion and proceed to next payee
- `i` - Ignore this payee in future runs
- `r` - Retry with an alternative emoji suggestion

## Customization

- Modify `ignored_payees.json` to manually ignore payees
- Configure LLM provider in the `.env` file

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

This tool interacts with your YNAB budget. Always review suggested changes carefully.