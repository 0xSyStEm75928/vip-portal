import sys
import os

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("🔳==================================================🔳")
    print("   ANONYMOUS OS // ZERO INTEGRATED COMMAND HUB")
    print("🔳==================================================🔳")
    print("  [1] zero-panel  : 5.0V 擬似電位パルス & モニター")
    print("  [2] zero-chat   : E2EE ビジュアルビジネスチャット")
    print("  [3] zero-stealth: 緊急偽装 & メモリ消去 (Panic)")
    print("  [0] exit        : セッション終了")
    print("🔳==================================================🔳")
    
    try:
        choice = input("\n[ZERO_HUB]:~# ").strip()
        if choice == "1":
            from zero_core.panel import main as panel_main
            panel_main()
        elif choice == "2":
            from zero_core.chat import main as chat_main
            chat_main()
        elif choice == "3":
            from zero_core.stealth import trigger_stealth_panic
            trigger_stealth_panic()
        elif choice in ["0", "exit", "quit"]:
            print("\n[*] ZERO HUB を正常にログアウトしました。")
        else:
            print("\n[!] 無効な選択です。")
    except (KeyboardInterrupt, EOFError):
        pass

if __name__ == "__main__":
    main()
