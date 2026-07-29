#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

BUNDLE="$ROOT/ZERO_CORE.export_bundle.json"
MAP="$ROOT/ZERO_CORE.distribution_map.json"
PACKAGE="$ROOT/ZERO_CORE.artifact_package.json"
MANIFEST="$ROOT/ZERO_CORE.distribution_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 39 DISTRIBUTION / EXPORT"


# -----------------------------------------------------
# Export Bundle
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 export_bundle_version:"1.0.0",
 generated_at:$t,

 includes:[
  "core",
  "runtime",
  "security",
  "profile",
  "validation",
  "operation",
  "documentation"
 ],

 status:"PACKAGED"
}
' > "$BUNDLE"


# -----------------------------------------------------
# Distribution Map
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 distribution_map_version:"1.0.0",
 generated_at:$t,

 targets:[
  "personal",
  "personal_plus",
  "small_business",
  "enterprise"
 ],

 channels:[
  "local",
  "private",
  "managed"
 ],

 status:"READY"
}
' > "$MAP"


# -----------------------------------------------------
# Artifact Package
# -----------------------------------------------------

jq -n \
 --slurpfile bundle "$BUNDLE" \
 --slurpfile map "$MAP" \
 --arg t "$TIME" '

{
 artifact_package_version:"1.0.0",
 generated_at:$t,

 bundle:$bundle[0],
 distribution:$map[0],

 integrity:"REQUIRED",

 status:"READY"
}
' > "$PACKAGE"


# -----------------------------------------------------
# Distribution Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile package "$PACKAGE" \
 --arg t "$TIME" '

{
 distribution_manifest_version:"1.0.0",
 generated_at:$t,

 package:$package[0],

 state:"DISTRIBUTION_READY"
}
' > "$MANIFEST"


echo
echo "[OK] BUNDLE   -> $BUNDLE"
echo "[OK] MAP      -> $MAP"
echo "[OK] PACKAGE  -> $PACKAGE"
echo "[OK] MANIFEST -> $MANIFEST"
echo
echo "[SUCCESS] FAST STAGE 39 BUILD_SUCCESS"
