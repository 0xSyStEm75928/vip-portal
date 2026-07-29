import json
import os
from datetime import datetime, timezone

BASE = "json_core"

FILES = [
    "ZERO_CORE.customer.json",
    "customer_intake.json",
    "customer_lifecycle_gate.json",
    "customer_review_queue.json",
    "tomorrow_operation_plan.json",

    "cli_business_candidate_review.json",
    "cli_business_signal_deep_review.json",

    "customer_real_deal_review.json",
    "customer_deal_sync_result.json",
    "customer_deal_action_plan.json",
    "customer_execution_gate_check.json",
    "customer_final_business_dashboard.json",

    "original_10_target_audit.json",
    "original_10_target_priority.json",

    "merged_business_view.json",
    "business_portfolio_status.json",
    "business_execution_queue.json",
    "today_business_focus.json",

    "business_integrity_report.json",
    "business_master_index.json",
    "business_pipeline_summary.json",
    "business_final_report.json",
    "business_release_check.json"
]

OUTPUT = os.path.join(BASE, "business_bundle.json")


def load(path):
    full = os.path.join(BASE, path)

    if not os.path.exists(full):
        return {
            "exists": False
        }

    try:
        with open(full, "r", encoding="utf-8") as f:
            return {
                "exists": True,
                "content": json.load(f)
            }
    except Exception as e:
        return {
            "exists": True,
            "error": str(e)
        }


bundle = {
    "version": "2.0.0",

    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "pipeline": "BUSINESS_MASTER",

    "status": "READY",

    "documents": {}
}

for file in FILES:
    bundle["documents"][file] = load(file)

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
print("BUSINESS BUNDLE COMPLETE")
print("FILES :", len(FILES))
print("OUTPUT:", OUTPUT)
print("=" * 72)
