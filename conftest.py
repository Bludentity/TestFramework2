"""
Purpose: Pytest configuration for Playwright browser setup/teardown and failure hooks.
Creates a browser fixture from config.py and captures screenshots + Jira tickets on failure.
"""
import pytest
import os
import time
import traceback as tb_module
from pathlib import Path
from playwright.sync_api import sync_playwright
from config import (
    BASE_URL,
    HEADLESS,
    BROWSER_NAME,
    SCREENSHOTS_DIR,
    timestamp,
    JIRA_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY,
)
from utils.jira_client import create_jira_issue_with_attachment, build_description


@pytest.fixture(scope='session')
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope='function')
def page(playwright_instance, request):
    if BROWSER_NAME == 'firefox':
        browser = playwright_instance.firefox.launch(headless=HEADLESS)
    elif BROWSER_NAME == 'webkit':
        browser = playwright_instance.webkit.launch(headless=HEADLESS)
    else:
        browser = playwright_instance.chromium.launch(headless=HEADLESS)

    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(10000)

    request.node._start_time = time.time()

    yield page

    try:
        context.close()
        browser.close()
    except Exception:
        pass


def _save_screenshot(page, nodeid: str) -> str | None:
    worker = os.getenv('PYTEST_XDIST_WORKER', 'local')
    safe_name = nodeid.replace('::', '_').replace('/', '_')
    fname = f"{worker}_{safe_name}_{timestamp()}.png"
    path = Path(SCREENSHOTS_DIR) / 'local_tests' / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(path), full_page=True)
        return str(path)
    except Exception:
        return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != 'call' or not rep.failed:
        return

    page = item.funcargs.get('page')
    if not page:
        return

    screenshot_path = _save_screenshot(page, item.nodeid)

    if not (JIRA_URL and JIRA_EMAIL and JIRA_API_TOKEN and JIRA_PROJECT_KEY):
        return


    traceback_str = 'Traceback unavailable.'
    try:
        if rep.longrepr:
            traceback_str = str(rep.longrepr)
    except Exception:
        pass

    start = getattr(item, '_start_time', None)
    duration = (time.time() - start) if start else 0.0

    description = build_description(
        test_nodeid=item.nodeid,
        test_name=item.name,
        traceback=traceback_str,
        browser=BROWSER_NAME,
        base_url=BASE_URL,
        duration=duration,
        screenshot_path=screenshot_path,
    )

    try:
        issue_key = create_jira_issue_with_attachment(
            project_key=JIRA_PROJECT_KEY,
            summary=f"[Automated] Test failure: {item.name}",
            description=description,
            filename=screenshot_path,
        )
        rep.jira_issue = issue_key
        print(f"\n  Jira issue created: {JIRA_URL.rstrip('/')}/browse/{issue_key}")
    except Exception:
        tb_module.print_exc()
