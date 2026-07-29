import json
import os
from datetime import datetime, timezone

BASE = "json_core"

FILES = [
    "business_master_index.json",
    "business_pipeline_summary.json",
    "business_integrity_report.json",
    "business_release_check.json",
    "business_final_report.json",
    "business_execution_queue.json",
    "today_business_focus.json",
    "business_portfolio_status.json",
    "merged_business_view.json",
    "customer_final_business_dashboard.json"
]

def load(name):
    path = os.path.join(BASE, name)

    if not os.path.exists(path):
        return {
            "exists": False
        }

    with open(path, "r", encoding="utf-8") as f:
        return {
            "exists": True,
            "content": json.load(f)
        }

bundle = {
    "version": "3.0.0",

    "generated_at":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "kernel": "BUSINESS_MASTER",

    "status": "READY",

    "documents": {},

    "statistics": {
        "total_documents": len(FILES),
        "loaded": 0,
        "missing": 0
    }
}

for file in FILES:

    obj = load(file)

    bundle["documents"][file] = obj

    if obj["exists"]:
        bundle["statistics"]["loaded"] += 1
    else:
        bundle["statistics"]["missing"] += 1

OUTPUT = os.path.join(
    BASE,
    "business_master_bundle.json"
)

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        bundle,
        f,
        indent=2,
        ensure_ascii=False
    )

print("=" * 72)
print("BUSINESS MASTER BUNDLE COMPLETE")
print("OUTPUT :", OUTPUT)
print("LOADED :", bundle["statistics"]["loaded"])
print("MISSING:", bundle["statistics"]["missing"])
print("=" * 72)
