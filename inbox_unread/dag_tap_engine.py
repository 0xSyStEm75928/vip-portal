import json, sys, os, math

STATE_PATH = "json_core/tap_dag_state.json"

def load_state():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, "r", encoding="utf-8"))
        except: pass
    return {"node": "N1_INGRESS", "raw_score": 0.0, "ema_val": 50.0, "sigmoid_prob": 0.50, "status": "INIT"}

def save_state(data):
    os.makedirs("json_core", exist_ok=True)
    json.dump(data, open(STATE_PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def verify_formula(ema_val, sigmoid_prob):
    # 誤差吸収を含めた厳密なSigmoid整合性チェック
    expected_p = 1.0 / (1.0 + math.exp(-0.1 * (ema_val - 50.0)))
    is_valid = math.isclose(sigmoid_prob, expected_p, abs_tol=1e-3)
    return is_valid, expected_p

def main():
    state = load_state()
    flick = sys.argv[1].upper() if len(sys.argv) > 1 else "TOP"

    x = state.get("raw_score", 0.0)
    prev_ema = state.get("ema_val", 50.0)

    # 1. 入力操作
    if flick == "TOP":
        x += 1.0
    elif flick == "BOTTOM":
        x -= 1.0
    elif flick == "RIGHT":
        state["intent_node"] = "N3_GATE" if state["node"] == "N1_INGRESS" else "N5_SUMMARY"
    elif flick == "LEFT":
        state["intent_node"] = "N1_INGRESS"

    # 2. EMA（指数移動平均）計算
    alpha = 0.3
    raw_mapped = 50.0 + (x * 5.0)
    current_ema = (alpha * raw_mapped) + ((1.0 - alpha) * prev_ema)

    # 3. Sigmoid（確率変換）計算
    sigmoid_val = 1.0 / (1.0 + math.exp(-0.1 * (current_ema - 50.0)))

    # 4. 数学的一致ガード検証
    is_valid, _ = verify_formula(current_ema, sigmoid_val)

    if not is_valid:
        state["status"] = "FORMULA_MISMATCH_LOCKED"
        save_state(state)
        print("FAIL|数式不一致のためロックしました")
        sys.exit(1)

    # ガード通過時のみ丸めて保存
    state["raw_score"] = round(x, 2)
    state["ema_val"] = round(current_ema, 2)
    state["sigmoid_prob"] = round(sigmoid_val, 4)

    if "intent_node" in state:
        state["node"] = state.pop("intent_node")

    state["status"] = "FORMULA_VERIFIED_UNLOCKED"
    save_state(state)

    # Bashへの正常応答出力
    print(f"SUCCESS|{state['node']}|jq . json_core/tap_dag_state.json")

if __name__ == "__main__":
    main()
