import json

# 個別取引のカスタム条件定義データ
custom_terms = {
    "target_customer_id": "CUST-001-ALPHA",
    "proposed_conditions": {
        "anonymity_requested": True,
        "settlement_type": "BARTER_OR_PHYSICAL_ASSET",  # 物々条件
        "irreversible_clause": True,                   # 後戻り不可（不可逆）の合意
        "escrow_bypass_allowed": False
    },
    "verification_checks": {
        "identity_compliance": "ANONYMOUS_WITH_ESCROW_REQUIRED",
        "settlement_risk_status": "HIGH_VOLATILITY_RISK",
        "legal_review_required": True,
        "proceed_permitted": False
    }
}

def evaluate_terms(data):
    print("=== 取引条件の照合評価 ===")
    print(f"対象顧客ID: {data['target_customer_id']}")
    print(f"匿名取引フラグ: {data['proposed_conditions']['anonymity_requested']}")
    print(f"決済形態: {data['proposed_conditions']['settlement_type']}")
    print(f"不可逆条項: {data['proposed_conditions']['irreversible_clause']}")
    print("-----------------------------------")
    
    # 評価ロジック
    if data['proposed_conditions']['settlement_type'] != "STANDARD_CURRENCY_OR_CRYPTO":
        print("⚠️ 注意: 非標準的な決済形態（物々取引等）が選択されています。評価額の客観的検証が必要です。")
    if data['proposed_conditions']['irreversible_clause']:
        print("⚠️ 注意: 不可逆（後戻り不能）な取引条件です。事前の事前受領または強固なエスクローが必要です。")

    print("\n[照合結果 JSON]")
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    evaluate_terms(custom_terms)
