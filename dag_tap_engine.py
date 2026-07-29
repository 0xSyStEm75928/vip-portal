import json, sys, os

STATE_PATH = "json_core/tap_dag_state.json"

def load_json(p):
    return json.load(open(p, "r", encoding="utf-8")) if os.path.exists(p) else {}

def save_json(p, d):
    os.makedirs("json_core", exist_ok=True)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def main():
    state = load_json(STATE_PATH)
    
    # 初期状態（無害なデフォルト値）
    current_node = state.get("node", "N1_INGRESS")
    val_bias = state.get("val_bias", 50.0) # 0.0 ~ 100.0 の範囲で微調整するパラメータ

    action = sys.argv[1].upper() if len(sys.argv) > 1 else "CENTER"

    # --- 無害化（クランプ）アルゴリズム演算 ---
    if action == "TOP":
        val_bias += 5.0
    elif action == "BOTTOM":
        val_bias -= 5.0
    elif action == "RIGHT":
        current_node = "N3_GATE" if current_node == "N1_INGRESS" else "N5_SUMMARY"
    elif action == "LEFT":
        current_node = "N1_INGRESS" if current_node == "N3_GATE" else "N3_GATE"

    # 【無害化ガード】数値が危険領域に行かないよう 0.0 ~ 100.0 に収めてピッタリ安全化
    val_bias = max(0.0, min(100.0, val_bias))

    # 状態の保存
    new_state = {"node": current_node, "val_bias": val_bias}
    save_json(STATE_PATH, new_state)

    # 次に発動すべきコマンドの生成（答え側の逆駆動）
    next_cmd = f"jssh CUSTOMER_001 {current_node}"
    
    # シェルへ結果を渡す (フォーマット: NODE|BIAS|CMD)
    print(f"{current_node}|{val_bias:.1f}|{next_cmd}")

if __name__ == "__main__":
    main()
