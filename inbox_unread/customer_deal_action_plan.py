import json
from datetime import datetime, timezone

INPUT = "json_core/customer_deal_sync_result.json"
OUTPUT = "json_core/customer_deal_action_plan.json"


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


def decide_priority(item):

    signal = item.get("signal", {})

    communication = signal.get(
        "communication",
        "UNVERIFIED"
    )

    commitment = signal.get(
        "commitment",
        "UNVERIFIED"
    )

    payment = signal.get(
        "payment",
        "UNVERIFIED"
    )


    if (
        communication == "SPEC_VERIFIED"
        and commitment == "NDA_IN_PROGRESS"
    ):
        return {
            "priority": "A",
            "action": "NDA_AND_REQUIREMENT_CONFIRMATION"
        }


    if communication == "OBSERVED":
        return {
            "priority": "B",
            "action": "VALIDATE_CONTACT_AND_REQUEST"
        }


    return {
        "priority": "C",
        "action": "WAIT_FOR_SIGNAL"
    }


def main():

    source = load_json(INPUT)

    result = {

        "version": "1.0.0",

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "policy": {
            "evidence_based": True,
            "no_assumption": True,
            "manual_execution": True
        },

        "tomorrow_actions": []
    }


    for customer in source.get(
        "customers",
        []
    ):

        decision = decide_priority(customer)

        result["tomorrow_actions"].append({

            "customer_id":
                customer.get("customer_id"),

            "current_status":
                customer.get("deal_status"),

            "priority":
                decision["priority"],

            "recommended_action":
                decision["action"],

            "required_checks":
                customer.get(
                    "next_action",
                    []
                ),

            "payment_state":
                customer.get(
                    "signal",
                    {}
                ).get(
                    "payment"
                )
        })


    save_json(
        OUTPUT,
        result
    )


    print("CUSTOMER DEAL ACTION PLAN COMPLETE")
    print("OUTPUT:", OUTPUT)


if __name__ == "__main__":
    main()
