import json
from datetime import datetime, timezone

INPUT = "json_core/cli_business_candidate_review.json"
OUTPUT = "json_core/cli_business_signal_deep_review.json"


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


def evaluate(candidate):

    signals = candidate.get("signals", [])

    priority = candidate.get("priority", "C")

    if priority == "A":
        approach = "TECHNICAL_BUSINESS_REVIEW"
    elif priority == "B":
        approach = "PUBLIC_PROFILE_REVIEW"
    else:
        approach = "LOW_PRIORITY_REVIEW"

    return {
        "name": candidate.get("name"),
        "url": candidate.get("url"),
        "stars": candidate.get("stars"),

        "public_signal": {
            "repository_exists": True,
            "public_activity": "UNVERIFIED",
            "maintainer_contact": "UNVERIFIED",
            "commercial_presence": "UNVERIFIED"
        },

        "technical_signal": {
            "matched_keywords": signals,
            "architecture_fit": candidate.get(
                "technical_match",
                "UNVERIFIED"
            )
        },

        "business_evaluation": {
            "contact_possible": "POSSIBLE",
            "partnership_fit": "UNVERIFIED",
            "purchase_intent": "UNVERIFIED"
        },

        "decision": {
            "priority": priority,
            "next_action": approach
        }
    }


def main():

    source = load_json(INPUT)

    candidates = source.get(
        "candidates",
        []
    )

    result = {
        "version": "1.0.0",

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "policy": {
            "public_data_only": True,
            "no_hidden_view_claim": True,
            "manual_confirmation_required": True
        },

        "summary": {
            "total_candidates": len(candidates)
        },

        "reviewed_candidates": [
            evaluate(c)
            for c in candidates
        ]
    }

    save_json(
        OUTPUT,
        result
    )

    print("CLI BUSINESS SIGNAL DEEP REVIEW COMPLETE")
    print("TARGETS:", len(candidates))
    print("OUTPUT:", OUTPUT)


if __name__ == "__main__":
    main()
