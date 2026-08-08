#!/usr/bin/env python3
import os
import json
import hashlib
from datetime import datetime, timezone

ROOT = os.path.expanduser("~/ZERO_CORE")
STATE = os.path.join(ROOT, "PANDEMONIUM", "state")
RUN = os.path.join(ROOT, "EVIDENCE", "runtime")

OUT = os.path.join(STATE, "JSSH_PORTABLE.json")

FILES = {
    "dag_registry": "EVIDENCE/runtime/dag_registry_layer.json",
    "dag_runtime_binding": "EVIDENCE/runtime/dag_runtime_binding_layer.json",
    "control_panel": "EVIDENCE/runtime/zero_core_control_panel_layer.json",
    "panel_source": "PANDEMONIUM/state/zero_core_panel_source.json"
}


def read_json(rel):
    path = os.path.join(ROOT, rel)

    if not os.path.isfile(path):
        return {
            "state": "MISSING",
            "path": rel
        }

    try:
        with open(path, encoding="utf-8") as f:
            return {
                "state": "PRESENT",
                "data": json.load(f)
            }
    except Exception as e:
        return {
            "state": "INVALID",
            "path": rel,
            "error": str(e)
        }


def make_digest(data):
    raw = json.dumps(
        data,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":")
    ).encode("utf-8")

    return hashlib.sha256(raw).hexdigest()


def main():

    payload = {
        "schema": "JSSH.portable.v1",
        "type": "PORTABLE_RUNTIME",
        "version": 1,

        "identity": {
            "name": "JSSH",
            "description": "JSON Shell / Portable Runtime",
            "root": "ZERO_CORE"
        },

        "runtime": {
            "format": "JSON",
            "mode": "READ_ONLY",
            "transport": "PORTABLE",
            "projection": "JSON_NATIVE"
        },

        "license": {
            "number": "JSSH-2026-0001",
            "scope": "JSSH"
        },

        "payload": {
            name: read_json(path)
            for name, path in FILES.items()
        },

        "security": {
            "private_key": False,
            "seed_phrase": False,
            "secret_material": False,
            "signature_material": False,
            "transaction_execution": False,
            "broadcast": False
        },

        "created_at":
            datetime.now(timezone.utc).isoformat()
    }

    payload["integrity"] = {
        "algorithm": "sha256",
        "digest": make_digest(payload)
    }

    os.makedirs(STATE, exist_ok=True)

    tmp = OUT + ".tmp"

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(
            payload,
            f,
            indent=2,
            ensure_ascii=False
        )
        f.write("\n")

    os.replace(tmp, OUT)

    score = 0
    total = 0

    for item in payload["payload"].values():
        total += 1
        if item.get("state") == "PRESENT":
            score += 1

    if payload["license"]["number"]:
        score += 1
    total += 1

    percent = int((score / total) * 100)

    print("JSSH %d%%___" % percent)
    print("│≡ LICENSE No. ▫️ %s" %
          payload["license"]["number"])
    print("└#→ PORTABLE")
    print()
    print("JSSH_PORTABLE=GENERATED")
    print("SELF_CONTAINED=True")
    print("DIGEST=" + payload["integrity"]["digest"])
    print("OUT=" + OUT)


if __name__ == "__main__":
    main()
