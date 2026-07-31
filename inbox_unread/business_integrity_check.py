import json
import os
from datetime import datetime, timezone

FILES = [
    "json_core/customer_real_deal_review.json",
    "json_core/original_10_target_priority.json",
    "json_core/merged_business_view.json",
    "json_core/business_portfolio_status.json",
    "json_core/business_execution_queue.json",
    "json_core/today_business_focus.json"
]

OUTPUT = "json_core/business_integrity_report.json"


def validate(path):
    if not os.path.exists(path):
        return {
            "file": path,
            "exists": False,
            "valid_json": False
        }

    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)

        return {
            "file": path,
            "exists": True,
            "valid_json": True
        }

    except Exception as e:
        return {
            "file": path,
            "exists": True,
            "valid_json": False,
            "error": str(e)
        }


report = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "policy": {
        "read_only": True,
        "schema_check": True,
        "manual_review_required": True
    },

    "files": []
}

ok = True

for path in FILES:

    item = validate(path)

    report["files"].append(item)

    if not (
        item["exists"]
        and item["valid_json"]
    ):
        ok = False

report["overall_status"] = (
    "HEALTHY"
    if ok
    else "CHECK_REQUIRED"
)

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        report,
        f,
        indent=2,
        ensure_ascii=False
    )

print("BUSINESS INTEGRITY CHECK COMPLETE")
print("STATUS:", report["overall_status"])
print("OUTPUT:", OUTPUT)
