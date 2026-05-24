import logging
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from . import github_utils, slack_utils
from .ai_investigator import investigate_incident
from .aws_devops_agent import AWSDevOpsAgentClient
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ops Commander")

aws_agent = AWSDevOpsAgentClient()


@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "message": "Ops Commander is running",
        "environment": settings.environment,
    }


@app.post("/webhook/sentry")
async def handle_sentry_webhook(payload: Dict[str, Any]):
    try:
        error_message = payload.get("error", {}).get("message") or payload.get("title")
        release = payload.get("release") or payload.get("release_version")
        project_name = payload.get("project_name")

        if not error_message:
            raise ValueError("No error message found in payload")

        if not settings.repo_full_name:
            raise RuntimeError("REPO_FULL_NAME environment variable must be set")

        commits = github_utils.get_recent_commits(settings.repo_full_name, n=10)

        ai_report = investigate_incident(
            error_message=error_message,
            project_name=project_name,
            release=release,
            commits=commits,
        )

        aws_report = None

        if settings.aws_devops_agent_enabled:
            aws_report = aws_agent.investigate_incident(payload)

        message = f"""
🚨 INCIDENT DETECTED

Project: {project_name}
Release: {release}
Error: {error_message}

AI Investigation:
{ai_report}

AWS DevOps Agent:
{aws_report}
"""

        slack_utils.send_message(message)

        return JSONResponse(
            {
                "status": "ok",
                "ai_report": ai_report,
                "aws_report": aws_report,
            }
        )

    except Exception as exc:
        logger.exception("Error handling incident")
        raise HTTPException(status_code=500, detail=str(exc))
