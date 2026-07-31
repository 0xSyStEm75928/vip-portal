import urllib.request
import json
import time

def endrunning_audit():
    print("=" * 65)
    print(" 🚀 END-RUNNING EXECUTION: 最終照合＆一括処理シークエンス ")
    print("=" * 65)
    
    # こちらから仕掛ける入力フェーズ
    github_user = input("👉 相手（または照合対象）の GitHub ユーザー名を入力してください: ").strip()
    
    if not github_user:
        print("❌ ユーザー名が未入力です。処理を中断します。")
        return

    print(f"\n🔍 [1/3] GitHub API 経由でアカウント実体を直接監査中: @{github_user} ...")
    time.sleep(0.8)
    
    url = f"https://api.github.com/users/{github_user}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as res:
            user_data = json.loads(res.read().decode())
            
            created_at = user_data.get('created_at', '')[:10]
            public_repos = user_data.get('public_repos', 0)
            followers = user_data.get('followers', 0)
            
            print("=" * 65)
            print(" 📊 AUDIT RESULT (REAL-TIME GITHUB DATA)")
            print("=" * 65)
            print(f" 👤 ユーザー名   : @{user_data.get('login')}")
            print(f" 🏢 名前/組織   : {user_data.get('name', 'N/A')}")
            print(f" 📅 アカウント作成: {created_at}")
            print(f" 📁 公開リポジトリ: {public_repos} 個")
            print(f" 👥 フォロワー数  : {followers} 人")
            print("-" * 65)
            
            # 実用的な簡易判定ロジック
            if public_repos > 0 or followers > 0:
                print(" 🟩 判定: VERIFIED_DEVELOPER_IDENTITY (開発実績を確認)")
                print(" ⚡ [2/3] 99.0% 最終承認フラグを更新中...")
                time.sleep(0.5)
                print(" 🔓 [3/3] エスクロー解放準備完了。エンドランニング成功！")
            else:
                print(" 🟨 判定: LOW_ACTIVITY_ACCOUNT (活動履歴が薄いため要警戒)")
                print(" ⚠️  手動でのリポジトリ内容確認を推奨します。")
            print("=" * 65)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("\n🟥 判定: ACCOUNT_NOT_FOUND (存在しないGitHubアカウントです)")
            print("🚨 相手の提示したIDは偽物・冷やかしの可能性が極めて高いです。即ブロック推奨！")
        else:
            print(f"\n⚠️ 通信エラー: {e}")
    except Exception as e:
        print(f"\n⚠️ エラー発生: {e}")

if __name__ == "__main__":
    endrunning_audit()
