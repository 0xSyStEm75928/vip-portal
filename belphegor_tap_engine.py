import json, sys, os, math

# ベルフェゴール v.old 用 状態格納ディレクトリ
STATE_PATH = "json_core/belphegor_v_old_state.json"

def load_state():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, "r", encoding="utf-8"))
        except: pass
    return {"node": "BELPHEGOR_ROOT", "raw_score": 0.0, "ema_val": 50.0, "sigmoid_prob": 0.50, "version": "v.old"}

def save_state(data):
    os.makedirs("json_core", exist_ok=True)
    json.dump(data, open(STATE_PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def verify_formula(ema_val, sigmoid_prob):
    expected_p = 1.0 / (1.0 + math.exp(-0.1 * (ema_val - 50.0)))
    return math.isclose(sigmoid_prob, expected_p, abs_tol=1e-3)

def main():
    state = load_state()
    flick = sys.argv[1].upper() if len(sys.argv) > 1 else "TOP"

    x = state.get("raw_score", 0.0)
    prev_ema = state.get("ema_val", 50.0)

    if flick == "TOP":
        x += 1.0
    elif flick == "BOTTOM":
        x -= 1.0
    elif flick == "RIGHT":
        state["intent_node"] = "BELPHEGOR_GATE"
    elif flick == "LEFT":
        state["intent_node"] = "BELPHEGOR_ROOT"

    # EMA & Sigmoid 演算
    alpha = 0.3
    raw_mapped = 50.0 + (x * 5.0)
    current_ema = (alpha * raw_mapped) + ((1.0 - alpha) * prev_ema)
    sigmoid_val = 1.0 / (1.0 + math.exp(-0.1 * (current_ema - 50.0)))

    # 検証
    if not verify_formula(current_ema, sigmoid_val):
        state["status"] = "BELPHEGOR_MISMATCH_LOCKED"
        save_state(state)
        print("FAIL|BELPHEGOR_LOCK")
        sys.exit(1)

    state["raw_score"] = round(x, 2)
    state["ema_val"] = round(current_ema, 2)
    state["sigmoid_prob"] = round(sigmoid_val, 4)

    if "intent_node" in state:
        state["node"] = state.pop("intent_node")

    state["status"] = "BELPHEGOR_DEPLOYED_STABLE"
    save_state(state)

    print(f"SUCCESS|{state['node']}|jq . json_core/belphegor_v_old_state.json")

if __name__ == "__main__":
    main()
