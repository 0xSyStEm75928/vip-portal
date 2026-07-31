import os, sys, json, time, re, hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
EMBEDDED_STORE = os.path.join(DATA_STORE, "embedded_base.ndjson")

class SilentAIEngine:
    """ 無応答AIエンジン：会話を一切せず、データ精査と構造化のみに徹底する """
    @staticmethod
    def process_silently(raw_input):
        # 1. データのクレンジング（ノイズ除去）
        cleaned = re.sub(r'[\r\n\t]+', ' ', str(raw_input)).strip()
        
        # 2. メタデータ＆データ品質スコアの自動算定（バックグラウンド評価）
        byte_len = len(cleaned.encode('utf-8'))
        has_code = bool(re.search(r'[{}\[\]\(\)=><;]', cleaned))
        
        # 3. 無応答AIによる判定タグ付け
        data_type = "CODE_PULSE" if has_code else "TEXT_PULSE"
        integrity_score = min(1.0, round(byte_len / 100.0, 2)) if byte_len > 0 else 0.0
        
        return {
            "type": data_type,
            "raw_payload": cleaned,
            "byte_size": byte_len,
            "integrity_score": integrity_score,
            "hash_signature": hashlib.sha256(cleaned.encode()).hexdigest()[:16]
        }

class EmbeddedJSONBase:
    """ 内蔵型JSON基盤：無応答AIの解析結果を安全に永続化する """
    @classmethod
    def ingest(cls, input_data=None):
        # 入力の受け取り（CLI引数 または 標準入力）
        if not input_data:
            if not sys.stdin.isatty():
                input_data = sys.stdin.read().strip()
            elif len(sys.argv) > 1:
                input_data = " ".join(sys.argv[1:])
            else:
                input_data = "DEFAULT_SYSTEM_CHECK"

        # 無応答AIエンジンによる裏方処理
        ai_result = SilentAIEngine.process_silently(input_data)
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # 堅牢な統合JSONレコード
        record = {
            "$schema": "https://belphegor.dev/schemas/v5/embedded-silent-core.json",
            "system_layer": "EMBEDDED_JSON_BASE",
            "silent_ai_node": {
                "status": "SILENT_PROCESSING_COMPLETE",
                "response_mode": "NO_CHAT_DATA_ONLY",
                "processed_at": now
            },
            "validated_payload": ai_result
        }

        # 永続化ストレージへの書き込み
        os.makedirs(DATA_STORE, exist_ok=True)
        with open(EMBEDDED_STORE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # ターミナル側にはログのみ出力（無駄なお喋りはしない）
        print(f"\033[1;32m[SILENT AI CORE]\033[0m 構造化完了 | Type: \033[1;33m{ai_result['type']}\033[0m | Hash: \033[1;36m{ai_result['hash_signature']}\033[0m | 蓄電完了")
        return record

if __name__ == "__main__":
    EmbeddedJSONBase.ingest()
