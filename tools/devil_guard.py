import sys, json, re, time, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_LOG_PATH = os.path.join(BASE_DIR, "data_store", "shared_stream.ndjson")

# 承認済みユニークトークン（環境変数やGitHub Secretからも拡張可能）
AUTHORIZED_UNIQUE_TOKENS = {
    "uv_devil_vip_888": "VIP_Client_Alpha",
    "uv_silent_pass_777": "Silent_Observer_Beta"
}

class DevilGuard:
    MALICIOUS_PATTERNS = [
        r"<script.*?>", r"javascript:", r"eval\(", r"exec\(",
        r"system\(", r"__import__", r"\.\./", r"<iframe", r"onload=", r"onerror="
    ]

    @classmethod
    def inspect_and_sanitize(cls, raw_input, token=""):
        # 1. 認めた顧客（Fast Pass）判定
        user_id = AUTHORIZED_UNIQUE_TOKENS.get(token, "Guest_Observer")

        # 2. 長さ制限（スパム防止：最大100文字）
        if not raw_input or len(raw_input) > 100:
            return None, "404: Input length exceeded"

        # 3. 悪意あるパターンの検知
        for pattern in cls.MALICIOUS_PATTERNS:
            if re.search(pattern, raw_input, re.IGNORECASE):
                return None, f"404: Malicious pattern detected ({pattern})"

        # 4. サニタイズ（HTML特殊文字のエスケープ）
        clean_text = (
            raw_input.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
            .strip()
        )

        return clean_text, user_id

def append_to_stream(raw_input, token=""):
    clean_msg, user_or_err = DevilGuard.inspect_and_sanitize(raw_input, token)
    
    if clean_msg is None:
        print(f"\033[1;31m[404 SILENT KILL]\033[0m {user_or_err} ➔ 破棄")
        sys.exit(1) # GitHub Actions側でエラー扱い（404サイレント閉鎖へ）

    now = time.time()
    event = {
        "id": f"msg_{int(now*1000)}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "user": user_or_err,
        "message": clean_msg
    }

    os.makedirs(os.path.dirname(SHARED_LOG_PATH), exist_ok=True)
    with open(SHARED_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"\033[1;32m[LOG ACCEPTED]\033[0m ({user_or_err}): \"{clean_msg}\"")
    return True

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else ""
    token = sys.argv[2] if len(sys.argv) > 2 else ""
    append_to_stream(msg, token)
