import json
import os
from datetime import datetime, timezone

INPUT = "json_core/cli_target_discovery.json"
OUTPUT = "json_core/cli_business_candidate_review.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def score_target(target):

    desc = (
        target.get("description") or ""
    ).lower()

    name = (
        target.get("name") or ""
    ).lower()

    signals = []

    keywords = {
        "ai": "AI",
        "agent": "AI_AGENT",
        "workflow": "AUTOMATION",
        "cli": "CLI",
        "developer": "DEVELOPER_PLATFORM",
        "knowledge": "KNOWLEDGE_SYSTEM",
        "automation": "AUTOMATION"
    }

    for key, label in keywords.items():
        if key in desc or key in name:
            signals.append(label)


    if len(signals) >= 3:
        priority = "A"
    elif len(signals) >= 1:
        priority = "B"
    else:
        priority = "C"


    return {
        "name": target.get("name"),
        "url": target.get("url"),
        "stars": target.get("stars"),
        "language": target.get("language"),
        "signals": signals,
        "technical_match": "POSSIBLE" if signals else "LOW",
        "business_contact": "REQUIRES_REVIEW",
        "private_interest": "UNVERIFIED",
        "priority": priority
    }


def main():

    data = load_json(INPUT)

    targets = data.get("targets", [])

    result = {
        "version": "1.0.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "policy": {
            "public_data_only": True,
            "no_hidden_interest_assumption": True,
            "human_review_required": True
        },

        "summary": {
            "total_targets": len(targets)
        },

        "candidates": [
            score_target(t)
            for t in targets
        ]
    }


    save_json(
        OUTPUT,
        result
    )

    print("CLI CANDIDATE REVIEW COMPLETE")
    print("TARGETS:", len(targets))
    print("OUTPUT:", OUTPUT)


if __name__ == "__main__":
    main()
