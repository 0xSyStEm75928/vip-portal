import sys
import pyotp

# --------------------------------------------------
# 1. ユーザーごとに発行・保存しておく秘密鍵（シークレット）
#    ※実際はデータベースや設定ファイル等から読み込みます
# --------------------------------------------------
# 例用のランダムキー（実際は pyotp.random_base32() で生成して顧客に渡す）
USER_SECRET_KEY = "JBSWY3DPEHPK3PXP"

# --------------------------------------------------
# 2. 初回登録用の情報表示（必要な場合のみ）
# --------------------------------------------------
def show_setup_info():
    totp = pyotp.TOTP(USER_SECRET_KEY)
    # Google Authenticatorに登録するためのURL
    auth_url = totp.provisioning_uri(name="your_user_id", issuer_name="YourBusinessName")
    print("=== Google Authenticator 初回設定 ===")
    print(f"手動入力用キー: {USER_SECRET_KEY}")
    print(f"設定URL (QRコード化用): {auth_url}")
    print("===================================\n")

# --------------------------------------------------
# 3. CLI認証メイン処理
# --------------------------------------------------
def verify_cli_access():
    totp = pyotp.TOTP(USER_SECRET_KEY)
    
    print("[SECURITY] 本人確認が必要です。")
    user_code = input("Google Authenticatorの6桁のコードを入力してください: ").strip()

    # 30秒のタイムラグを考慮して検証
    if totp.verify(user_code):
        print("\n[SUCCESS] 認証成功。CLI処理を開始します...\n")
        # ----------------------------------------------
        # ここに本処理（コマンドの実行やプロトコル操作）を書く
        # ----------------------------------------------
    else:
        print("\n[ERROR] 認証コードが不正または有効期限切れです。処理を中止します。")
        sys.exit(1)

if __name__ == "__main__":
    # 実行時に認証を挟む
    verify_cli_access()
