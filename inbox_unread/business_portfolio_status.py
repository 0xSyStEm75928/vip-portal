import json
import os
from datetime import datetime, timezone

BASE = "json_core"

FILES = {
    "legacy": os.path.join(BASE, "customer_real_deal_review.json"),
    "cli": os.path.join(BASE, "original_10_target_priority.json")
}

OUTPUT = os.path.join(BASE, "business_portfolio_status.json")


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


legacy = load_json(FILES["legacy"])
cli = load_json(FILES["cli"])

result = {
    "version": "1.0.0",
    "generated_at": datetime.now(timezone.utc).isoformat(),

    "policy": {
        "datasets_separated": True,
        "manual_review_required": True,
        "public_data_only": True,
        "no_private_interest_assumption": True
    },

    "summary": {
        "legacy_total": len(legacy.get("customers", [])),
        "cli_total": len(cli.get("targets", [])),
        "portfolio_total": (
            len(legacy.get("customers", []))
            + len(cli.get("targets", []))
        )
    },

    "portfolio": []
}

for c in legacy.get("customers", []):
    result["portfolio"].append({
        "source": "LEGACY",
        "id": c.get("customer_id"),
        "stage": c.get("status"),
        "priority": "BUSINESS",
        "payment": c.get("signal", {}).get("payment"),
        "next_step": c.get("review", {}).get("next_check", [])
    })

for t in cli.get("targets", []):
    result["portfolio"].append({
        "source": "CLI_DISCOVERY",
        "id": t.get("name"),
        "stage": t.get("review_stage"),
        "priority": t.get("priority"),
        "contact": t.get("contact_state"),
        "next_step": [
            t.get("next_action")
        ]
    })

save_json(OUTPUT, result)

print("BUSINESS PORTFOLIO STATUS COMPLETE")
print("OUTPUT:", OUTPUT)
