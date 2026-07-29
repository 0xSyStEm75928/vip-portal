import json
from datetime import datetime, timezone

INPUT = "json_core/business_portfolio_status.json"
OUTPUT = "json_core/business_execution_queue.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def score(item):
    if item["source"] == "LEGACY":
        return 0

    priority = item.get("priority")

    if priority == "A":
        return 1

    if priority == "B":
        return 2

    return 3


source = load_json(INPUT)

queue = sorted(
    source.get("portfolio", []),
    key=score
)

result = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "policy": {
        "manual_review_required": True,
        "public_data_only": True,
        "execution_requires_confirmation": True
    },

    "execution_queue": []
}

for index, item in enumerate(queue, start=1):

    result["execution_queue"].append({

        "order": index,

        "source": item["source"],

        "target": item["id"],

        "priority": item.get("priority"),

        "stage": item.get("stage"),

        "next_step": item.get("next_step", [])

    })

save_json(OUTPUT, result)

print("BUSINESS EXECUTION QUEUE COMPLETE")
print("OUTPUT:", OUTPUT)
