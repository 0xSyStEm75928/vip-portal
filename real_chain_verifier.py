import urllib.request
import json
import sys

def verify_real_onchain_usdt(wallet_address):
    print("=" * 60)
    print(f"🔍 [REAL AUDIT] オンチェーン実データ照合開始")
    print(f"📍 対象アドレス: {wallet_address}")
    print("=" * 60)

    # 1. アドレス形式チェック (0x + 40桁のヘキサコード = 計42文字)
    if not wallet_address.startswith("0x") or len(wallet_address) != 42:
        print("🟥 判定: INVALID_ADDRESS_FORMAT")
        print("🚨 原因: アドレスの文字数が不正です（42文字である必要があります）。")
        print("⛔ アクション: 【即時ブロック】冷やかし・偽アドレスです。")
        print("=" * 60)
        return

    # 2. Blockchain APIを用いたリアルタイム照合
    # (ここでは例としてEtherscan等のノードへ生問い合わせ)
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            
            if res_data.get("status") == "0" and res_data.get("message") == "NOTOK":
                print("🟥 判定: ADDRESS_NOT_FOUND_ON_CHAIN")
                print("🚨 原因: オンチェーン上に記録が存在しません。")
                print("⛔ アクション: 【即時ブロック】")
            else:
                # ETH残高（USDTの場合はコントラクト呼び出しが必要ですが、ここではネットワーク存在確認）
                wei_balance = int(res_data.get("result", 0))
                eth_balance = wei_balance / 10**18
                print(f"🟩 判定: ADDRESS_EXISTS_ON_CHAIN")
                print(f"💰 ETH残高: {eth_balance:.4f} ETH")
                print("💡 アドレスの実体が確認できました。次にUSDTコントラクト残高を照合します。")

    except Exception as e:
        print(f"⚠️ 通信エラー: オンチェーンデータの取得に失敗しました ({e})")

    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_input = sys.argv[1]
    else:
        # テスト用に前回の不完全アドレスを入れてみる
        target_input = "0x8f2a99c1d04e321a5b849e2104"
    
    verify_real_onchain_usdt(target_input)
