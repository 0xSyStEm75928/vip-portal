import json
from datetime import datetime, timezone

INPUT = "json_core/cli_target_discovery.json"
OUTPUT = "json_core/original_10_target_audit.json"


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


def classify_target(target, index):

    if index < 3:
        group = "ORIGINAL_3"
        review = "EARLY_TARGET_REVIEW"
    else:
        group = "DISCOVERY_7"
        review = "PUBLIC_DISCOVERY_REVIEW"

    return {

        "name":
            target.get("name"),

        "url":
            target.get("url"),

        "stars":
            target.get("stars"),

        "language":
            target.get("language"),

        "group":
            group,

        "review_stage":
            review,

        "evidence": {

            "public_presence":
                True,

            "contact_history":
                "UNVERIFIED",

            "private_interest":
                "UNVERIFIED",

            "silent_view":
                "UNVERIFIED",

            "business_intent":
                "UNVERIFIED"
        },

        "next_check": [

            "verify_public_contact",
            "verify_project_alignment",
            "human_message_required"

        ]

    }


def main():

    source = load_json(INPUT)

    targets = source.get(
        "targets",
        []
    )


    result = {

        "version":
            "1.0.0",

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "policy": {

            "public_data_only":
                True,

            "no_hidden_monitoring_claim":
                True,

            "no_private_interest_assumption":
                True,

            "manual_review_required":
                True

        },

        "summary": {

            "total":
                len(targets),

            "original_3":
                min(3, len(targets)),

            "discovery_7":
                max(0, len(targets)-3)

        },


        "targets": [

            classify_target(t, i)

            for i, t in enumerate(targets)

        ]

    }


    save_json(
        OUTPUT,
        result
    )


    print(
        "ORIGINAL 10 TARGET AUDIT COMPLETE"
    )

    print(
        "OUTPUT:",
        OUTPUT
    )


if __name__ == "__main__":
    main()
