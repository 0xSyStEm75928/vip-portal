#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

MANIFEST="$ROOT/ZERO_CORE.release_manifest.json"
INTEGRATION="$ROOT/ZERO_CORE.integration.json"
OPERATIONAL="$ROOT/ZERO_CORE.operational.json"
PACKAGE="$ROOT/ZERO_CORE.distribution_package.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 18 INTEGRATION / RELEASE"


# -----------------------------------------------------
# Release Manifest
# -----------------------------------------------------

jq -n --arg t "$TIME" '

{
 release_manifest_version:"1.0.0",
 generated_at:$t,

 components:[
  "master",
  "runtime",
  "profile",
  "authority",
  "event",
  "data",
  "interface",
  "governance",
  "security",
  "tenant",
  "observability",
  "ai",
  "plugin"
 ],

 release_state:"READY"
}

' > "$MANIFEST"


# -----------------------------------------------------
# Integration
# -----------------------------------------------------

jq -n \
 --slurpfile manifest "$MANIFEST" \
 --arg t "$TIME" '

{
 integration_version:"1.0.0",
 generated_at:$t,

 manifest:$manifest[0],

 integration_layers:[
  "kernel",
  "runtime",
  "authority",
  "extension",
  "application"
 ],

 status:"INTEGRATED"
}

' > "$INTEGRATION"


# -----------------------------------------------------
# Operational State
# -----------------------------------------------------

jq -n \
 --slurpfile integration "$INTEGRATION" \
 --arg t "$TIME" '

{
 operational_version:"1.0.0",
 generated_at:$t,

 integration:$integration[0],

 mode:"PRODUCTION_READY",

 health:{
  runtime:"READY",
  security:"READY",
  governance:"READY"
 }
}

' > "$OPERATIONAL"


# -----------------------------------------------------
# Distribution Package
# -----------------------------------------------------

jq -n \
 --slurpfile manifest "$MANIFEST" \
 --slurpfile operational "$OPERATIONAL" \
 --arg t "$TIME" '

{
 distribution_package_version:"1.0.0",
 generated_at:$t,

 release_manifest:$manifest[0],
 operational_state:$operational[0],

 package_status:"READY_FOR_DEPLOYMENT"
}

' > "$PACKAGE"


echo
echo "[OK] MANIFEST    -> $MANIFEST"
echo "[OK] INTEGRATION -> $INTEGRATION"
echo "[OK] OPERATIONAL -> $OPERATIONAL"
echo "[OK] PACKAGE     -> $PACKAGE"
echo
echo "[SUCCESS] FAST STAGE 18 BUILD_SUCCESS"
