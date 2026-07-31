import urllib.request
import json

# VercelのデプロイURLを指定（ローカルテスト時は http://localhost:3000/api/ghost-spread-check）
VERCEL_API_URL = "https://your-app.vercel.app/api/ghost-spread-check"

def check_ghost_spread(dex_a, dex_b, threshold=0.20):
    payload = {
        "dex_a_price": dex_a,
        "dex_b_price": dex_b,
        "min_profit_threshold": threshold
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(VERCEL_API_URL, data=json.dumps(payload).encode('utf-8'), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read().decode('utf-8'))
            print(f"[{result['status']}] {result['message']}")
            if result['trigger_execution']:
                print("  🚀 -> ゴーストスプレッド実行シグナル発火！")
    except Exception as e:
        print(f"送信エラー: {e}")

if __name__ == "__main__":
    print("--- テスト1: 通常の小さなノイズ（反応しない） ---")
    check_ghost_spread(1.000, 1.001)  # 0.1% (閾値0.2%以下)

    print("\n--- テスト2: ゴーストスプレッド発生（反応する） ---")
    check_ghost_spread(1.000, 1.005)  # 0.5% (閾値0.2%超え)
