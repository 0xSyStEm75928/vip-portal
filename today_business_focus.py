import json
from datetime import datetime, timezone

INPUT = "json_core/business_execution_queue.json"
OUTPUT = "json_core/today_business_focus.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


source = load_json(INPUT)

queue = source.get("execution_queue", [])

result = {
    "version": "1.0.0",

    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "policy": {
        "manual_execution": True,
        "human_confirmation_required": True,
        "no_delivery_without_payment": True,
        "public_data_only": True
    },

    "today_focus": []
}

for item in queue[:5]:

    result["today_focus"].append({

        "order": item.get("order"),

        "target": item.get("target"),

        "source": item.get("source"),

        "priority": item.get("priority"),

        "stage": item.get("stage"),

        "status": "READY_FOR_REVIEW",

        "required_action": item.get(
            "next_step",
            []
        )

    })

save_json(
    OUTPUT,
    result
)

print("TODAY BUSINESS FOCUS COMPLETE")
print("OUTPUT:", OUTPUT)
