"""
Purpose: Central configuration for the E2E framework. Holds base URL, environment toggles,
browser settings, timeouts, and paths. This file is the single place to swap base URLs
and environment-level settings when testing different websites/environments.
"""
from pathlib import Path
import os
import datetime
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
env_path = ROOT / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# Base URL for the site under test.
BASE_URL = os.getenv('BASE_URL', 'https://practicesoftwaretesting.com/')

# Browser settings
HEADLESS = os.getenv('HEADLESS_MODE', os.getenv('HEADLESS', 'true')).lower() in ('1', 'true', 'yes')
BROWSER_NAME = os.getenv('BROWSER', 'chromium')  # 'chromium', 'firefox', 'webkit'

# Data-driven toggle
USE_CSV_DATA = os.getenv('USE_CSV_DATA', 'true').lower() in ('1', 'true', 'yes')
SINGLE_SEARCH_TERM = os.getenv('SINGLE_SEARCH_TERM', 'chisel')
PDP_TEST_TERMS = [t.strip() for t in os.getenv('PDP_TEST_TERMS', 'chisel, hammer, shirt').split(',')]

# Jira configuration (may be unset in local runs)
JIRA_URL = os.getenv('JIRA_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

# Timeouts (ms)
DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '10000'))

# Screenshots directory
SCREENSHOTS_DIR = ROOT / 'screenshots'
SCREENSHOTS_DIR.mkdir(exist_ok=True)


def timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
