# YNAB Utilities Core Package

## Overview

This core package provides shared utilities and services for YNAB-related Python projects, including:

- Configuration management
- YNAB API interactions
- LLM (Language Model) services
- Text processing utilities

## Package Structure

- `config.py`: Configuration management and loading
- `services/`
  - `ynab_service.py`: YNAB API interactions
  - `llm_service.py`: Language Model service abstractions
- `utils/`
  - `text_utils.py`: Text processing utilities

## Key Features

- Flexible configuration loading
- YNAB API service with comprehensive methods
- LLM service with Groq API implementation
- Emoji and text processing utilities

## Requirements

- Python 3.7+
- `requests` library
- `python-dotenv`

## Usage

Import and use services and utilities in your YNAB-related projects:

```python
from core.config import load_config
from core.services.ynab_service import YNABService
from core.utils.text_utils import has_emoji
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

These utilities are provided as-is and may require adaptation for specific use cases.