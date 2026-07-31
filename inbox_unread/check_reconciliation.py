import json

# 1. こちらの要求条件
required_keys = ["github_user", "signature"]

# 2. 受信データ（incoming_payload.json があれば読み込み）
try:
    with open("incoming_payload.json", "r") as f:
        incoming_data = json.load(f)
    
    print("=== 📥 受信データの照合性（Reconciliation）チェック ===")
    print(f"検出されたデータ: {incoming_data}")
    
    # 照合ロジック
    matched = all(key in incoming_data for key in required_keys)
    if matched:
        print("🟩 照合性: SUCCESS (必要データがすべて揃っています)")
    else:
        print("🟨 照合性: INCOMPLETE (一部のフィールドが未入力です)")

except FileNotFoundError:
    print("ℹ️ 受信データファイル (incoming_payload.json) はまだ生成されていません。")
