import sys, json, re, time, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_LOG_PATH = os.path.join(BASE_DIR, "data_store", "shared_stream.ndjson")

# 悪魔の契約を結んだ「ユニークビュー」のトークンリスト（認めた顧客）
AUTHORIZED_UNIQUE_TOKENS = {
    "uv_devil_vip_888": "VIP_Client_Alpha",
    "uv_silent_pass_777": "Silent_Observer_Beta"
}

class DevilGuard:
    MALICIOUS_PATTERNS = [
        r"<script.*?>", r"javascript:", r"eval\(", r"exec\(",
        r"system\(", r"__import__", r"../", r"<iframe"
    ]

    @classmethod
    def inspect_and_sanitize(cls, raw_user_input, token=None):
        # 1. 【ユニークビュー判定】認めた顧客トークンかチェック
        client_name = AUTHORIZED_UNIQUE_TOKENS.get(token)
        if client_name:
            # 認めたユニークビュー顧客 ➔ 軽量チェックで高速パス（Fast Pass）！
            print(f"\033[1;36m[UNIQUE VIEW]\033[0m 認めた顧客 '{client_name}' を確認。軽量通関します。")
        else:
            # 野良アクセス（未承認） ➔ 通常の厳密セキュリティ監査
            pass

        # 2. 巨大入力（スパム）のガード (100文字制限)
        if not raw_user_input or len(raw_user_input) > 100:
            return cls.trigger_404_silent_kill("入力長オーバー")

        # 3. 危険キーワードの検知
        for pattern in cls.MALICIOUS_PATTERNS:
            if re.search(pattern, raw_user_input, re.IGNORECASE):
                return cls.trigger_404_silent_kill(f"攻撃検知: {pattern}")

        # 4. サニタイズ処理
        clean_text = (
            raw_user_input.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
            .strip()
        )

        return clean_text, client_name or "Anonymous_Guest"

    @staticmethod
    def trigger_404_silent_kill(reason):
        print(f"\033[1;31m[404 NOT FOUND]\033[0m 未承認・異常アクセス検知: {reason} ➔ 存在を隠蔽してサイレント破棄")
        return None, None

def write_shared_log(user_input, token=None):
    clean_msg, user_id = DevilGuard.inspect_and_sanitize(user_input, token)
    
    if clean_msg is None:
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

    print(f"\033[1;32m[LOG ACCEPTED]\033[0m 契約承認 ({user_id}): \"{clean_msg}\"")
    return True

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello Unique View!"
    token = sys.argv[2] if len(sys.argv) > 2 else None
    write_shared_log(msg, token)
