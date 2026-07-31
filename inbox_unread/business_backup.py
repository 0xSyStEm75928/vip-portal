import json
import shutil
import os
from datetime import datetime, timezone

BASE = "json_core"
BACKUP_ROOT = "json_backup"

timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
backup_dir = os.path.join(BACKUP_ROOT, timestamp)

os.makedirs(backup_dir, exist_ok=True)

copied = []

for name in sorted(os.listdir(BASE)):
    if name.endswith(".json"):
        src = os.path.join(BASE, name)
        dst = os.path.join(backup_dir, name)
        shutil.copy2(src, dst)
        copied.append(name)

report = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),
    "backup_directory": backup_dir,
    "files": copied,
    "count": len(copied)
}

with open(
    os.path.join(backup_dir, "backup_report.json"),
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        report,
        f,
        indent=2,
        ensure_ascii=False
    )

print("BUSINESS BACKUP COMPLETE")
print("FILES :", len(copied))
print("DIR   :", backup_dir)
