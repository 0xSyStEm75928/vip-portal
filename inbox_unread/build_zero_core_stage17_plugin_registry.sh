#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

PLUGIN="$ROOT/ZERO_CORE.plugin_registry.json"
MODULE="$ROOT/ZERO_CORE.module_registry.json"
POLICY="$ROOT/ZERO_CORE.extension_policy.json"
LOADER="$ROOT/ZERO_CORE.loader.json"
CATALOG="$ROOT/ZERO_CORE.catalog.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 17 PLUGIN / MODULE REGISTRY"


# -----------------------------------------------------
# Plugin Registry
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 plugin_registry_version:"1.0.0",
 generated_at:$t,
 registry_type:"PLUGIN",
 plugins:[],
 status:"STAGE_READY"
}
' > "$PLUGIN"


# -----------------------------------------------------
# Module Registry
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 module_registry_version:"1.0.0",
 generated_at:$t,
 modules:[
  {
   name:"core",
   type:"system",
   enabled:true
  }
 ],
 lifecycle:[
  "registered",
  "validated",
  "enabled",
  "disabled"
 ]
}
' > "$MODULE"


# -----------------------------------------------------
# Extension Policy
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 extension_policy_version:"1.0.0",
 generated_at:$t,
 rules:[
  "signature_required",
  "permission_required",
  "audit_required"
 ],
 default_action:"DENY"
}
' > "$POLICY"


# -----------------------------------------------------
# Loader
# -----------------------------------------------------

jq -n \
 --slurpfile modules "$MODULE" \
 --slurpfile policy "$POLICY" \
 --arg t "$TIME" '

{
 loader_version:"1.0.0",
 generated_at:$t,
 module_registry:$modules[0],
 extension_policy:$policy[0],
 loading_mode:"CONTROLLED"
}
' > "$LOADER"


# -----------------------------------------------------
# Catalog
# -----------------------------------------------------

jq -n \
 --slurpfile plugin "$PLUGIN" \
 --slurpfile modules "$MODULE" \
 --arg t "$TIME" '

{
 catalog_version:"1.0.0",
 generated_at:$t,
 plugin_registry:$plugin[0],
 module_registry:$modules[0],
 searchable:true
}
' > "$CATALOG"


echo
echo "[OK] PLUGIN  -> $PLUGIN"
echo "[OK] MODULE  -> $MODULE"
echo "[OK] POLICY  -> $POLICY"
echo "[OK] LOADER  -> $LOADER"
echo "[OK] CATALOG -> $CATALOG"
echo
echo "[SUCCESS] FAST STAGE 17 BUILD_SUCCESS"
