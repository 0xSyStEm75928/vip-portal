#!/bin/sh

echo "===================================================="
echo " 🌐 [PIRDAG CLIENT DISPATCHER - 表シンプル / 裏 ZERO_CORE]"
echo "===================================================="

# 顧客用案内文の表示
cat CLIENT_OFFER.txt
echo ""

# 顧客送信用の標準リクエストテンプレート生成（business-flow用）
mkdir -p client_payloads
cat << 'JSON' > client_payloads/request_template.json
{
  "protocol": "PIRDAG_CLI_V1",
  "client_id": "CLIENT_001",
  "action": "REQUEST_ACCESS",
  "payload": {
    "intent": "BUSINESS_FLOW",
    "status": "READY"
  }
}
JSON

echo " 📄 顧客向けリクエスト用テンプレートを作成しました:"
echo "    ➔ client_payloads/request_template.json"
echo "----------------------------------------------------"
echo " 🛡️ 裏側ステータス: ZERO_CORE (0x1225) 潜伏防衛中"
echo "===================================================="
