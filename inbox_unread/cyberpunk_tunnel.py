import sys, time, os, json

# 24bit True Color ネオンカラー定義
C_RESET   = "\033[0m"
C_MAGENTA = "\033[38;2;255;0;127m"  # ネオンマゼンタ
C_CYAN    = "\033[38;2;0;243;255m"  # ネオンシアン
C_GREEN   = "\033[38;2;50;255;50m"   # ネオングリーン
C_YELLOW  = "\033[38;2;255;230;0m"  # ネオンイエロー
C_DARK_BG = "\033[48;2;10;10;25m"   # サイバーダーク背景

def draw_cyber_tunnel():
    state_file = "json_core/kbd_x_belphegor_state.json"
    log_info = "NO_DATA_STREAM"
    if os.path.exists(state_file):
        try:
            d = json.load(open(state_file, "r", encoding="utf-8"))
            log_info = f"CYCLE:{d.get('cycle')} | X:{d.get('unk_x')} | IMPACT:{d.get('multiplied_impact')} | MODE:{d.get('ai_mode')}"
        except: pass

    # カーソル非表示
    print("\033[?25l", end="")

    # 4フレームの光速パルスアニメーション
    for frame in range(4):
        # 画面先頭へ戻して上書き描画（チラつき防止）
        print("\033[H", end="")
        print(f"{C_DARK_BG}")
        print(f"{C_CYAN}═" * 80 + f"{C_RESET}")
        print(f"{C_MAGENTA} ⚡ [CYBERPUNK NEON TUNNEL v2.0] ⚡  <64-BIT HIGH-SPEED STREAM>{C_RESET}")
        print(f"{C_CYAN}═" * 80 + f"{C_RESET}\n")

        # 1. サイバーパンク・入り口ゲート
        print(f"   {C_MAGENTA}╔══════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"   {C_MAGENTA}║  {C_YELLOW}▲ ENTRANCE GATE (CYBERPUNK PORTAL) ▲{C_MAGENTA}                            ║{C_RESET}")

        # 2. ワイヤーフレーム構造の奥行き（ネオン棒線トンネル）
        for depth in range(1, 5):
            pad = " " * (depth * 3)
            w = 58 - (depth * 6)
            
            # 光線パルスの移動演出
            if (depth + frame) % 2 == 0:
                color = C_CYAN
                line_char = "═"
            else:
                color = C_MAGENTA
                line_char = "─"

            if depth == 2:
                # トンネル中層にホログラム状の最新ログを表示
                print(f"   {pad}{color}┌{line_char*w}┐{C_RESET}")
                print(f"   {pad}{color}│ {C_GREEN}★ CORE-DATA: {log_info[:w-16].ljust(w-16)} {color}│{C_RESET}")
                print(f"   {pad}{color}└{line_char*w}┘{C_RESET}")
            else:
                print(f"   {pad}{color}┌{line_char*w}┐{C_RESET}")
                print(f"   {pad}{color}└{line_char*w}┘{C_RESET}")

        # 3. 消失点（SYSTEM CORE）
        print(f"               {C_GREEN}││  ░▒▓█ [DEEP SYSTEM CORE] █▓▒░  ││{C_RESET}")
        print(f"               {C_GREEN}▼▼                                ▼▼{C_RESET}\n")

        print(f"{C_CYAN}─" * 80 + f"{C_RESET}")
        print(f"{C_YELLOW} >>> [history -s] 光速ラインを充填中... 『↑』 ➔ Enter で推進！{C_RESET}")
        time.sleep(0.03)

    # カーソル復元
    print("\033[?25h", end="")

if __name__ == "__main__":
    draw_cyber_tunnel()
