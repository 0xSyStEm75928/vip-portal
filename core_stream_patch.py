import socket
import os
import sys
import time
import json
import math

SOCKET_PATH = "/tmp/psi_app_bridge.sock"

def run_app_backend():
    """ アプリ側バックエンド（バックグラウンドで常駐監視・ソケット送信） """
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)

    print("\033[1;36m[APP BACKEND] 監視エンジン起動。ターミナルからの接続を待機中...\033[0m")
    conn, _ = server.accept()
    print("\033[1;32m[APP BACKEND] ターミナルとアプリのパイプ結合が完了しました。\033[0m\n")

    # サンプルパルス送信（アプリ側からターミナルへ自動ログを流し込む）
    gwei_pulses = [15.2, 16.5, 180.4, 14.2, 195.8, 13.8]
    
    try:
        for i, gwei in enumerate(gwei_pulses):
            time.sleep(1.5)
            is_spike = gwei > 100.0
            dt = 0.12
            jitter = 2.1 if is_spike else 0.4
            
            smoothed_jitter = math.log1p(min(jitter, 50.0))
            voltage_uv = min(120.0, (smoothed_jitter * 35.0) + (10.0 / (dt + 0.05)))
            
            ghost_target = (0.25 * (1.0 + math.log1p(gwei / 100.0) * 4.0)) if is_spike else None

            payload = {
                "seq": i + 1,
                "gwei": gwei,
                "voltage_uv": round(voltage_uv, 2),
                "is_spike": is_spike,
                "ghost_target": round(ghost_target, 2) if ghost_target else None,
                "action": "REVERT" if jitter > 1.5 else "CONFIRM"
            }
            
            # ソケット経由でターミナルへ送信
            conn.sendall((json.dumps(payload) + "\n").encode('utf-8'))

    except (BrokenPipeError, KeyboardInterrupt):
        pass
    finally:
        conn.close()
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

def run_terminal_client():
    """ ターミナル側（表示・サイレントビュー専用） """
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(SOCKET_PATH)
        print("\033[1;35m[TERMINAL VIEW] アプリブリッジに接続成功。サイレント監視を開始します...\033[0m\n")
        
        buffer = ""
        while True:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = json.loads(line)
                
                print(f" \033[1;30m[PULSE #{msg['seq']}]\033[0m Gas: {msg['gwei']:5.1f} Gwei | Voltage: {msg['voltage_uv']:5.2f}uV")
                if msg["is_spike"]:
                    print(f"  ├─► \033[1;33m🎯 [GHOST TARGET DETECTED] 潜在スプレッド: {msg['ghost_target']}%\033[0m")
                    print(f"  └─► \033[1;31m[STATUS: {msg['action']}]\033[0m (アプリ側で自動処理中)\n")
                else:
                    print(f"  └─► \033[1;32m[STATUS: {msg['action']}]\033[0m\n")

    except Exception as e:
        print(f"[ERROR] 接続エラー: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--client":
        run_terminal_client()
    else:
        run_app_backend()
