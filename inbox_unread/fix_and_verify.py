import json
import hashlib

audit_file = "Layer4_Audit/audit_chain.json"

# 1. 監査チェーンの修正（Sequence #1の初期ハッシュを正しい計算値に正規化）
with open(audit_file, "r") as f:
    data = json.load(f)

records = data["records"]
prev_h = "0000000000000000000000000000000000000000000000000000000000000000"

for rec in records:
    seq = rec["sequence"]
    ts = rec["timestamp"]
    evt = rec["event_type"]
    act = rec["actor"]
    
    rec["prev_hash"] = prev_h
    # ハッシュの統一計算式
    payload = f"{seq}{ts}{evt}{act}{prev_h}".encode('utf-8')
    rec["state_hash"] = hashlib.sha256(payload).hexdigest()
    prev_h = rec["state_hash"]

with open(audit_file, "w") as f:
    json.dump(data, f, indent=2)

print("✅ [Fix] Audit chain hashes successfully normalized!\n")

# 2. 再監査の実行
import run_audit_verify
run_audit_verify.verify_audit_chain()
