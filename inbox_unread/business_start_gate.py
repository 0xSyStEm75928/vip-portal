import json
import os
from datetime import datetime, timezone


CHECK_FILE = "json_core/system_alignment_healthcheck.json"
OUTPUT = "json_core/business_start_gate.json"


def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def main():

    check = load_json(
        CHECK_FILE
    )


    health = check.get(
        "status",
        "UNKNOWN"
    )


    allowed = (
        health == "HEALTHY"
    )


    result = {

        "version": "1.0.0",

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),


        "source":
            CHECK_FILE,


        "gate": {

            "status":
                "OPEN"
                if allowed
                else "CLOSED",

            "reason":
                "SYSTEM_ALIGNMENT_VALIDATED"
                if allowed
                else "SYSTEM_ALIGNMENT_REQUIRED"

        },


        "execution_policy": {

            "continue_existing_pipeline":
                allowed,

            "new_architecture_creation":
                False,

            "automatic_business_action":
                False,

            "human_confirmation_required":
                True

        }

    }


    save_json(
        OUTPUT,
        result
    )


    print(
        "BUSINESS START GATE COMPLETE"
    )

    print(
        "GATE:",
        result["gate"]["status"]
    )

    print(
        "OUTPUT:",
        OUTPUT
    )


if __name__ == "__main__":
    main()
