import json
import os
from datetime import datetime, timezone

BASE = "json_core"

FILES = {
    "summary": "business_pipeline_summary.json",
    "integrity": "business_integrity_report.json",
    "portfolio": "business_portfolio_status.json",
    "focus": "today_business_focus.json"
}

OUTPUT = os.path.join(BASE, "business_final_report.json")


def load(name):
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


summary = load(FILES["summary"])
integrity = load(FILES["integrity"])
portfolio = load(FILES["portfolio"])
focus = load(FILES["focus"])

result = {
    "version": "1.0.0",
    "generated_at": datetime.now(timezone.utc).isoformat(),

    "status": {
        "pipeline": summary.get("status", "UNKNOWN"),
        "health": integrity.get("overall_status", "UNKNOWN")
    },

    "counts": {
        "portfolio": portfolio.get("summary", {}).get("portfolio_total", 0),
        "legacy": portfolio.get("summary", {}).get("legacy_total", 0),
        "cli": portfolio.get("summary", {}).get("cli_total", 0),
        "today_focus": len(focus.get("today_focus", []))
    },

    "policy": {
        "public_data_only": True,
        "manual_review_required": True,
        "no_private_interest_assumption": True,
        "execution_requires_confirmation": True
    },

    "result": "READY_FOR_HUMAN_REVIEW"
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("BUSINESS FINAL REPORT COMPLETE")
print("OUTPUT:", OUTPUT)
