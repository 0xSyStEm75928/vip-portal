import json

part_files = [
    "sovereign_part1.json",
    "sovereign_part2.json",
    "sovereign_part3.json",
    "sovereign_part4.json",
    "sovereign_part5.json"
]

master_config = {}

for file in part_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            master_config.update(data)
    except Exception as e:
        print(f"[!] Error loading {file}: {e}")

with open("master_sovereign_config.json", "w", encoding="utf-8") as out:
    json.dump(master_config, out, indent=2, ensure_ascii=False)

print("[SUCCESS] All 5 parts merged into 'master_sovereign_config.json'!")
