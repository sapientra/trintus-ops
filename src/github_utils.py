import os
import logging
from typing import List, Dict, Any

import requests

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"


def _get_headers() -> Dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ops-commander-mvp",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_recent_commits(repo_full_name: str, n: int = 5) -> List[Dict[str, Any]]:
    url = f"{GITHUB_API_BASE}/repos/{repo_full_name}/commits"
    response = requests.get(url, headers=_get_headers(), params={"per_page": n}, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"GitHub API error {response.status_code}: {response.text}")

    commits = []
    for commit in response.json():
        commit_info = commit.get("commit", {})
        author_info = commit_info.get("author", {})
        commits.append({
            "sha": commit.get("sha"),
            "message": commit_info.get("message", "").strip(),
            "author_name": author_info.get("name"),
            "author_email": author_info.get("email"),
            "date": author_info.get("date"),
        })

    return commits
