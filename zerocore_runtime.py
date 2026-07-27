import json
import hashlib
from datetime import datetime

def run_zerocore_full():
    print("=== ZeroCore Multi-Layer Runtime Initiating ===")
    
    # 1. Boot & Capability Verification
    with open("Layer0_Boot/boot_record.json", "r") as f:
        boot_record = json.load(f)
    with open("Layer3_Registry/capability_registry.json", "r") as f:
        cap_reg = json.load(f)
    print(f"[Layer 0 Boot] Initialized: {boot_record['boot_id']}")
    
    # 2. AI Planner Loading (Layer 6)
    with open("Layer6_AI/planner.json", "r") as f:
        ai_plan = json.load(f)
    print(f"[Layer 6 AI] Loaded Plan: {ai_plan['plan_id']} for Agent '{ai_plan['target_agent']}'")
    
    # 3. Process Check (Layer 2)
    with open("Layer2_ObjectSystem/process_table.json", "r") as f:
        proc_table = json.load(f)
    agent_proc = next((p for p in proc_table["active_processes"] if p["process_name"] == ai_plan["target_agent"]), None)
    
    if not agent_proc or agent_proc["state"] != "RUNNING":
        print("[SECURITY ERROR] AI Agent process is not active!")
        return

    print(f"[Layer 2 Process] Active PID: {agent_proc['pid']} ({agent_proc['process_name']})")
    
    # 4. Execute AI Planned Task -> Business State Transition (Layer 5)
    for task in ai_plan["tasks"]:
        req_cap = task["required_capability"]
        
        # Capability Boundary Guard
        if req_cap in agent_proc["capabilities_held"]:
            print(f"[Layer 3 Capability] Granted: {req_cap}")
            
            # Update Business Registry (Layer 5)
            with open("Layer5_Business/invoice_registry.json", "r+") as f:
                inv_data = json.load(f)
                for inv in inv_data["invoices"]:
                    if inv["invoice_id"] == task["target_invoice"]:
                        inv["status"] = "APPROVED"
                        print(f"[Layer 5 Business] Invoice '{inv['invoice_id']}' Status Changed: DRAFT -> APPROVED")
                f.seek(0)
                json.dump(inv_data, f, indent=2)
                f.truncate()
                
            # Commit Audit Record (Layer 4)
            commit_audit(f"INVOICE_APPROVED_{task['target_invoice']}", agent_proc["process_name"])
        else:
            print(f"[SECURITY ALERT] Unauthorized Task Attempt: {task['action']}")

def commit_audit(event_type, actor):
    audit_file = "Layer4_Audit/audit_chain.json"
    with open(audit_file, "r") as f:
        audit_chain = json.load(f)
        
    records = audit_chain["records"]
    last_record = records[-1]
    
    new_seq = last_record["sequence"] + 1
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    prev_hash = last_record["state_hash"]
    
    hash_payload = f"{new_seq}{timestamp}{event_type}{actor}{prev_hash}".encode('utf-8')
    new_hash = hashlib.sha256(hash_payload).hexdigest()
    
    new_entry = {
        "sequence": new_seq,
        "timestamp": timestamp,
        "event_id": f"evt_run_{new_seq:03d}",
        "event_type": event_type,
        "actor": actor,
        "capability_verified": True,
        "state_hash": new_hash,
        "prev_hash": prev_hash,
        "status": "COMMITTED"
    }
    
    records.append(new_entry)
    audit_chain["total_records"] = len(records)
    
    with open(audit_file, "w") as f:
        json.dump(audit_chain, f, indent=2)
        
    print(f"[Layer 4 Audit] Cryptographic Block Committed! Sequence: #{new_seq} | Hash: {new_hash[:16]}...")

if __name__ == "__main__":
    run_zerocore_full()
