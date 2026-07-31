import time, json

def handle_suspicious_request(ip_address, payload):
    """攻撃者を永遠に終わらない応答（無制限ループ・遅延応答）の渦に閉じ込める"""
    print(f"[VORTEX] Disorienting malicious origin: {ip_address}")
    fake_matrix = {"traffic_vortex": "ACTIVE", "redirect_cycles": 99999}
    time.sleep(0.5) # レスポンスをわざと遅延
    return json.dumps(fake_matrix)
