import json
from datetime import datetime, timezone

INPUT = "json_core/original_10_target_audit.json"
OUTPUT = "json_core/original_10_target_priority.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def calc_priority(target):

    stars = target.get("stars") or 0
    group = target.get("group")

    if group == "ORIGINAL_3":
        priority = "A"
    elif stars >= 100000:
        priority = "A"
    elif stars >= 50000:
        priority = "B"
    else:
        priority = "C"

    return {
        "name": target.get("name"),
        "url": target.get("url"),
        "group": group,
        "stars": stars,
        "priority": priority,
        "review_stage": target.get("review_stage"),
        "business_state": "REVIEW_REQUIRED",
        "contact_state": "NOT_STARTED",
        "interest": "UNVERIFIED",
        "next_action": "HUMAN_REVIEW"
    }


def main():

    source = load_json(INPUT)

    targets = [
        calc_priority(t)
        for t in source.get("targets", [])
    ]

    order = {"A": 0, "B": 1, "C": 2}
    targets.sort(
        key=lambda x: (
            order[x["priority"]],
            -(x["stars"] or 0)
        )
    )

    result = {
        "version": "1.0.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "policy": {
            "public_data_only": True,
            "manual_review_required": True,
            "no_private_interest_assumption": True
        },
        "targets": targets
    }

    save_json(
        OUTPUT,
        result
    )

    print("TARGET PRIORITY COMPLETE")
    print("OUTPUT:", OUTPUT)


if __name__ == "__main__":
    main()
