#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

ENV="$ROOT/ZERO_CORE.environment.json"
PROFILE="$ROOT/ZERO_CORE.deployment_profile.json"
MATRIX="$ROOT/ZERO_CORE.package_matrix.json"
MANIFEST="$ROOT/ZERO_CORE.deployment_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 33 DEPLOYMENT PACKAGE"


# -----------------------------------------------------
# Environment
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 environment_version:"1.0.0",
 generated_at:$t,

 environments:[
  "local",
  "private",
  "managed",
  "enterprise"
 ],

 runtime:"ZERO_CORE",

 status:"READY"
}
' > "$ENV"


# -----------------------------------------------------
# Deployment Profile
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 deployment_profile_version:"1.0.0",
 generated_at:$t,

 profiles:[
  {
   name:"01_PERSONAL",
   target:"individual"
  },
  {
   name:"02_PERSONAL_PLUS",
   target:"advanced_individual"
  },
  {
   name:"03_SMALL_BUSINESS",
   target:"organization"
  },
  {
   name:"04_ENTERPRISE",
   target:"enterprise"
  }
 ],

 status:"READY"
}
' > "$PROFILE"


# -----------------------------------------------------
# Package Matrix
# -----------------------------------------------------

jq -n \
 --slurpfile profile "$PROFILE" \
 --arg t "$TIME" '

{
 package_matrix_version:"1.0.0",
 generated_at:$t,

 profiles:$profile[0],

 packages:[
  "core",
  "standard",
  "business",
  "enterprise"
 ],

 status:"MAPPED"
}
' > "$MATRIX"


# -----------------------------------------------------
# Deployment Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile env "$ENV" \
 --slurpfile matrix "$MATRIX" \
 --arg t "$TIME" '

{
 deployment_manifest_version:"1.0.0",
 generated_at:$t,

 environment:$env[0],
 package_matrix:$matrix[0],

 deployment_state:"READY"
}
' > "$MANIFEST"


echo
echo "[OK] ENVIRONMENT -> $ENV"
echo "[OK] PROFILE     -> $PROFILE"
echo "[OK] MATRIX      -> $MATRIX"
echo "[OK] MANIFEST    -> $MANIFEST"
echo
echo "[SUCCESS] FAST STAGE 33 BUILD_SUCCESS"
