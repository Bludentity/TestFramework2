"""
Purpose: Create Jira bug tickets with full context on test failure.
Uses Jira REST API v2 with wiki-markup description (supported by all Jira Cloud plans).
"""
import requests
from typing import Optional
from pathlib import Path
from config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN


def _auth():
    return (JIRA_EMAIL, JIRA_API_TOKEN)


def create_jira_issue_with_attachment(
    project_key: str,
    summary: str,
    description: str,
    filename: Optional[str] = None,
) -> Optional[str]:
    if not (JIRA_URL and JIRA_EMAIL and JIRA_API_TOKEN):
        raise RuntimeError('Jira not configured — set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN in .env')

    create_url = f"{JIRA_URL.rstrip('/')}/rest/api/2/issue"
    payload = {
        'fields': {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Bug'},
        }
    }
    r = requests.post(
        create_url,
        json=payload,
        auth=_auth(),
        headers={'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    issue_key = r.json().get('key')

    if filename and Path(filename).exists():
        attach_url = f"{JIRA_URL.rstrip('/')}/rest/api/2/issue/{issue_key}/attachments"
        with open(filename, 'rb') as fh:
            requests.post(
                attach_url,
                files={'file': (Path(filename).name, fh, 'image/png')},
                auth=_auth(),
                headers={'X-Atlassian-Token': 'no-check'},
                timeout=30,
            ).raise_for_status()

    return issue_key


def build_description(
    test_nodeid: str,
    test_name: str,
    traceback: str,
    browser: str,
    base_url: str,
    duration: float,
    screenshot_path: Optional[str] = None,
) -> str:


    screenshot_note = (
        f"Screenshot attached: *{Path(screenshot_path).name}*"
        if screenshot_path and Path(screenshot_path).exists()
        else "No screenshot captured."
    )

    return (
        f"h2. Automated Test Failure\n\n"
        f"||Field||Value||\n"
        f"|Test name|{test_name}|\n"
        f"|Node ID|{test_nodeid}|\n"
        f"|Browser|{browser}|\n"
        f"|Base URL|{base_url}|\n"
        f"|Duration|{duration:.2f}s|\n\n"
        f"h3. Failure Details\n\n"
        f"{screenshot_note}\n\n"
        f"h3. Traceback\n\n"
        f"{{code:language=python}}\n"
        f"{traceback}\n"
        f"{{code}}"
    )
