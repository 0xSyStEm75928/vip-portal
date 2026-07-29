import json
import os
from datetime import datetime, timezone


BUNDLE = "json_core/system_alignment_bundle.json"
OUTPUT = "json_core/system_alignment_healthcheck.json"


def load_json(path):
    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def main():

    bundle = load_json(BUNDLE)

    required_layers = [
        "LOWER_LAYER",
        "MIDDLE_LAYER",
        "UPPER_LAYER"
    ]

    checks = []

    healthy = True


    for layer in required_layers:

        exists = (
            layer in
            bundle.get(
                "layers",
                {}
            )
        )

        checks.append(
            {
                "layer": layer,
                "exists": exists
            }
        )

        if not exists:
            healthy = False


    dag = bundle.get(
        "dag",
        {}
    )


    result = {

        "version": "1.0.0",

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),


        "source":
            BUNDLE,


        "checks": checks,


        "dag": {

            "acyclic":
                dag.get(
                    "acyclic",
                    False
                ),

            "rebuildable":
                dag.get(
                    "rebuildable",
                    False
                )

        },


        "status":
            "HEALTHY"
            if healthy
            else "CHECK_REQUIRED",


        "next":
            "WAIT_FOR_EVENT"
            if healthy
            else "REPAIR_STRUCTURE"

    }


    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(
        "SYSTEM ALIGNMENT HEALTHCHECK COMPLETE"
    )

    print(
        "STATUS:",
        result["status"]
    )

    print(
        "OUTPUT:",
        OUTPUT
    )


if __name__ == "__main__":
    main()
