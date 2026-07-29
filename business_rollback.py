import os
import json
import shutil
import sys
from datetime import datetime, timezone

BASE = "json_core"
BACKUP_ROOT = "json_backup"

OUTPUT = os.path.join(
    BASE,
    "rollback_result.json"
)


def latest_backup():
    if not os.path.exists(BACKUP_ROOT):
        return None

    dirs = [
        d for d in os.listdir(BACKUP_ROOT)
        if os.path.isdir(
            os.path.join(BACKUP_ROOT, d)
        )
    ]

    if not dirs:
        return None

    return sorted(dirs)[-1]


def restore(backup_dir):

    src_dir = os.path.join(
        BACKUP_ROOT,
        backup_dir
    )

    restored = []

    for name in os.listdir(src_dir):

        if not name.endswith(".json"):
            continue

        if name == "backup_report.json":
            continue

        src = os.path.join(
            src_dir,
            name
        )

        dst = os.path.join(
            BASE,
            name
        )

        shutil.copy2(
            src,
            dst
        )

        restored.append(name)

    return restored


backup = (
    sys.argv[1]
    if len(sys.argv) > 1
    else latest_backup()
)


result = {
    "version": "1.0.0",
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "policy": {
        "manual_confirmation_required": True,
        "restore_only": True
    },

    "backup_used": backup,
    "status": "FAILED",
    "restored_files": []
}


if backup:

    files = restore(backup)

    result["status"] = "RESTORED"
    result["restored_files"] = files


with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=2,
        ensure_ascii=False
    )


print("BUSINESS ROLLBACK COMPLETE")
print("STATUS:", result["status"])
print("OUTPUT:", OUTPUT)
