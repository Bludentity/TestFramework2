# E2E Test Framework

A comprehensive end-to-end testing framework built with Playwright and pytest for web application testing.

## Features

- **Playwright Integration**: Modern browser automation with support for Chromium, Firefox, and WebKit
- **Pytest Framework**: Powerful test runner with fixtures and parameterization
- **Page Object Model**: Clean and maintainable test architecture
- **Data-Driven Testing**: Support for CSV-based test data
- **Environment Configuration**: Flexible configuration via environment variables
- **Screenshot Capture**: Automatic screenshot capture on test failures
- **Parallel Execution**: Support for parallel test execution with pytest-xdist
- **Jira Integration**: Optional Jira integration for test management

## Prerequisites

- Python 3.8 or higher
- Node.js (for Playwright browsers)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Configuration

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Key configuration options:
- `BASE_URL`: Base URL for the application under test
- `BROWSER`: Browser to use (chromium, firefox, webkit)
- `HEADLESS_MODE`: Run tests in headless mode (true/false)
- `DEFAULT_TIMEOUT`: Default timeout in milliseconds

## Project Structure

```
├── pages/          # Page object models
├── tests/          # Test cases
├── utils/          # Utility functions
├── data/           # Test data files
├── locators.py     # Element locators
├── config.py       # Configuration settings
├── conftest.py     # Pytest fixtures
└── base_page.py    # Base page class
```


## Environment Variables

The framework supports the following environment variables:

- `BASE_URL`: Application base URL
- `BROWSER`: Browser selection (chromium/firefox/webkit)
- `HEADLESS_MODE`: Headless mode toggle
- `USE_CSV_DATA`: Enable CSV data-driven testing
- `SINGLE_SEARCH_TERM`: Single search term for testing
- `PDP_TEST_TERMS`: Comma-separated list of PDP test terms
- `DEFAULT_TIMEOUT`: Default timeout in milliseconds

## Jira Integration (Optional)

To enable Jira integration, set the following environment variables:
- `JIRA_URL`: Jira instance URL
- `JIRA_EMAIL`: Jira email
- `JIRA_API_TOKEN`: Jira API token
- `JIRA_PROJECT_KEY`: Jira project key

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request
