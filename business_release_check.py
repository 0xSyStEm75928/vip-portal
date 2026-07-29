import json
import os
from datetime import datetime, timezone

BASE = "json_core"

FILES = [
    "business_master_index.json",
    "business_pipeline_summary.json",
    "business_final_report.json",
    "business_integrity_report.json",
    "business_execution_queue.json",
    "today_business_focus.json"
]

OUTPUT = os.path.join(BASE, "business_release_check.json")


def check(path):
    full = os.path.join(BASE, path)

    item = {
        "file": path,
        "exists": os.path.exists(full),
        "valid_json": False
    }

    if item["exists"]:
        try:
            with open(full, "r", encoding="utf-8") as f:
                json.load(f)
            item["valid_json"] = True
        except Exception as e:
            item["error"] = str(e)

    return item


results = [check(x) for x in FILES]

ready = all(
    r["exists"] and r["valid_json"]
    for r in results
)

report = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "release_state":
        "READY"
        if ready
        else "CHECK_REQUIRED",

    "policy": {
        "read_only": True,
        "manual_release_required": True,
        "public_data_only": True
    },

    "files": results
}

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

print("BUSINESS RELEASE CHECK COMPLETE")
print("STATUS:", report["release_state"])
print("OUTPUT:", OUTPUT)
