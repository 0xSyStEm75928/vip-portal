import json
import os
import subprocess
from datetime import datetime, timezone


GATE_FILE = "json_core/business_start_gate.json"

OUTPUT = "json_core/business_guarded_runner_result.json"


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

    gate = load_json(
        GATE_FILE
    )


    gate_status = gate.get(
        "gate",
        {}
    ).get(
        "status",
        "CLOSED"
    )


    result = {

        "version": "1.0.0",

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "gate":
            gate_status,


        "runner":

            {
                "executed":
                    False,

                "command":
                    "python3 business_master_runner.py",

                "return_code":
                    None
            }

    }


    if gate_status != "OPEN":

        result["runner"]["reason"] = (
            "START_GATE_CLOSED"
        )

        save_json(
            OUTPUT,
            result
        )

        print(
            "RUN BLOCKED BY START GATE"
        )

        return


    proc = subprocess.run(
        [
            "python3",
            "business_master_runner.py"
        ]
    )


    result["runner"]["executed"] = True

    result["runner"]["return_code"] = (
        proc.returncode
    )


    result["status"] = (
        "SUCCESS"
        if proc.returncode == 0
        else "FAILED"
    )


    save_json(
        OUTPUT,
        result
    )


    print(
        "BUSINESS GUARDED RUNNER COMPLETE"
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
