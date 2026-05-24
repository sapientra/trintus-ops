import re
from typing import List, Dict, Any, Optional


def find_root_cause(error_message: str, commits: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not commits:
        return None

    error_tokens = set(re.findall(r"\\b\\w+\\b", error_message.lower()))

    best_match = None
    best_score = 0

    for commit in commits:
        message_tokens = set(re.findall(r"\\b\\w+\\b", commit["message"].lower()))
        overlap = error_tokens & message_tokens
        score = len(overlap)

        if score > best_score:
            best_score = score
            best_match = commit

    return best_match if best_match is not None else commits[0]
