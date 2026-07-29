import sys, json, re, time, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_LOG_PATH = os.path.join(BASE_DIR, "data_store", "shared_stream.ndjson")

class DevilGuard:
    # 悪意あるパターン（HTML/JSインジェクション、コマンド実行など）
    MALICIOUS_PATTERNS = [
        r"<script.*?>", r"javascript:", r"eval\(", r"exec\(",
        r"system\(", r"__import__", r"../", r"<iframe"
    ]

    @classmethod
    def inspect_and_sanitize(cls, raw_user_input, user_id="anonymous"):
        # 1. 巨大入力（スパム）のガード (100文字制限)
        if not raw_user_input or len(raw_user_input) > 100:
            return cls.trigger_404_silent_kill("入力長オーバー")

        # 2. 危険なキーワード/パターンの検知
        for pattern in cls.MALICIOUS_PATTERNS:
            if re.search(pattern, raw_user_input, re.IGNORECASE):
                return cls.trigger_404_silent_kill(f"攻撃検知: {pattern}")

        # 3. 特殊文字のエスケープ（完全無害化）
        clean_text = (
            raw_user_input.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
            .strip()
        )

        return clean_text

    @staticmethod
    def trigger_404_silent_kill(reason):
        print(f"\033[1;31m[404 NOT FOUND]\033[0m 契約違反検知: {reason} ➔ 存在を隠蔽してサイレント破棄")
        # Webサーバー連携時はここで HTTP 404 Status Code を返して接続を切る
        return None

def write_shared_log(user_input, user_id="anon"):
    clean_msg = DevilGuard.inspect_and_sanitize(user_input, user_id)
    
    if clean_msg is None:
        # 404弾き発生（ログに書かずに終了）
        return False

    now = time.time()
    event = {
        "id": f"msg_{int(now*1000)}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "user": user_id,
        "message": clean_msg
    }

    os.makedirs(os.path.dirname(SHARED_LOG_PATH), exist_ok=True)
    with open(SHARED_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"\033[1;32m[LOG ACCEPTED]\033[0m 安全なログとして契約承認: \"{clean_msg}\"")
    return True

if __name__ == "__main__":
    test_input = sys.argv[1] if len(sys.argv) > 1 else "Hello World!"
    write_shared_log(test_input)
