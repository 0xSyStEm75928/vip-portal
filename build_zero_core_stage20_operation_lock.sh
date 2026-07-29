#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

PROFILE="$ROOT/ZERO_CORE.operation_profile.json"
DEPLOY="$ROOT/ZERO_CORE.deployment_blueprint.json"
LOCK="$ROOT/ZERO_CORE.version_lock.json"
MANIFEST="$ROOT/ZERO_CORE.runtime_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 20 OPERATION / VERSION LOCK"


# -----------------------------------------------------
# Operation Profile
# -----------------------------------------------------

jq -n --arg t "$TIME" '

{
 operation_profile_version:"1.0.0",
 generated_at:$t,

 mode:"OPERATIONAL",

 enabled_layers:[
  "runtime",
  "authority",
  "profile",
  "security",
  "ai",
  "plugin",
  "validation"
 ],

 state:"READY"
}

' > "$PROFILE"


# -----------------------------------------------------
# Deployment Blueprint
# -----------------------------------------------------

jq -n --arg t "$TIME" '

{
 deployment_blueprint_version:"1.0.0",
 generated_at:$t,

 targets:[
  "personal",
  "personal_plus",
  "small_business",
  "enterprise"
 ],

 deployment_modes:[
  "local",
  "private",
  "managed"
 ],

 status:"READY"
}

' > "$DEPLOY"


# -----------------------------------------------------
# Version Lock
# -----------------------------------------------------

jq -n --arg t "$TIME" '

{
 version_lock_version:"1.0.0",
 generated_at:$t,

 core_version:"1.0.0",

 locked_components:[
  "kernel",
  "runtime",
  "authority",
  "security",
  "release"
 ],

 immutable:true
}

' > "$LOCK"


# -----------------------------------------------------
# Runtime Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile profile "$PROFILE" \
 --slurpfile deploy "$DEPLOY" \
 --slurpfile lock "$LOCK" \
 --arg t "$TIME" '

{
 runtime_manifest_version:"1.0.0",
 generated_at:$t,

 operation_profile:$profile[0],
 deployment:$deploy[0],
 version_lock:$lock[0],

 status:"OPERATIONAL_READY"
}

' > "$MANIFEST"


echo
echo "[OK] PROFILE  -> $PROFILE"
echo "[OK] DEPLOY   -> $DEPLOY"
echo "[OK] LOCK     -> $LOCK"
echo "[OK] MANIFEST -> $MANIFEST"
echo
echo "[SUCCESS] FAST STAGE 20 BUILD_SUCCESS"
