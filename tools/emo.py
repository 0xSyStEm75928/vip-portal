import os, sys, json, time

p = "data_store/embedded_base.ndjson"
os.makedirs("data_store", exist_ok=True)
raw = " ".join(sys.argv[1:]) or "パルス"

pos = sum(1 for w in ["よし","完璧","安泰","成功","最高","完成"] if w in raw)
neg = sum(1 for w in ["惜しい","エラー","ダメ","失敗"] if w in raw)
ana = sum(1 for w in ["アルゴリズム","JSON","基盤","構造"] if w in raw)

pol = round((pos - neg) / (pos + neg), 2) if (pos + neg) > 0 else 0.0
tone = "LOGICAL_ANALYSIS" if ana > 0 and (pos + neg) == 0 else ("POSITIVE_PASSION" if pol > 0.2 else ("CRITICAL_CAUTION" if pol < -0.2 else "NEUTRAL_BALANCED"))

rec = {
    "$schema": "v6/emotion-embedded",
    "declared_tone": tone,
    "polarity": pol,
    "raw": raw,
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
}

with open(p, "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"\033[1;32m[EMOTION]\033[0m Tone: {tone} | Polarity: {pol} | 蓄電完了")
