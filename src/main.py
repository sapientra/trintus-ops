import os
import logging
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from . import github_utils, investigator, slack_utils

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ops Commander MVP")

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Ops Commander is running"}

@app.post("/webhook/sentry")
async def handle_sentry_webhook(payload: Dict[str, Any]):
    try:
        error_message = payload.get("error", {}).get("message") or payload.get("title")
        release = payload.get("release") or payload.get("release_version")
        project_name = payload.get("project_name")

        if not error_message:
            raise ValueError("No error message found in payload")

        repo_full_name = os.getenv("REPO_FULL_NAME")
        if not repo_full_name:
            raise RuntimeError("REPO_FULL_NAME environment variable must be set")

        commits = github_utils.get_recent_commits(repo_full_name, n=5)
        culprit = investigator.find_root_cause(error_message, commits)

        text_lines = [
            f"🚨 Incident detected in `{project_name}`",
            f"Error: {error_message}",
        ]

        if release:
            text_lines.append(f"Release: {release}")

        if culprit:
            text_lines.append(
                f"Suspected commit: {culprit['sha'][:7]} by {culprit['author_name']}"
            )
            text_lines.append(f"Commit message: {culprit['message']}")
            text_lines.append("Suggested action: rollback latest deployment and investigate changes.")
        else:
            text_lines.append("No specific commit identified.")

        slack_text = "\n".join(text_lines)
        slack_utils.send_message(slack_text)

        logger.info("Incident processed successfully")
        return JSONResponse({"status": "ok"})

    except Exception as exc:
        logger.exception("Error handling Sentry webhook")
        raise HTTPException(status_code=500, detail=str(exc))
