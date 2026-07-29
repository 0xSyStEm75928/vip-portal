import json
import os
from datetime import datetime, timezone

BASE = "json_core"

FILES = {
    "deal": os.path.join(BASE, "customer_real_deal_review.json"),
    "customer": os.path.join(BASE, "ZERO_CORE.customer.json"),
    "queue": os.path.join(BASE, "customer_review_queue.json")
}

OUTPUT = os.path.join(
    BASE,
    "customer_deal_sync_result.json"
)


def load_json(path):
    if not os.path.exists(path):
        return {}
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


def find_customer(customers, cid):
    if isinstance(customers, dict):
        if cid in customers:
            val = customers[cid]
            return val if isinstance(val, dict) else {'customer_id': cid}
        for k, v in customers.items():
            if isinstance(v, dict) and v.get('customer_id') == cid:
                return v
    elif isinstance(customers, list):
        for c in customers:
            if isinstance(c, dict) and c.get('customer_id') == cid:
                return c
    return None
def find_queue(data, cid):

    queue = data.get("queue", [])

    for q in queue:
        if (
            q.get("customer_id") == cid
            or q.get("target_id") == cid
        ):
            return q

    return None


def main():

    deal = load_json(FILES["deal"])
    customer = load_json(FILES["customer"])
    queue = load_json(FILES["queue"])

    result = {
        "version": "1.0.0",

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "policy": {
            "read_only_check": True,
            "no_state_change": True,
            "evidence_required": True
        },

        "customers": []
    }


    for item in deal.get("customers", []):

        cid = item.get("customer_id")

        result["customers"].append({

            "customer_id": cid,

            "deal_status":
                item.get("status"),

            "signal":
                item.get("signal"),

            "existing_customer_record":
                "FOUND"
                if find_customer(customer, cid)
                else "NOT_FOUND",

            "queue_record":
                "FOUND"
                if find_queue(queue, cid)
                else "NOT_FOUND",

            "next_action":
                item.get("review", {})
                .get("next_check", [])
        })


    save_json(
        OUTPUT,
        result
    )

    print("CUSTOMER DEAL SYNC CHECK COMPLETE")
    print("OUTPUT:", OUTPUT)


if __name__ == "__main__":
    main()
