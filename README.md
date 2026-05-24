# Ops Commander MVP

This repository contains a minimal proof-of-concept for an **autonomous incident investigation agent**.

The goal of this MVP is to demonstrate how a small service can ingest error alerts, correlate them with recent GitHub commits, and notify a team in Slack with a probable root cause and suggested action. It is intentionally simple but designed to be extended into a multi-agent, always-on incident response and mitigation system.

## How it works

1. **Webhook endpoint** - The service exposes a `/webhook/sentry` endpoint using FastAPI. You can configure Sentry to call this URL when an error occurs.
2. **Incident ingestion** - When an alert arrives, the server extracts the error message, project, release, and timestamp.
3. **GitHub context** - The service fetches recent commits from the configured GitHub repository using the GitHub REST API.
4. **Root cause heuristic** - The MVP compares the error message with recent commit messages and selects the most likely culprit.
5. **Slack notification** - The service posts an incident summary to Slack through an incoming webhook.

## Project structure

```text
src/main.py          FastAPI app and Sentry webhook route
src/github_utils.py  GitHub API helpers
src/investigator.py  Root-cause heuristic
src/slack_utils.py   Slack webhook helper
requirements.txt     Python dependencies
Dockerfile           Container runtime
```

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Create a `.env` file:

```env
GITHUB_TOKEN=ghp_xxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
REPO_FULL_NAME=yourusername/yourrepo
```

## Test payload

```bash
curl -X POST http://localhost:8000/webhook/sentry \
  -H "Content-Type: application/json" \
  -d '{"title":"TypeError: Cannot read property id of undefined","project_name":"payments-api","release":"abc123"}'
```

## Next extensions

- Slack bot with `/investigate`, `/rollback`, and `/postmortem`
- LLM-powered investigation using stack traces, diffs, logs, and deploy metadata
- Human approval workflow for rollback
- Recovery verification agent
- Prevention PR agent that proposes code/config changes after incident resolution
