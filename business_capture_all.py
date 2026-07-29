import json
import os
import hashlib
from datetime import datetime, timezone

BASE = "json_core"
OUTPUT = os.path.join(BASE, "business_capture_all.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(65536)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


bundle = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),
    "status": "CAPTURED",
    "summary": {
        "total_files": 0,
        "valid_json": 0,
        "invalid_json": 0
    },
    "files": []
}

if os.path.isdir(BASE):

    for name in sorted(os.listdir(BASE)):

        if not name.endswith(".json"):
            continue

        path = os.path.join(BASE, name)

        item = {
            "file": name,
            "size": os.path.getsize(path),
            "sha256": sha256(path),
            "valid_json": False
        }

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            item["valid_json"] = True
            item["root_type"] = type(data).__name__

            if isinstance(data, dict):
                item["keys"] = sorted(list(data.keys()))

            bundle["summary"]["valid_json"] += 1

        except Exception as e:
            item["error"] = str(e)
            bundle["summary"]["invalid_json"] += 1

        bundle["files"].append(item)

bundle["summary"]["total_files"] = len(bundle["files"])

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        bundle,
        f,
        indent=2,
        ensure_ascii=False
    )

print("=" * 72)
print("BUSINESS CAPTURE COMPLETE")
print("FILES :", bundle["summary"]["total_files"])
print("VALID :", bundle["summary"]["valid_json"])
print("INVALID :", bundle["summary"]["invalid_json"])
print("OUTPUT :", OUTPUT)
print("=" * 72)
