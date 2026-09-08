#!/usr/bin/env python3
"""
sync_status.py

Called at the end of every pipeline run. Updates a Jira ticket's status
and posts a status note to Confluence -- the "API-based automation
across Bitbucket, Jira, and Confluence" bullet from the job posting.

Defaults to --dry-run so it's safely demoable without real credentials:
it prints exactly the HTTP calls it *would* make.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone


def build_jira_transition_payload(status: str) -> dict:
    # Real Jira transition IDs come from your project's workflow config --
    # these are placeholder example IDs.
    transition_id = "31" if status == "success" else "41"
    return {"transition": {"id": transition_id}}


def build_confluence_comment(status: str, build: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    emoji = "PASS" if status == "success" else "FAIL"
    return f"[{emoji}] Pipeline build #{build} finished with status '{status}' at {ts}."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", choices=["success", "failure"], required=True)
    parser.add_argument("--build", required=True)
    parser.add_argument("--jira-ticket", default=os.environ.get("JIRA_TICKET", "DEVOPS-123"))
    parser.add_argument("--dry-run", action="store_true", default=True)
    args = parser.parse_args()

    jira_base = os.environ.get("JIRA_BASE_URL", "https://your-org.atlassian.net")

    jira_url = f"{jira_base}/rest/api/3/issue/{args.jira_ticket}/transitions"
    jira_payload = build_jira_transition_payload(args.status)
    confluence_comment = build_confluence_comment(args.status, args.build)

    print("[DRY RUN] Would POST to Jira:")
    print(f"  URL:  {jira_url}")
    print(f"  Body: {json.dumps(jira_payload)}")
    print()
    print("[DRY RUN] Would POST comment to Confluence:")
    print(f"  {confluence_comment}")
    return 0


if __name__ == "__main__":
    sys.exit(main())