#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

TENANT="$ROOT/ZERO_CORE.tenant_package_map.json"
PACKAGE="$ROOT/ZERO_CORE.deployment_package.json"
MANIFEST="$ROOT/ZERO_CORE.tenant_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE STAGE 48 TENANT PACKAGE MAP"


# -----------------------------------------------------
# Tenant Package Map
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 tenant_package_map_version:"1.0.0",
 generated_at:$t,

 packages:{
  personal:{
   profile:"01_PERSONAL",
   tenant:false,
   isolation:"local"
  },

  personal_plus:{
   profile:"02_PERSONAL_PLUS",
   tenant:false,
   isolation:"private"
  },

  small_business:{
   profile:"03_SMALL_BUSINESS",
   tenant:true,
   isolation:"organization"
  },

  enterprise:{
   profile:"04_ENTERPRISE",
   tenant:true,
   isolation:"multi_namespace"
  }
 },

 status:"MAPPED"
}
' > "$TENANT"


# -----------------------------------------------------
# Deployment Package
# -----------------------------------------------------

jq -n \
 --slurpfile tenant "$TENANT" \
 --arg t "$TIME" '

{
 deployment_package_version:"1.0.0",
 generated_at:$t,

 tenant_model:$tenant[0],

 deployment_targets:[
  "local",
  "private",
  "organization",
  "enterprise"
 ],

 deployment_state:"READY"
}
' > "$PACKAGE"


# -----------------------------------------------------
# Tenant Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile tenant "$TENANT" \
 --slurpfile package "$PACKAGE" \
 --arg t "$TIME" '

{
 tenant_manifest_version:"1.0.0",
 generated_at:$t,

 tenant_map:$tenant[0],
 deployment:$package[0],

 state:"TENANT_READY"
}
' > "$MANIFEST"


echo
echo "[OK] TENANT   -> $TENANT"
echo "[OK] PACKAGE  -> $PACKAGE"
echo "[OK] MANIFEST -> $MANIFEST"
echo
echo "[SUCCESS] STAGE 48 BUILD_SUCCESS"
