import os, sys, json, time, math, hashlib, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
NDJSON_PATH = os.path.join(DATA_STORE, "embedded_base.ndjson")

PSI_FACTOR = 0.318999999139
MAX_SAFE_VOLTAGE_MV = 3300.0

class MasterPipeline:
    @staticmethod
    def analyze_tone(text):
        pos = sum(1 for w in ["よし", "完璧", "安泰", "成功", "最高", "完成"] if w in text)
        neg = sum(1 for w in ["惜しい", "エラー", "ダメ", "失敗"] if w in text)
        ana = sum(1 for w in ["アルゴリズム", "JSON", "基盤", "構造", "コード"] if w in text)
        
        pol = round((pos - neg) / (pos + neg), 2) if (pos + neg) > 0 else 0.0
        tone = "LOGICAL_ANALYSIS" if ana > 0 and (pos + neg) == 0 else (
            "POSITIVE_PASSION" if pol > 0.2 else ("CRITICAL_CAUTION" if pol < -0.2 else "NEUTRAL_BALANCED")
        )
        return tone, pol

    @staticmethod
    def read_latest_context(limit=3):
        if not os.path.exists(NDJSON_PATH):
            return []
        records = []
        with open(NDJSON_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try: records.append(json.loads(line))
                    except: continue
        return records[-limit:]

    @classmethod
    def execute(cls, raw_input=None):
        if not raw_input:
            raw_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "100%マスターパイプライン起動"

        raw_bytes = raw_input.encode('utf-8')
        pulse_len = len(raw_bytes)

        # 1. PSI共鳴 & 電圧計算
        raw_psi = abs(math.sin(pulse_len * PSI_FACTOR))
        resonance_pct = round(raw_psi * 100, 2)
        safe_v = min(pulse_len * PSI_FACTOR * 12.0, MAX_SAFE_VOLTAGE_MV)

        # 2. 感情トーン解析
        tone, polarity = cls.analyze_tone(raw_input)

        # 3. 過去文脈の継承
        prev_context = cls.read_latest_context(2)

        # 4. 100% 構造化統合パケット
        packet = {
            "$schema": "https://belphegor.dev/schemas/v100/master-pipeline.json",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "telemetry": {
                "resonance_pct": f"{resonance_pct}%",
                "voltage_mv": round(safe_v, 2),
                "payload_hash": hashlib.sha256(raw_bytes).hexdigest()[:16]
            },
            "meta_analysis": {
                "declared_tone": tone,
                "polarity": polarity
            },
            "payload": raw_input,
            "inherited_context_count": len(prev_context)
        }

        # 保存
        os.makedirs(DATA_STORE, exist_ok=True)
        with open(NDJSON_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(packet, ensure_ascii=False) + "\n")

        print(f"\033[1;32m[100% MASTER PIPELINE]\033[0m 処理完了 | 共鳴: \033[1;36m{resonance_pct}%\033[0m | 電圧: \033[1;33m{round(safe_v,1)}mV\033[0m | Tone: \033[1;35m{tone}\033[0m")
        print(f"  └─ 継承文脈数: {len(prev_context)} 件 | ハッシュ: {packet['telemetry']['payload_hash']}")
        return packet

if __name__ == "__main__":
    MasterPipeline.execute()
