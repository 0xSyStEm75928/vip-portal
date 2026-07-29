import json
from datetime import datetime, timezone

INPUT = "json_core/customer_execution_gate_check.json"
OUTPUT = "json_core/customer_final_business_dashboard.json"


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


def classify(item):

    execution = item.get(
        "execution_state",
        "UNKNOWN"
    )

    priority = item.get(
        "priority",
        "C"
    )

    if execution == "POSSIBLE":
        stage = "READY_FOR_HUMAN_REVIEW"

    elif priority == "A":
        stage = "HIGH_PRIORITY_PENDING"

    elif priority == "B":
        stage = "OBSERVATION"

    else:
        stage = "LOW_SIGNAL"


    return {
        "customer_id":
            item.get("customer_id"),

        "priority":
            priority,

        "execution_state":
            execution,

        "business_stage":
            stage,

        "contact_permission":
            "NOT_GRANTED",

        "purchase_intent":
            "UNVERIFIED",

        "next_step": [
            "human_confirmation",
            "verify_requirement",
            "verify_contract",
            "verify_payment"
        ]
    }


def main():

    source = load_json(INPUT)

    result = {

        "version": "1.0.0",

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "policy": {

            "public_data_only":
                True,

            "no_hidden_interest_claim":
                True,

            "no_auto_contact":
                True,

            "human_decision_required":
                True
        },


        "dashboard": [

            classify(x)
            for x in source.get(
                "execution_checks",
                []
            )

        ]

    }


    save_json(
        OUTPUT,
        result
    )


    print(
        "CUSTOMER FINAL BUSINESS DASHBOARD COMPLETE"
    )

    print(
        "OUTPUT:",
        OUTPUT
    )


if __name__ == "__main__":
    main()
