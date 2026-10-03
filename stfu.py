#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["typesafe-sdk>=0.7"]
# ///

import json
import sys

from typesafe_sdk import RetryPolicy, Score, TypeSafeClient

MODEL = "jev-latest"
MIN_CONFIDENCE = 0.5

LEVELS = [
    ("A yes/no, a single fact, a name, or a command",
     "Answer in one sentence, up to 10 words."),
    ("A short explanation or a quick comparison",
     "Answer in up to three sentences, up to 10 words each."),
    ("An explanation that needs some nuance",
     "Answer in one short paragraph, up to 60 words."),
    ("Code changes, multi-step work, debugging, or a document; must not be truncated",
     None),
]


def ideal_length(prompt: str) -> tuple[float, float]:
    with TypeSafeClient(
        model=MODEL,
        timeout=5.0,
        retry=RetryPolicy(max_retries=0),
    ) as client:
        response = client.system_one(
            state=prompt[:8000],
            questions={
                "length": Score(
                    instructions="How long the ideal answer to this request to a coding agent is",
                    criteria=[desc for desc, _ in LEVELS],
                ),
            },
        )
    answer = response.scores["length"]
    return answer.score, answer.confidence


def main() -> None:
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
        if not prompt or prompt.startswith("/"):
            return
        score, confidence = ideal_length(prompt)
        if confidence < MIN_CONFIDENCE:
            return
        level = min(max(int(score + 0.5), 0), len(LEVELS) - 1)
        rule = LEVELS[level][1]
        if rule:
            print(
                "Response length constraint for this turn, only for the "
                f"answer you write to the user: {rule}"
            )
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)
