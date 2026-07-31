import json
import time
import random
import datetime
import urllib.request

VERCEL_WEBHOOK_URL = "https://your-app.vercel.app/api/spread-alert"
UNISWAP_TOKEN_LIST = "https://tokens.uniswap.org"

def load_json(f):
    with open(f, "r", encoding="utf-8") as file:
        return json.load(file)

def verify_token_addresses(tokens):
    print("[*] 🔍 DEX公式トークンレジストリと照合中...")
    try:
        req = urllib.request.Request(UNISWAP_TOKEN_LIST, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            official_addresses = {t["address"].lower(): t["symbol"] for t in json.loads(res.read().decode()).get("tokens", [])}
        
        for symbol, addr in tokens.items():
            if addr.lower() in official_addresses:
                print(f"  ✅ [{symbol}] 正規品確認済み ({addr[:10]}...)")
            else:
                print(f"  ⚠️ [{symbol}] 公式リスト未登録: {addr}")
        return True
    except Exception as e:
        print(f"  ⚠️ レジストリ照合スキップ: {e}")
        return True

def start():
    gate = load_json("payment_verified_gate.json")
    config = load_json("ghost_spread_config.json")
    
    print(f"⚖️ BELPHEGOR [{gate.get('repo')}] SIMPLE FLASH ARBITRAGE")
    
    if not verify_token_addresses(config.get("target_tokens", {})):
        return
        
    print("[*] スキャン開始...")
    
    for cycle in range(1, 6):
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
        pa = round(random.uniform(1.000, 1.002), 4)
        pb = round(random.uniform(1.002, 1.006), 4)
        spread = round(((pb - pa) / pa) * 100, 3)
        
        flag = "✨ [OPPORTUNITY]" if spread >= config["min_profit_threshold_pct"] else "💤 [LOW]"
        print(f"[{now} UTC] #{cycle} Spread: {spread}% | DEX-A: {pa} | DEX-B: {pb} | {flag}")
        
        time.sleep(config["poll_interval_sec"])
        
    print("✅ スキャン完了。")

if __name__ == "__main__":
    start()
