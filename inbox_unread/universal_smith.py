import os, sys, json, platform, time, hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
DOMINATION_STORE = os.path.join(DATA_STORE, "domination_blend.ndjson")

# 3:318...9999^1 式による「極限3層」マトリックス
CONDENSED_MATRIX = {
    "1": {"brand": "MJSON (Micro-Core)", "spec": "PACKET_MINIMAL_CORE", "ratio": "33.3%"},
    "2": {"brand": "SJSON (Silent-Armor)", "spec": "STEALTH_404_PROTECT", "ratio": "66.6%"},
    "3": {"brand": "ForgeJSON (A-Forge)", "spec": "CONDENSED_HEAVY_SMITH", "ratio": "99.9% (COMPLETE)"}
}

class UniversalJSONSmith:
    @classmethod
    def process_condensed_equation(cls, num_str="3"):
        num = num_str if num_str in CONDENSED_MATRIX else "3"
        target = CONDENSED_MATRIX[num]
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # 計算式 3 * 318...9999^1 によるメタの等倍還元処理
        payload = {
            "equation_applied": "3 * (318...9999)^1",
            "condensed_no": f"NO_{num}",
            "brand": target["brand"],
            "spec": target["spec"],
            "status": "PERFECT_BALANCED"
        }

        raw_str = json.dumps(payload, ensure_ascii=False)
        blend_hash = hashlib.sha256((raw_str + timestamp).encode('utf-8')).hexdigest()[:10]

        armored_json = {
            "$schema": "dhjson/v3/condensed-3tier",
            "_equation_header": {
                "algorithm_no": int(num),
                "brand": target["brand"],
                "condensed_spec": target["spec"],
                "equation_hash": f"EQ1-{blend_hash.upper()}",
                "timestamp": timestamp
            },
            "_inner_core": payload
        }

        os.makedirs(DATA_STORE, exist_ok=True)
        with open(DOMINATION_STORE, "a", encoding="utf-8") as f:
            f.write(json.dumps(armored_json, ensure_ascii=False) + "\n")

        print(f"\033[1;33m[EQUATION CALCULATED]\033[0m 318...9999^1 式を適用 ➔ \033[1;35m{target['brand']}\033[0m")
        print(f"\033[1;32m[CONDENSED SUCCESS]\033[0m 3層凝縮アルゴリズム No.{num} を自律配置完了！")

if __name__ == "__main__":
    opt = sys.argv[1] if len(sys.argv) > 1 else "3"
    UniversalJSONSmith.process_condensed_equation(opt)
