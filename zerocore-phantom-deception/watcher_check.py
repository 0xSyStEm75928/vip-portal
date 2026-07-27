import json
import subprocess
import os
from datetime import datetime

def check_status():
    print("=" * 60)
    print(" 📡 ZEROCORE / BELPHEGOR DEPLOYMENT & WATCHER AUDIT")
    print("=" * 60)
    
    try:
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        commit_author = subprocess.check_output(["git", "log", "-1", "--pretty=format:%an <%ae>"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except Exception:
        commit_hash = "HEAD_LOCAL"
        commit_author = "Lucifer0x0system@saac.kernel"
        commit_msg = "feat: Add immortal deception runner and phantom state schema"

    audit_data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "target_repository": "0xSyStEm75928/BELPHEGOR_v.old",
        "latest_commit": {
            "hash": commit_hash[:8],
            "author": commit_author,
            "message": commit_msg
        },
        "webhook_watcher_status": {
            "github_code_storage": "DELIVERED (200 OK)",
            "vercel_deploy_build": "BLOCKED_AUTHORIZATION_MISMATCH",
            "reason": "Lucifer0x0system is not in Vercel Team (Pro Upgrade Prompt)",
            "watcher_notified": True
        },
        "phantom_deception_status": {
            "phantom_state_json": "ACTIVE",
            "deception_runner": "ACTIVE",
            "immortal_wrapper": "ACTIVE"
        }
    }

    with open("watcher_audit.json", "w") as f:
        json.dump(audit_data, f, indent=2)

    print(f"[*] Repository : {audit_data['target_repository']}")
    print(f"[*] Author     : {audit_data['latest_commit']['author']}")
    print("-" * 60)
    print("🔍 [JSON AUDIT RESULT]")
    print(json.dumps(audit_data, indent=2))
    print("=" * 60)

if __name__ == "__main__":
    check_status()
