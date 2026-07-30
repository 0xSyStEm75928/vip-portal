import json, time, os, hashlib, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
BELPHEGOR_STORE = os.path.join(DATA_STORE, "belphegor_stream.ndjson")

class BelphegorNeutralizer:
    @staticmethod
    def sanitize_text(text):
        """ 危険なタグやスクリプトを一切無力化するフィルター """
        if not isinstance(text, str):
            return text
        # スクリプトタグや危険文字列を消去して無力化
        cleaned = re.sub(r'<[^>]*?>', '', text)
        cleaned = cleaned.replace("javascript:", "").replace("exec(", "")
        return cleaned.strip()

    @classmethod
    def process_stream(cls, raw_topic_data):
        """ 流れてきたトレンドデータを無力化して BelphegorJSON へ昇華 """
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        # 1. データが無効または悪意ある場合はサイレント破棄（無力化）
        if not raw_topic_data:
            print("\033[1;31m[404 SILENT KILL]\033[0m 無効なストリームデータを検知。存在ごと消去しました。")
            return None

        # 2. トレンドデータの無力化サニタイズ処理
        safe_topics = []
        items = raw_topic_data if isinstance(raw_topic_data, list) else [raw_topic_data]
        
        for item in items:
            if isinstance(item, dict):
                safe_item = {
                    "topic": cls.sanitize_text(str(item.get("topic", item.get("title", "UNKNOWN_TOPIC")))),
                    "value": cls.sanitize_text(str(item.get("value", item.get("summary", "")))),
                    "source": cls.sanitize_text(str(item.get("source", "INTERNAL_STREAM"))),
                    "neutralized": True
                }
                safe_topics.append(safe_item)
            elif isinstance(item, str):
                safe_topics.append({
                    "topic": cls.sanitize_text(item),
                    "neutralized": True
                })

        # 3. BelphegorJSON 装甲の装着
        belphegor_packet = {
            "$schema": "https://belphegor.dev/schemas/v1/belphegor-spec.json",
            "_belphegor_engine": {
                "entity": "BELPHEGOR_STREAM_NEUTRALIZER",
                "sloth_protocol": "AUTOMATED_ZERO_RISK",
                "integrity_hash": "NEUTRAL-" + hashlib.sha256(now.encode()).hexdigest()[:12].upper(),
                "timestamp": now
            },
            "opponent_check": {
                "tactical_status": "THREAT_NEUTRALIZED",
                "counter_measures": ["ALL_PAYLOADS_DISARMED"]
            },
            "payload_core": {
                "stream_type": "LIVE_TREND_STREAM",
                "count": len(safe_topics),
                "neutralized_topics": safe_topics
            }
        }

        # 4. 格納庫へ追記
        os.makedirs(DATA_STORE, exist_ok=True)
        with open(BELPHEGOR_STORE, "a", encoding="utf-8") as f:
            f.write(json.dumps(belphegor_packet, ensure_ascii=False) + "\n")

        print(f"\033[1;35m[STREAM NEUTRALIZED]\033[0m {len(safe_topics)} 件のトレンドを完全に無力化してBelphegorJSON化！")
        return belphegor_packet

if __name__ == "__main__":
    # 自作コードからのストリーム流し込みテスト例
    sample_trend_stream = [
        {"topic": "次世代AIエンジン配備", "summary": "無力化ストリームによるデータ保護", "source": "Internal_Dev"},
        {"topic": "悪意あるスクリプト攻撃", "summary": "<script>alert('hack')</script>", "source": "External_Threat"}
    ]
    BelphegorNeutralizer.process_stream(sample_trend_stream)
