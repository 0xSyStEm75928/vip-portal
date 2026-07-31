import json

INPUT = "json_core/original_10_target_priority.json"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print("CLI TARGET REVIEW REPORT")
print("=" * 80)

for i, t in enumerate(data.get("targets", []), 1):
    print(f"[{i}] {t['name']}")
    print(f"  Priority : {t['priority']}")
    print(f"  Group    : {t['group']}")
    print(f"  Stars    : {t['stars']}")
    print(f"  Contact  : {t['contact_state']}")
    print(f"  Review   : {t['review_stage']}")
    print(f"  Interest : {t['interest']}")
    print(f"  URL      : {t['url']}")
    print("-" * 80)

print("TOTAL:", len(data.get("targets", [])))
