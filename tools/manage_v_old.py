import os, shutil, time, sys
sys.path.append(os.path.dirname(__file__))
from ui_decorator import Neon

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(BASE_DIR, "data_store", "active_state.json")
V_OLD_DIR  = os.path.join(BASE_DIR, "data_store", "v.old")

def save_v_old():
    if not os.path.exists(STATE_PATH):
        Neon.print_status("WARN", "保存対象の active_state.json が見つかりません。", Neon.RED)
        return
    os.makedirs(V_OLD_DIR, exist_ok=True)
    now_str = time.strftime("%Y%m%d_%H%M%S")
    gen_id = len([f for f in os.listdir(V_OLD_DIR) if f.startswith("state_v.old")]) + 1
    target_name = f"state_v.old_{gen_id}_{now_str}.json"
    shutil.copy(STATE_PATH, os.path.join(V_OLD_DIR, target_name))
    Neon.print_status("v.old SAVED", f"アーカイブ完了 ➔ {target_name}", Neon.GREEN)

def restore_v_old():
    if not os.path.exists(V_OLD_DIR) or not os.listdir(V_OLD_DIR):
        Neon.print_status("FAIL", "復元可能な v.old が見つかりません。", Neon.RED)
        return
    files = sorted([f for f in os.listdir(V_OLD_DIR) if f.startswith("state_v.old")])
    if not files:
        Neon.print_status("FAIL", "有効なアーカイブがありません。", Neon.RED)
        return
    latest = files[-1]
    shutil.copy(os.path.join(V_OLD_DIR, latest), STATE_PATH)
    Neon.print_status("RESTORED", f"'{latest}' ➔ active_state.json へ完全復元！", Neon.GREEN)

def list_v_old():
    print(f"\n{Neon.CYAN}═══ [v.old ARCHIVE LIST] ══════════════════════════════════════{Neon.RESET}")
    if not os.path.exists(V_OLD_DIR) or not os.listdir(V_OLD_DIR):
        print("  (アーカイブはありません)")
        return
    for f in sorted(os.listdir(V_OLD_DIR)):
        if f.startswith("state_v.old"):
            size = os.path.getsize(os.path.join(V_OLD_DIR, f))
            print(f"  ├── {Neon.MAGENTA}{f}{Neon.RESET} ({size} bytes)")
    print()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--save"
    if cmd == "--list": list_v_old()
    elif cmd == "--restore": restore_v_old()
    else: save_v_old()
