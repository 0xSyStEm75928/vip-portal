import json, sys, os

SCHEMA_PATH = "json_core/dag_keyboard_schema.json"
STATE_PATH = "json_core/dag_keyboard_state.json"

def load_j(p):
    return json.load(open(p, "r", encoding="utf-8")) if os.path.exists(p) else {}

def save_j(p, d):
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def main():
    schema = load_j(SCHEMA_PATH)
    state = load_j(STATE_PATH)
    curr_id = state.get("current_node", schema.get("root", "KEYBOARD_ROOT"))

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        save_j(STATE_PATH, {"current_node": schema.get("root", "KEYBOARD_ROOT")})
        print("RESET|KEYBOARD_ROOT|echo '[KEYBOARD RESET]'")
        return

    flick = "LEFT"
    if "--flick" in sys.argv:
        idx = sys.argv.index("--flick")
        if idx + 1 < len(sys.argv):
            flick = sys.argv[idx + 1].upper()

    nodes = schema.get("nodes", {})
    curr_node = nodes.get(curr_id, {})
    flick_map = curr_node.get("flick_map", {})

    if flick in flick_map:
        next_id = flick_map[flick]
        next_node = nodes.get(next_id, {})
        
        if next_node.get("type") == "ACTION":
            cmd = next_node.get("command", "")
            sug = next_node.get("next_suggest", "")
            save_j(STATE_PATH, {"current_node": sug if sug else schema["root"]})
            # シェル側へ渡す結果（型：ACTION | 次ノード | 発動コマンド）
            print(f"ACTION|{sug}|{cmd}")
        else:
            save_j(STATE_PATH, {"current_node": next_id})
            print(f"NODE|{next_id}|echo 'TRANSITION TO {next_id}'")
    else:
        print(f"ERROR|{curr_id}|echo 'INVALID FLICK {flick}'")

if __name__ == "__main__":
    main()
