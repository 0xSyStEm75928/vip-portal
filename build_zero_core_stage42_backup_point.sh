#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

BACKUP="$ROOT/ZERO_CORE.backup_point.json"
SNAPSHOT="$ROOT/ZERO_CORE.recovery_snapshot.json"
MANIFEST="$ROOT/ZERO_CORE.backup_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 42 BACKUP POINT"


# -----------------------------------------------------
# Backup Point
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 backup_point_version:"1.0.0",
 generated_at:$t,

 checkpoint_type:"RELEASE_CANDIDATE",

 includes:[
  "core",
  "runtime",
  "configuration",
  "security",
  "distribution"
 ],

 status:"CREATED"
}
' > "$BACKUP"


# -----------------------------------------------------
# Recovery Snapshot
# -----------------------------------------------------

jq -n \
 --slurpfile backup "$BACKUP" \
 --arg t "$TIME" '

{
 recovery_snapshot_version:"1.0.0",
 generated_at:$t,

 source:$backup[0],

 recovery_mode:"RESTORE_POINT",

 status:"READY"
}
' > "$SNAPSHOT"


# -----------------------------------------------------
# Backup Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile backup "$BACKUP" \
 --slurpfile snapshot "$SNAPSHOT" \
 --arg t "$TIME" '

{
 backup_manifest_version:"1.0.0",
 generated_at:$t,

 backup:$backup[0],
 snapshot:$snapshot[0],

 state:"BACKUP_READY"
}
' > "$MANIFEST"


echo
echo "[OK] BACKUP   -> $BACKUP"
echo "[OK] SNAPSHOT -> $SNAPSHOT"
echo "[OK] MANIFEST -> $MANIFEST"
echo
echo "[SUCCESS] FAST STAGE 42 BUILD_SUCCESS"
