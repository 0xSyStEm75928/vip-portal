import os
import time
import random
import sys

C_RESET = "\033[0m"
C_CYAN = "\033[38;2;0;255;255m"
C_GREEN = "\033[38;2;50;255;50m"
C_PURPLE = "\033[38;2;180;50;255m"
C_AMBER = "\033[38;2;255;191;0m"
C_DIM = "\033[2m"

SAMPLE_LOGS = [
    ("Node_0x4A8F", "⚡ 契約プロトコル v2.1 デプロイ完了 (Hash: 0x8F9A...)"),
    ("Devil_Core", "📜 羊皮紙ログに暗号署名してエスクローバインド完了。確認頼む。"),
    ("Node_0x99BC", "💰 エスクロー着金を検知。スマートコントラクトを自動実行します。"),
    ("Node_0x77EE", "🔐 ゼロ知識証明（ZKP）パラメータの検証に成功しました。")
]

ONLINE_NODES = [
    ("Node_0x4A8F", "契約ノード / Verify: OK"),
    ("Devil_Core", "生体ハッシュ同調完了"),
    ("Node_0x99BC", "自動決済ノード / Escrow: Ready"),
    ("Node_0x77EE", "暗号鍵リレーノード")
]

def render_chat_interface(logs):
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{C_PURPLE}🔳================================================================================🔳{C_RESET}")
    print(f"  {C_CYAN}ZERO_CORE // ANONYMOUS MECHANICS BIZ-HUB & E2EE CHAT ENGINE{C_RESET}")
    print(f"  ARCHITECTURE: [64-BIT / P2P MESH] // ACTIVE NODES: 128 NODES // NETWORK STATUS: SECURE")
    print(f"{C_PURPLE}🔳================================================================================🔳{C_RESET}")
    print(f"  {C_AMBER}【視覚化ノード】{C_RESET} ║ [📡 P2P MESH: 128] ──► [🔐 E2EE VAULT: ACTIVE] ──► [💼 BIZ CONTRACT HUB]")
    print(f"{C_PURPLE}🔳================================================================================🔳{C_RESET}")
    print(f"  ║ {C_CYAN}💬 #BIZ_DEAL_ROOM{C_RESET}            │ {C_GREEN}👥 ONLINE ANONYMOUS NODES (ACTIVE: {len(ONLINE_NODES)}){C_RESET}               ║")
    print(f"  ║ --------------------------- │ -------------------------------------------------- ║")
    
    for i in range(3):
        log_user, log_msg = logs[i] if i < len(logs) else ("---", "---")
        node_id, node_desc = ONLINE_NODES[i] if i < len(ONLINE_NODES) else ("---", "---")
        
        print(f"  ║ {C_DIM}[12:40:{i*15:02d}]{C_RESET} {C_CYAN}{log_user:<12}{C_RESET} │ {C_GREEN}● {node_id:<12}{C_RESET} ({node_desc})")
        print(f"  ║  └─► {log_msg:<38} │")
        
    print(f"{C_PURPLE}🔳================================================================================🔳{C_RESET}")
    payload_hash = f"0x{random.randint(0x100000, 0xFFFFFF):06X}"
    print(f"  ║ {C_AMBER}【リアルタイムデータパケット】{C_RESET} ║ {C_GREEN}{payload_hash}_TRANSFER_100%_OK [RATE: {random.uniform(8.0, 12.0):.1f} MB/s]{C_RESET}  ║")
    print(f"{C_PURPLE}    print(f"  {C_CYAN}VOLTAGE_BUS_ALIGN ║ 通電プロトコル: 'ACTIVE_TRANSACTION'{C_RESET}")
    print(f"{C_PURPLE}■================================================================================🔳{C_RESET}")

def main():
    logs = list(SAMPLE_LOGS)
    render_chat_interface(logs)
    
    while True:
        try:
            inp = input(f"\n{C_CYAN}[入力コマンド (例: /send, /contract, /escrow, /exit)]:~#{C_RESET} ").strip()
            if inp.lower() in ["/exit", "exit", "quit", "おわり"]:
                print(f"\n{C_AMBER}[*] ZERO-CHAT アノニマスセッションを安全に切り離しました。{C_RESET}")
                break
                
            if inp.startswith("/send "):
                msg = inp[6:]
                logs.pop(0)
                logs.append(("YOU_NODE", f"💬 {msg}"))
            elif inp.startswith("/contract"):
                logs.pop(0)
                logs.append(("YOU_NODE", "⚡ 新規スマートコントラクト提案を発行しました"))
            elif inp.startswith("/escrow"):
                logs.pop(0)
                logs.append(("YOU_NODE", "💰 エスクロー預託リクエストを暗号送信しました"))
            else:
                if inp:
                    logs.pop(0)
                    logs.append(("YOU_NODE", f"RAW_SIGNAL: {inp}"))
                    
            render_chat_interface(logs)
            
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
