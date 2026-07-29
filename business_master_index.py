import json
from datetime import datetime, timezone

OUTPUT = "json_core/business_master_index.json"

files = [
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
    "business_integrity_report.json"
]

result = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "pipeline_status": "READY",

    "documents": files
}

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        result,
        f,
        indent=2,
        ensure_ascii=False
    )

print("BUSINESS MASTER INDEX COMPLETE")
print("OUTPUT:", OUTPUT)
