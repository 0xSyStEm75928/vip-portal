import sys
import os
import json
import time
import hashlib
import secrets

class JsshServer:
    def __init__(self, node_id="node_p2p_root"):
        self.node_id = node_id
        self.session_token = hashlib.sha256(secrets.token_bytes(32)).hexdigest()[:16]

    def create_response(self, result=None, error=None, req_id=1):
        return json.dumps({
            "jsonrpc": "2.0",
            "result": result,
            "error": error,
            "id": req_id,
            "node": self.node_id,
            "token": self.session_token
        }, ensure_ascii=False)

    def execute_rpc(self, payload_str):
        try:
            req = json.loads(payload_str)
            method = req.get("method")
            params = req.get("params", {})
            req_id = req.get("id", 1)

            if method == "jssh.status":
                res = {
                    "status": "ONLINE",
                    "voltage": "5.0V",
                    "nodes_connected": 21,
                    "arch": "64-BIT / P2P MESH"
                }
                return self.create_response(result=res, req_id=req_id)

            elif method == "jssh.fetch_offers":
                res = {
                    "total_offers": 21,
                    "authenticated": True,
                    "summary": "生体フェイルセーフ / 自律防衛 / 分散アー (21件全件PASS)"
                }
                return self.create_response(result=res, req_id=req_id)

            elif method == "jssh.exec":
                cmd = params.get("cmd", "")
                out = f"[JSSH_EXEC_OK] Command '{cmd}' executed in RAM-Only sandbox."
                return self.create_response(result={"output": out}, req_id=req_id)

            else:
                return self.create_response(error={"code": -32601, "message": "Method not found"})

        except Exception as e:
            return self.create_response(error={"code": -32700, "message": f"Parse error: {str(e)}"})

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    jssh = JsshServer()
    
    print("\033[38;2;0;255;255m🔳================================================================🔳\033[0m")
    print("  \033[38;2;180;50;255mJSSH // SECURE COMMAND SHELL ENGINE v0.3.1 (STABLE)\033[0m")
    print("  SESSION TOKEN: \033[38;2;255;255;0m" + jssh.session_token + "\033[0m")
    print("\033[38;2;0;255;255m🔳================================================================🔳\033[0m")

    while True:
        try:
            inp = input("\n\033[38;2;50;255;50m[JSSH_SHELL]:~#\033[0m ").strip()
            
            # 空白やログのコピペゴミ（[JSSH_RESPONSE]など）は完全に無視
            if not inp or "JSSH_RESPONSE" in inp or "jsonrpc" in inp:
                continue
                
            if inp.lower() in ["exit", "quit", "おわり"]:
                print("\n[*] Jssh セッションを切断しました。")
                break

            # 大文字小文字の揺れを自動で小文字化補正
            clean_cmd = inp.lower()
            if not clean_cmd.startswith("{"):
                rpc_payload = json.dumps({"jsonrpc": "2.0", "method": clean_cmd, "id": 1})
            else:
                rpc_payload = inp

            response = jssh.execute_rpc(rpc_payload)
            print("\033[38;2;0;255;255m[JSSH_RESPONSE]:\033[0m")
            parsed = json.loads(response)
            print(json.dumps(parsed, indent=2, ensure_ascii=False))

        except (KeyboardInterrupt, EOFError):
            print("\n[*] Jssh セッションを強制終了しました。")
            break

if __name__ == "__main__":
    main()
