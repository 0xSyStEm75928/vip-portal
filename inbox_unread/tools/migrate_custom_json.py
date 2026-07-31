import json, os, sys, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
PROCESSED_LOG = os.path.join(DATA_STORE, "optimized_master.ndjson")

def process_custom_json(input_json_path):
    if not os.path.exists(input_json_path):
        print(f"\033[1;31m[ERROR]\033[0m ファイルが見つかりません: {input_json_path}")
        return

    print(f"\033[1;36m[MIGRATING]\033[0m 企業向けJSON \"{input_json_path}\" を個人最強フォーマットへ移植中...")

    try:
        with open(input_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 配列でも単一オブジェクトでも柔軟にNDJSON化
        items = data if isinstance(data, list) else [data]
        
        os.makedirs(DATA_STORE, exist_ok=True)
        count = 0
        with open(PROCESSED_LOG, "a", encoding="utf-8") as out_f:
            for item in items:
                record = {
                    "_imported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "_guard_status": "VERIFIED_PERSONAL",
                    "payload": item
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1

        print(f"\033[1;32m[SUCCESS]\033[0m {count} 件のデータを 『optimized_master.ndjson』 に統合完了！")

    except Exception as e:
        print(f"\033[1;31m[404 SILENT KILL]\033[0m JSON構造解析失敗: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.json"
    process_custom_json(target)
