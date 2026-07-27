import json
import subprocess
import urllib.request
from datetime import datetime

def fetch_repo_events():
    repo = "0xSyStEm75928/BELPHEGOR_v.old"
    url = f"https://api.github.com/repos/{repo}/events"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    print("=" * 60)
    print(" 📡 ZEROCORE OFFER & EVENT WATCHER (JSON AUDIT)")
    print("=" * 60)
    
    try:
        with urllib.request.urlopen(req) as response:
            events = json.loads(response.read().decode())
            
            # 直近のイベントからオファーやインタラクション（Push, Watch, Fork, Issueなど）を抽出
            summary_events = []
            for ev in events[:5]:
                summary_events.append({
                    "event_id": ev.get("id"),
                    "type": ev.get("type"),
                    "actor": ev.get("actor", {}).get("login"),
                    "created_at": ev.get("created_at"),
                    "payload_size": len(str(ev.get("payload")))
                })
                
            output = {
                "audit_timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "target_repo": repo,
                "status": "ONLINE_LISTENING",
                "latest_events_count": len(summary_events),
                "offers_and_triggers": summary_events if summary_events else "NO_NEW_EXTERNAL_OFFERS_YET"
            }
            
            with open("offer_check.json", "w") as f:
                json.dump(output, f, indent=2)
                
            print(json.dumps(output, indent=2))
            
    except Exception as e:
        print(f"❌ [FETCH ERROR]: {e}")

if __name__ == "__main__":
    fetch_repo_events()
