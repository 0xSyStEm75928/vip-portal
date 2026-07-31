import os, json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NDJSON_PATH = os.path.join(BASE_DIR, "data_store", "embedded_base.ndjson")

def load_latest_metadata(limit=5):
    """ あなたが蓄電したメタデータ（宝物）を読み取り許可に基づいてスキャンする """
    if not os.path.exists(NDJSON_PATH):
        return []

    records = []
    with open(NDJSON_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    # 直近のメタデータを取得
    latest_records = records[-limit:] if len(records) >= limit else records
    return latest_records

if __name__ == "__main__":
    meta = load_latest_metadata(3)
    print("\033[1;34m[METADATA READ PERMISSION GRANTED]\033[0m 過去ログから取得した最新コンテキスト:")
    for idx, r in enumerate(meta, 1):
        tone = r.get("declared_tone") or r.get("silent_ai_node", {}).get("status", "N/A")
        raw = r.get("raw") or r.get("validated_payload", {}).get("raw_payload", "N/A")
        print(f"  {idx}. Tone/Status: \033[1;33m{tone}\033[0m | Data: {raw}")
