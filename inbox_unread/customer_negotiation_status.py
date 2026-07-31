import json
from datetime import datetime, timezone

INPUT = "json_core/customer_real_deal_review.json"
OUTPUT = "json_core/customer_negotiation_status.json"

with open(INPUT, "r", encoding="utf-8") as f:
    src = json.load(f)

result = {
    "version": "1.0.0",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "policy": {
        "evidence_required": True,
        "manual_review_required": True
    },
    "negotiation": []
}

for c in src.get("customers", []):

    commit = c.get("signal", {}).get("commitment", "UNVERIFIED")

    if commit in (
        "NDA_IN_PROGRESS",
        "NEGOTIATION",
        "CONTRACT_REVIEW"
    ):
        stage = "NEGOTIATION"
    else:
        stage = "NOT_IN_NEGOTIATION"

    result["negotiation"].append({
        "customer_id": c.get("customer_id"),
        "stage": stage,
        "commitment": commit,
        "status": c.get("status"),
        "payment": c.get("signal", {}).get("payment", "UNVERIFIED")
    })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("NEGOTIATION STATUS COMPLETE")
print("OUTPUT:", OUTPUT)
