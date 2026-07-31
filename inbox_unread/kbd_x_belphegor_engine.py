import json, sys, os, time, math, random

STATE_PATH = "json_core/kbd_x_belphegor_state.json"

def main():
    state = {}
    if os.path.exists(STATE_PATH):
        try: state = json.load(open(STATE_PATH, "r"))
        except: pass

    cycle = state.get("cycle", 0) + 1
    arg_cmd = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
    is_override = (arg_cmd == "OVERRIDE")

    now = time.time()
    last_ts = state.get("last_ts", now)
    delta_ms = max(10, int((now - last_ts) * 1000))

    prev_x = state.get("unk_x", 0.10)
    unk_x = round(min(0.30, max(0.01, prev_x + random.uniform(-0.02, 0.02))), 4)

    if is_override:
        sigmoid_p, ai_mode, node_label, unk_x, impact = 1.0, "FORCE_OVERRIDDEN", "N_REAL_OVERRIDE", 0.9999, 999.99
    else:
        speed_factor = round(1000.0 / delta_ms, 2)
        impact = round(speed_factor * unk_x, 4)
        sigmoid_p = round(1.0 / (1.0 + math.exp(-0.1 * (impact - 15.0))), 4)
        if delta_ms < 150 and unk_x > 0.25 and sigmoid_p > 0.80:
            ai_mode, node_label = "RARE_UNMASKED", "N_UNMASKED"
        else:
            ai_mode, node_label = "MASKED_STABLE", "N_MASKED"

    state.update({"cycle": cycle, "delta_ms": delta_ms, "unk_x": unk_x, "multiplied_impact": impact, "sigmoid_p": sigmoid_p, "ai_mode": ai_mode, "last_ts": now})
    os.makedirs("json_core", exist_ok=True)
    json.dump(state, open(STATE_PATH, "w", encoding="utf-8"))

    print(f"SUCCESS|{cycle}|{unk_x}|{impact}|{ai_mode}|{delta_ms}")

if __name__ == "__main__":
    main()
