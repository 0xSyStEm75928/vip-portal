import flask
from flask import Flask, request, jsonify
import time
import json
import datetime

app = Flask(__name__)

# 空白（時間・処理遅延・パラメータギャップ）受信用レシーバー
captured_logs = []

@app.route('/api/v1/ghost_gap', methods=['GET', 'POST', 'PUT'])
def ghost_gap_handler():
    """
    UI/認可の『空白』時間をローカルで安全に検証・記録するレシーバー
    """
    # 遅延パラメータ（指定がなければ0秒）
    req_json = request.get_json(silent=True) or {}
    delay_seconds = req_json.get('delay', 0)
    
    if delay_seconds > 0:
        time.sleep(delay_seconds)

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "method": request.method,
        "headers": dict(request.headers),
        "args": dict(request.args),
        "body": req_json,
        "simulated_delay": f"{delay_seconds}s"
    }

    captured_logs.append(log_entry)

    print(f"\n[+] 📩 [GHOST_GAP_LOG] データ取得成功 ({datetime.datetime.now().strftime('%H:%M:%S')})")
    print(json.dumps(log_entry, indent=2, ensure_ascii=False))

    return jsonify({
        "status": "200_OK",
        "message": "Ghost Gap captured successfully in local works",
        "entry_id": len(captured_logs)
    }), 200

if __name__ == '__main__':
    print("[*] Local Ghost Gap Receiver Starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
