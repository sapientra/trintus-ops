import json
from openai import OpenAI

from .config import settings

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = "You are an expert SRE and incident investigation assistant. Return concise JSON."


def investigate_incident(error_message, project_name, release, commits):
    prompt = f"""
Analyze this production incident.

Project: {project_name}
Release: {release}
Error: {error_message}

Recent commits:
{json.dumps(commits, indent=2)}

Return JSON with:
- severity
- probable_root_cause
- suspected_commit_sha
- confidence_score
- recommended_mitigation
- rollback_recommended
- slack_summary
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content
