import json
import os
from datetime import datetime, timezone

BASE = "json_core"

GROUPS = {
    "lower_layer": [],
    "middle_layer": [],
    "upper_layer": []
}

OUTPUT = os.path.join(
    BASE,
    "business_layer_bundle.json"
)


def load(path):
    full = os.path.join(BASE, path)

    if not os.path.exists(full):
        return None

    with open(full, "r", encoding="utf-8") as f:
        return json.load(f)


bundle = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "layer": {
        "lower": {},
        "middle": {},
        "upper": {}
    }
}

for name in GROUPS["lower_layer"]:
    bundle["layer"]["lower"][name] = load(name)

for name in GROUPS["middle_layer"]:
    bundle["layer"]["middle"][name] = load(name)

for name in GROUPS["upper_layer"]:
    bundle["layer"]["upper"][name] = load(name)

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

print("BUSINESS LAYER BUNDLE COMPLETE")
print("OUTPUT:", OUTPUT)
