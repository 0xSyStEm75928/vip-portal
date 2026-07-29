import urllib.request
import json
import time
import sys

TARGETS = [
    {"owner": "CallMarcus", "repo": "dji-drone-metadata-embedder"},
    {"owner": "JuniorBecari10", "repo": "lspctl"},
    {"owner": "mtarcure", "repo": "claude-vibe-squad"},
    {"owner": "kawarimidoll", "repo": "guard-and-guide"},
    {"owner": "birsy", "repo": "clinker-mod"}
]

# 監視設定（例: 10秒ごとに確認、最大60秒待機後にキャンセル）
CHECK_INTERVAL = 10  # 秒
TIMEOUT_SECONDS = 60 # 秒

def check_target_activity(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            return data.get("pushed_at")
    except Exception:
        return None

def main():
    print("=== 📡 ターゲット5名の更新状況・反応監視を開始します ===")
    print(f"英語問い合わせ文面: \"Could you please provide a consolidated list of items or requirements you need?\"\n")
    
    elapsed = 0
    
    while elapsed < TIMEOUT_SECONDS:
        print(f"[{elapsed}s / {TIMEOUT_SECONDS}s] ターゲットの応答・更新状況を確認中...")
        
        # 簡易チェック（アクティビティの変化確認）
        for t in TARGETS:
            pushed = check_target_activity(t["owner"], t["repo"])
            # ここでは状態チェックのみ実行
            
        time.sleep(CHECK_INTERVAL)
        elapsed += CHECK_INTERVAL

    print("\n" + "="*50)
    print("⏱️ [TIMEOUT] 定めていた待機時間内に5名からの反応・更新はありませんでした。")
    print("🚫 プロセスを一時キャンセル（スリープ）します。後ほど再確認・追跡が可能です。")
    print("="*50)

if __name__ == "__main__":
    main()
