#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

REGISTRY="$ROOT/ZERO_CORE.config_registry.json"
LOADER="$ROOT/ZERO_CORE.environment_loader.json"
CONFIG="$ROOT/ZERO_CORE.runtime_config.json"
MANIFEST="$ROOT/ZERO_CORE.config_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 37 CONFIGURATION LOADER"


jq -n --arg t "$TIME" '
{
 config_registry_version:"1.0.0",
 generated_at:$t,

 configs:[
  "runtime",
  "security",
  "profile",
  "policy",
  "deployment"
 ],

 status:"READY"
}
' > "$REGISTRY"


jq -n --arg t "$TIME" '
{
 environment_loader_version:"1.0.0",
 generated_at:$t,

 sources:[
  "json",
  "environment",
  "runtime"
 ],

 priority:[
  "policy",
  "environment",
  "default"
 ],

 status:"READY"
}
' > "$LOADER"


jq -n --arg t "$TIME" '
{
 runtime_config_version:"1.0.0",
 generated_at:$t,

 mode:"STRICT",

 defaults:{
  profile:"01_PERSONAL",
  runtime:"enabled",
  audit:true
 },

 status:"LOADED"
}
' > "$CONFIG"


jq -n \
 --slurpfile registry "$REGISTRY" \
 --slurpfile loader "$LOADER" \
 --slurpfile config "$CONFIG" \
 --arg t "$TIME" \
 '
{
 config_manifest_version:"1.0.0",
 generated_at:$t,

 registry:$registry[0],
 loader:$loader[0],
 config:$config[0],

 state:"CONFIG_READY"
}
' > "$MANIFEST"


echo
echo "[OK] REGISTRY -> $REGISTRY"
echo "[OK] LOADER   -> $LOADER"
echo "[OK] CONFIG   -> $CONFIG"
echo "[OK] MANIFEST -> $MANIFEST"
echo
echo "[SUCCESS] FAST STAGE 37 BUILD_SUCCESS"
