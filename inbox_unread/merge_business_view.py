import json
import os
from datetime import datetime, timezone

BASE = "json_core"

LEGACY = os.path.join(BASE, "customer_real_deal_review.json")
CLI = os.path.join(BASE, "original_10_target_priority.json")
OUTPUT = os.path.join(BASE, "merged_business_view.json")


def load_json(path):
    if not os.path.exists(path):
        return {}
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


legacy = load_json(LEGACY)
cli = load_json(CLI)

result = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "policy": {
        "datasets_are_separated": True,
        "public_data_only_for_cli": True,
        "manual_review_required": True,
        "no_private_interest_assumption": True
    },

    "legacy_candidates": [],
    "cli_candidates": []
}

for c in legacy.get("customers", []):

    result["legacy_candidates"].append({

        "source": "LEGACY",

        "id": c.get("customer_id"),

        "status": c.get("status"),

        "communication":
            c.get("signal", {}).get("communication"),

        "commitment":
            c.get("signal", {}).get("commitment"),

        "payment":
            c.get("signal", {}).get("payment")

    })


for t in cli.get("targets", []):

    result["cli_candidates"].append({

        "source": "CLI_DISCOVERY",

        "name": t.get("name"),

        "priority": t.get("priority"),

        "group": t.get("group"),

        "contact": t.get("contact_state"),

        "interest": t.get("interest")

    })


save_json(
    OUTPUT,
    result
)

print("MERGED BUSINESS VIEW COMPLETE")
print("OUTPUT:", OUTPUT)
