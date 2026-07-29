import json
import os
from datetime import datetime, timezone

BASE = "json_core"

FILES = {
    "integrity": "business_integrity_report.json",
    "portfolio": "business_portfolio_status.json",
    "queue": "business_execution_queue.json",
    "focus": "today_business_focus.json",
    "dashboard": "customer_final_business_dashboard.json"
}

OUTPUT = os.path.join(BASE, "business_pipeline_summary.json")


def load(name):
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


integrity = load(FILES["integrity"])
portfolio = load(FILES["portfolio"])
queue = load(FILES["queue"])
focus = load(FILES["focus"])
dashboard = load(FILES["dashboard"])

result = {
    "version": "1.0.0",
    "generated_at": datetime.now(timezone.utc).isoformat(),

    "summary": {
        "pipeline_health": integrity.get(
            "overall_status",
            "UNKNOWN"
        ),

        "portfolio_total":
            portfolio.get(
                "summary",
                {}
            ).get(
                "portfolio_total",
                0
            ),

        "execution_queue":
            len(
                queue.get(
                    "execution_queue",
                    []
                )
            ),

        "today_focus":
            len(
                focus.get(
                    "today_focus",
                    []
                )
            ),

        "dashboard_items":
            len(
                dashboard.get(
                    "dashboard",
                    []
                )
            )
    },

    "status": "READY"
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

print("BUSINESS PIPELINE SUMMARY COMPLETE")
print("OUTPUT:", OUTPUT)
