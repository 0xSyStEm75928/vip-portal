import json
import os
from datetime import datetime, timezone, timedelta


BASE = "json_core"

OUTPUT = os.path.join(
    BASE,
    "dag_integrity_report.json"
)

JST = timezone(
    timedelta(hours=9)
)


NODES = {
    "INGRESS": os.path.join(
        BASE,
        "cli_contact_evidence_registry.json"
    ),

    "GATE": os.path.join(
        BASE,
        "customer_lifecycle_gate.json"
    ),

    "PERSISTENCE": os.path.join(
        BASE,
        "ZERO_CORE.customer.json"
    ),

    "PLAN": os.path.join(
        BASE,
        "tomorrow_operation_plan.json"
    ),

    "REVIEW": os.path.join(
        BASE,
        "customer_review_queue.json"
    )
}


EDGES = [
    ["INGRESS", "GATE"],
    ["GATE", "PERSISTENCE"],
    ["PERSISTENCE", "PLAN"],
    ["PLAN", "REVIEW"]
]


def now_jst():
    return datetime.now(JST).isoformat()


def check_json(path):

    if not os.path.exists(path):
        return {
            "exists": False,
            "valid_json": False
        }

    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            json.load(f)

        return {
            "exists": True,
            "valid_json": True
        }

    except Exception as e:

        return {
            "exists": True,
            "valid_json": False,
            "error": str(e)
        }


def check_dag():

    visited = set()
    path = []

    def visit(node):

        if node in path:
            return False

        if node in visited:
            return True

        path.append(node)

        for edge in EDGES:

            if edge[0] == node:

                if not visit(edge[1]):
                    return False

        path.pop()
        visited.add(node)

        return True


    return visit("INGRESS")


def main():

    result = {

        "version": "1.0.0",

        "generated_at":
            now_jst(),

        "mode":
            "READ_ONLY",

        "nodes":
            {},

        "dag": {

            "acyclic":
                check_dag(),

            "edges":
                EDGES
        },

        "status":
            "UNKNOWN"
    }


    healthy = True


    for name, path in NODES.items():

        result["nodes"][name] = {
            "path": path,
            **check_json(path)
        }

        if not result["nodes"][name]["valid_json"]:
            healthy = False


    if not result["dag"]["acyclic"]:
        healthy = False


    result["status"] = (
        "HEALTHY"
        if healthy
        else "CHECK_REQUIRED"
    )


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
        "DAG INTEGRITY CHECK COMPLETE"
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
