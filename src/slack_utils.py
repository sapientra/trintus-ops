import os
import json
import logging
from typing import Dict

import requests

logger = logging.getLogger(__name__)


def send_message(text: str, blocks: list | None = None) -> None:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URL not set; skipping Slack notification")
        return

    payload: Dict[str, any] = {"text": text}

    if blocks:
        payload["blocks"] = blocks

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        webhook_url,
        headers=headers,
        data=json.dumps(payload),
        timeout=10,
    )

    if response.status_code >= 400:
        raise RuntimeError(f"Slack webhook error {response.status_code}: {response.text}")
