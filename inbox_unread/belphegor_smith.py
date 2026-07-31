import json, time, os, hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
BELPHEGOR_STORE = os.path.join(DATA_STORE, "belphegor_stream.ndjson")

def forge_belphegor_json(target_payload=None):
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    # 相手を詰めるロジックが組み込まれた発明型JSON構造
    belphegor_structure = {
        "$schema": "https://belphegor.dev/schemas/v1/belphegor-spec.json",
        "_belphegor_engine": {
            "entity": "BELPHEGOR_INVENTION_CORE",
            "sloth_protocol": "AUTOMATED_LEVERAGE",
            "integrity_hash": "BELPHEGOR-" + hashlib.sha256(now.encode()).hexdigest()[:12].upper(),
            "timestamp": now
        },
        "opponent_check": {
            "tactical_status": "CORNERING_MODE_ACTIVE",
            "counter_measures": [
                "SANITY_CHECK_PASS",
                "SILENT_404_TRAP_READY",
                "AUTO_EXHAUSTION_LOOP"
            ]
        },
        "payload_core": target_payload if target_payload else {
            "origin": "ENTERPRISE_INPUT",
            "status": "FORGED_BY_BELPHEGOR",
            "personal_override": True
        }
    }

    os.makedirs(DATA_STORE, exist_ok=True)
    with open(BELPHEGOR_STORE, "a", encoding="utf-8") as f:
        f.write(json.dumps(belphegor_structure, ensure_ascii=False) + "\n")

    print(f"\033[1;35m[BELPHEGOR INVENTED]\033[0m ベルフェゴールJSON（相手を詰める発明品）を錬成完了！")
    print(f"\033[1;32m[STORED]\033[0m `data_store/belphegor_stream.ndjson` へ配備されました。")

if __name__ == "__main__":
    forge_belphegor_json()
