import json
import os
from datetime import datetime, timezone, timedelta

BASE = "json_core"

CORE_FILE = os.path.join(
    BASE,
    "ZERO_CORE.customer.json"
)

PLAN_FILE = os.path.join(
    BASE,
    "tomorrow_operation_plan.json"
)

QUEUE_FILE = os.path.join(
    BASE,
    "customer_review_queue.json"
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


def dispatch():

    timestamp = now_jst()

    core = load(
        CORE_FILE
    )

    plan = load(
        PLAN_FILE
    )

    queue = load(
        QUEUE_FILE
    )


    plan.setdefault(
        "tasks",
        []
    )

    queue.setdefault(
        "pending_reviews",
        []
    )


    for customer_id, customer in core.get(
        "customers",
        {}
    ).items():

        if customer.get(
            "status"
        ) != "VERIFIED":

            continue


        task = {
            "task_id":
                "TASK_" + customer_id,

            "target_id":
                customer_id,

            "action":
                "CONFIRM_NEXT_BUSINESS_STEP",

            "created_at":
                timestamp
        }


        review = {
            "queue_id":
                "Q_" + customer_id,

            "target_id":
                customer_id,

            "priority":
                "A",

            "next_action":
                "HUMAN_CONFIRMATION",

            "requires_approval":
                True,

            "created_at":
                timestamp
        }


        plan["tasks"].append(
            task
        )

        queue["pending_reviews"].append(
            review
        )


    plan["updated_at"] = timestamp
    queue["updated_at"] = timestamp


    save(
        PLAN_FILE,
        plan
    )

    save(
        QUEUE_FILE,
        queue
    )


    print(
        "[DISPATCH SYNC COMPLETE]"
    )

    print(
        "PERSISTENCE -> PLAN -> REVIEW_QUEUE"
    )


if __name__ == "__main__":
    dispatch()
