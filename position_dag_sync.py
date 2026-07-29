import json
import os
from datetime import datetime, timezone, timedelta


BASE = "json_core"

MANIFEST = "current_position_manifest.json"

REPORT = os.path.join(
    BASE,
    "dag_integrity_report.json"
)

OUTPUT = os.path.join(
    BASE,
    "position_dag_sync_status.json"
)


JST = timezone(
    timedelta(hours=9)
)


def now_jst():
    return datetime.now(JST).isoformat()


def load(path):

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save(path, data):

    tmp = path + ".tmp"

    with open(
        tmp,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    os.replace(
        tmp,
        path
    )


def main():

    manifest = load(
        MANIFEST
    )

    report = load(
        REPORT
    )


    dag_status = report.get(
        "status",
        "UNKNOWN"
    )


    current_anchor = manifest.get(
        "current_task_anchor",
        {}
    )


    result = {

        "version": "1.0.0",

        "generated_at":
            now_jst(),

        "purpose":
            "Current position and DAG state alignment",

        "position": {

            "phase":
                current_anchor.get(
                    "phase",
                    "UNKNOWN"
                ),

            "state":
                current_anchor.get(
                    "state",
                    "UNKNOWN"
                ),

            "timestamp":
                current_anchor.get(
                    "timestamp_jst"
                )
        },


        "dag_state": {

            "integrity":
                dag_status,

            "acyclic":
                report.get(
                    "dag",
                    {}
                ).get(
                    "acyclic",
                    False
                )
        },


        "execution_gate": {

            "allowed":
                dag_status == "HEALTHY",

            "reason":
                "DAG_VALIDATED"
                if dag_status == "HEALTHY"
                else "DAG_CHECK_REQUIRED"
        },


        "next_position": {

            "current":
                "DAG_POSITION_ALIGNED",

            "next":
                "WAIT_FOR_EVENT_INPUT"

        }
    }


    save(
        OUTPUT,
        result
    )


    print(
        "POSITION DAG SYNC COMPLETE"
    )

    print(
        "STATUS:",
        result["execution_gate"]["reason"]
    )

    print(
        "OUTPUT:",
        OUTPUT
    )


if __name__ == "__main__":
    main()
