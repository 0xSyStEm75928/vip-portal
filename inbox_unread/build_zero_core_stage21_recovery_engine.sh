#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

BACKUP="$ROOT/ZERO_CORE.backup.json"
SNAPSHOT="$ROOT/ZERO_CORE.snapshot_registry.json"
RECOVERY="$ROOT/ZERO_CORE.recovery_plan.json"
MIGRATION="$ROOT/ZERO_CORE.migration.json"
RESTORE="$ROOT/ZERO_CORE.restore_state.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 21 BACKUP / RECOVERY / MIGRATION"


# -----------------------------------------------------
# Backup Registry
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 backup_version:"1.0.0",
 generated_at:$t,

 strategy:[
  "snapshot",
  "archive",
  "restore"
 ],

 backups:[],
 status:"READY"
}
' > "$BACKUP"


# -----------------------------------------------------
# Snapshot Registry
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 snapshot_registry_version:"1.0.0",
 generated_at:$t,

 snapshots:[],

 retention_policy:{
  enabled:true,
  mode:"VERSIONED"
 }
}
' > "$SNAPSHOT"


# -----------------------------------------------------
# Recovery Plan
# -----------------------------------------------------

jq -n \
 --slurpfile backup "$BACKUP" \
 --slurpfile snapshot "$SNAPSHOT" \
 --arg t "$TIME" '

{
 recovery_plan_version:"1.0.0",
 generated_at:$t,

 backup:$backup[0],
 snapshot:$snapshot[0],

 recovery_steps:[
  "detect",
  "validate",
  "restore",
  "verify"
 ],

 status:"READY"
}
' > "$RECOVERY"


# -----------------------------------------------------
# Migration
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 migration_version:"1.0.0",
 generated_at:$t,

 supported:[
  "schema_upgrade",
  "profile_change",
  "version_transition"
 ],

 migrations:[],
 status:"READY"
}
' > "$MIGRATION"


# -----------------------------------------------------
# Restore State
# -----------------------------------------------------

jq -n \
 --slurpfile recovery "$RECOVERY" \
 --slurpfile migration "$MIGRATION" \
 --arg t "$TIME" '

{
 restore_state_version:"1.0.0",
 generated_at:$t,

 recovery:$recovery[0],
 migration:$migration[0],

 state:"STANDBY"
}
' > "$RESTORE"


echo
echo "[OK] BACKUP    -> $BACKUP"
echo "[OK] SNAPSHOT  -> $SNAPSHOT"
echo "[OK] RECOVERY  -> $RECOVERY"
echo "[OK] MIGRATION -> $MIGRATION"
echo "[OK] RESTORE   -> $RESTORE"
echo
echo "[SUCCESS] FAST STAGE 21 BUILD_SUCCESS"
