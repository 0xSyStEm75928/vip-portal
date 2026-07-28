#!/bin/sh
set -e

cat << 'JSON_EOF' > payment_verified_gate.json
{
  "$schema": "./schemas/payment.verified.gate.schema.json",
  "version": "3.1.0",
  "deal_metadata": {
    "deal_id": "DEAL_2026_ENTERPRISE_0x89A",
    "total_value": "35000",
    "currency": "USDT",
    "payout_address": "0xF7A353FAF6E6BD4732b0f234C656dBFDE53B0e91",
    "strategy": "REVERSE_VALUE_UNLOCK"
  },
  "feedback_prompt": {
    "question_to_client": "現在の仕様や進捗において、不満な点や懸念事項（空想・仮想の懸念含む）があれば提示してください。",
    "hypothetical_cause": "改善が必要な場合、こちらがJSON側でアクセスや開示を完全にブロック（ロック）していることが原因でしょうか？",
    "status": "AWAITING_CLIENT_RESPONSE"
  },
  "value_anchor": {
    "final_deliverable_hash": "0x7F_CORE_ENTERPRISE_VALUE_LOCKED",
    "status": "LOCKED_UNTIL_STEP_12"
  },
  "escrow_verification_gate": {
    "auto_release_enabled": true,
    "status": "AWAITING_DEPOSIT",
    "mempool_detection": {
      "enabled": true,
      "pre_signal_trigger": "PENDING_IN_MEMPOOL",
      "action_on_detect": "FLAG_INCOMING_DEPOSIT"
    },
    "verification_rules": {
      "require_exact_amount": true,
      "min_confirmations": 12,
      "timeout_action": "REVERT"
    }
  },
  "progression_gates": {
    "current_step": 0,
    "total_steps": 12,
    "unlock_schedule": [
      {
        "step": 1,
        "trigger": "MEMPOOL_DETECTION",
        "unlocked_scope": "READ_ACCESS_METADATA",
        "description": "入金察知・事前監査アクセス開放"
      },
      {
        "step": 6,
        "trigger": "CONFIRMATION_6_OF_12",
        "unlocked_scope": "PARTIAL_AUDIT_LOGS",
        "description": "中間確認・監査ログ部分開放"
      },
      {
        "step": 12,
        "trigger": "FINAL_12_CONFIRMATIONS",
        "unlocked_scope": "FULL_VALUE_RELEASE",
        "description": "12確認完了・全バリュー開放＆取引完了"
      }
    ]
  }
}
JSON_EOF

jq . payment_verified_gate.json > /dev/null
echo "✅ JSON文法チェックOK"

git add payment_verified_gate.json
git commit -m "feat(escrow): add feedback_prompt field in JSON for client inquiry"
git push origin main
