import json
from datetime import datetime, timezone

INPUT = "json_core/customer_deal_action_plan.json"
OUTPUT = "json_core/customer_execution_gate_check.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def gate_check(item):

    payment = item.get(
        "payment_state"
    )

    priority = item.get(
        "priority"
    )

    if payment == "VERIFIED":
        execution = "POSSIBLE"
    else:
        execution = "LOCKED"

    return {
        "customer_id":
            item.get("customer_id"),

        "priority":
            priority,

        "recommended_action":
            item.get("recommended_action"),

        "execution_state":
            execution,

        "reason":
            "PAYMENT_CONFIRMATION_REQUIRED"
            if execution == "LOCKED"
            else "PAYMENT_CONFIRMED",

        "manual_review":
            True
    }


def main():

    source = load_json(INPUT)

    result = {
        "version": "1.0.0",

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "policy": {
            "no_delivery_before_confirmation": True,
            "payment_gate_required": True,
            "human_approval_required": True
        },

        "execution_checks": [
            gate_check(x)
            for x in source.get(
                "tomorrow_actions",
                []
            )
        ]
    }

    save_json(
        OUTPUT,
        result
    )

    print("CUSTOMER EXECUTION GATE CHECK COMPLETE")
    print("OUTPUT:", OUTPUT)


if __name__ == "__main__":
    main()
