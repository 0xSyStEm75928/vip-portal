import json
import hashlib

def verify_audit_chain():
    print("==========================================")
    print(" 🛡️ ZeroCore Audit Chain Integrity Check")
    print("==========================================\n")
    
    audit_file = "Layer4_Audit/audit_chain.json"
    
    try:
        with open(audit_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to load audit chain file: {e}")
        return False

    records = data.get("records", [])
    total_records = data.get("total_records", 0)
    
    print(f"[*] Target File: {audit_file}")
    print(f"[*] Total Registered Records: {total_records}\n")
    
    if len(records) == 0:
        print("[WARNING] Audit chain is empty.")
        return True

    previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    is_valid = True

    for record in records:
        seq = record.get("sequence")
        timestamp = record.get("timestamp")
        event_type = record.get("event_type")
        actor = record.get("actor")
        recorded_prev_hash = record.get("prev_hash")
        recorded_state_hash = record.get("state_hash")
        
        # 1. 前のハッシュの連続性チェック
        if recorded_prev_hash != previous_hash:
            print(f"❌ [FAIL] Sequence #{seq}: Broken Chain Link!")
            print(f"   Expected Prev Hash : {previous_hash}")
            print(f"   Recorded Prev Hash : {recorded_prev_hash}")
            is_valid = False
            break
            
        # 2. 現在のブロックのハッシュ再計算（改ざん検知）
        hash_payload = f"{seq}{timestamp}{event_type}{actor}{recorded_prev_hash}".encode('utf-8')
        calculated_hash = hashlib.sha256(hash_payload).hexdigest()
        
        if calculated_hash != recorded_state_hash:
            print(f"❌ [FAIL] Sequence #{seq}: State Tampering Detected!")
            print(f"   Calculated Hash : {calculated_hash}")
            print(f"   Recorded Hash   : {recorded_state_hash}")
            is_valid = False
            break
            
        print(f"✅ [OK] Seq #{seq:03d} | Event: {event_type:<25} | Hash: {recorded_state_hash[:16]}...")
        previous_hash = recorded_state_hash

    print("\n------------------------------------------")
    if is_valid:
        print("🎯 AUDIT RESULT: PASSED (Chain Integrity Verified)")
        print("   すべての監査ログの整合性および連続性が証明されました。")
    else:
        print("🚨 AUDIT RESULT: FAILED (Tampering or Desync Detected)")
        print("   不整合または改ざんが検知されました。")
    print("------------------------------------------")

if __name__ == "__main__":
    verify_audit_chain()
