import sys, time, os, math, json

# 24bit True Color ネオンカラー
C_RESET   = "\033[0m"
C_MAGENTA = "\033[38;2;255;0;127m"  # ネオンマゼンタ
C_CYAN    = "\033[38;2;0;243;255m"  # ネオンシアン
C_PURPLE  = "\033[38;2;180;0;255m"  # ネオンパープル
C_YELLOW  = "\033[38;2;255;230;0m"  # ネオンイエロー

def draw_vortex():
    state_file = "json_core/kbd_x_belphegor_state.json"
    x_val, impact, mode, cycle = 0.0, 0.0, "UNKNOWN", 0
    if os.path.exists(state_file):
        try:
            d = json.load(open(state_file, "r", encoding="utf-8"))
            x_val = d.get('unk_x', 0.0)
            impact = d.get('multiplied_impact', 0.0)
            mode = d.get('ai_mode', 'INIT')
            cycle = d.get('cycle', 0)
        except: pass

    # カーソル隠蔽
    print("\033[?25l", end="")

    # 🌀 渦のアニメーション回転（6フレーム）
    for frame in range(6):
        print("\033[H", end="") # ホーム位置へ移動（チラつき防止）
        
        # 渦の回転角度パラメータ
        angle = frame * 0.5
        
        # ネオンのグラデーションカラー切り替え
        c1 = C_CYAN if frame % 2 == 0 else C_MAGENTA
        c2 = C_MAGENTA if frame % 2 == 0 else C_PURPLE

        print(f"\n{C_PURPLE}─── [ LOG STREAM HISTORY #00{cycle} ] ──────────────────────────────────────────{C_RESET}\n")
        
        # ネオン渦（Vortex）の動的描画（数学的回転パターン）
        v1 = f"{c1}       . - ~ ~ ~ - .{C_RESET}"
        v2 = f"{c2}   . '   {c1}/   🌀   \\{c2}   ' .{C_RESET}"
        v3 = f"{c1} /     /  {C_YELLOW}x_value: {x_val}{c1}  \\     \\{C_RESET}"
        v4 = f"{c2}|     |   {C_YELLOW}impact : {impact}{c2}   |     |{C_RESET}"
        v5 = f"{c1} \\     \\  {C_YELLOW}mode   : {mode[:12]}{c1} /     /{C_RESET}"
        v6 = f"{c2}   . '   {c1}\\        /{c2}   ' .{C_RESET}"
        v7 = f"{c1}       ' - _ _ _ - '{C_RESET}"

        # アニメーションごとの渦のダイナミック変形
        if frame % 3 == 1:
            v2, v6 = v6, v2
        elif frame % 3 == 2:
            v3, v5 = v5, v3

        print(v1)
        print(v2)
        print(v3)
        print(v4)
        print(v5)
        print(v6)
        print(v7)

        print(f"\n{C_CYAN}────────────────────────────────────────────────────────────────────────{C_RESET}")
        print(f"{C_YELLOW}>>> [VORTEX LOADED] 『↑』 ➔ Enter で渦の中に次のログを叩き込め！{C_RESET}")
        time.sleep(0.03)

    print("\033[?25h", end="") # カーソル復元

if __name__ == "__main__":
    draw_vortex()
