# Ops Commander

Ops Commander is a production-grade autonomous incident response and mitigation platform.

It continuously monitors incidents, correlates telemetry with deploys and GitHub commits, performs AI-powered investigations, integrates with AWS DevOps Agent, and delivers operational intelligence directly into Slack.

## Architecture

```text
Sentry / Alerts
    ↓
Ops Commander API
    ↓
Investigation Pipeline
    ├── GitHub correlation
    ├── AI Investigator
    ├── AWS DevOps Agent adapter
    ├── Incident orchestration
    └── Slack notification engine
```

## Features

- FastAPI production API
- AI-powered incident investigation
- GitHub deploy correlation
- Slack incident summaries
- AWS DevOps Agent integration layer
- Typed configuration system
- Extensible multi-agent architecture
- Production-ready dependency stack

## Environment Variables

```env
REPO_FULL_NAME=sapientra/trintus-ops
GITHUB_TOKEN=github_token
SLACK_WEBHOOK_URL=slack_webhook
OPENAI_API_KEY=openai_key
OPENAI_MODEL=gpt-4.1-mini
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=aws_key
AWS_SECRET_ACCESS_KEY=aws_secret
AWS_DEVOPS_AGENT_ENABLED=true
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Test incident

```bash
curl -X POST http://127.0.0.1:8000/webhook/sentry \
  -H "Content-Type: application/json" \
  -d '{"title":"TypeError: Cannot read property id of undefined","project_name":"payments-api","release":"abc123"}'
```

## Next production upgrades

- Postgres incident persistence
- Slack interactive approvals
- Autonomous rollback engine
- Recovery verification agent
- Prevention PR generator
- Kubernetes and CloudWatch integrations
- Long-term operational memory
- Multi-tenant architecture
