#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

RELEASE="$ROOT/ZERO_CORE.release_candidate.json"
VERSION="$ROOT/ZERO_CORE.version_snapshot.json"
MANIFEST="$ROOT/ZERO_CORE.final_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 40 RELEASE CANDIDATE"


# -----------------------------------------------------
# Release Candidate
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 release_candidate_version:"1.0.0",
 generated_at:$t,

 release_line:"ZERO_CORE",

 included:[
  "core",
  "runtime",
  "authority",
  "profile",
  "security",
  "ai",
  "plugin",
  "validation",
  "operation",
  "distribution"
 ],

 status:"CANDIDATE"
}
' > "$RELEASE"


# -----------------------------------------------------
# Version Snapshot
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 version_snapshot_version:"1.0.0",
 generated_at:$t,

 core_version:"1.0.0",

 snapshot:[
  "architecture",
  "configuration",
  "runtime",
  "security",
  "deployment"
 ],

 immutable:true
}
' > "$VERSION"


# -----------------------------------------------------
# Final Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile release "$RELEASE" \
 --slurpfile version "$VERSION" \
 --arg t "$TIME" '

{
 final_manifest_version:"1.0.0",
 generated_at:$t,

 release:$release[0],
 version:$version[0],

 state:"RELEASE_CANDIDATE_READY"
}
' > "$MANIFEST"


echo
echo "[OK] RELEASE  -> $RELEASE"
echo "[OK] VERSION   -> $VERSION"
echo "[OK] MANIFEST  -> $MANIFEST"
echo
echo "[SUCCESS] FAST STAGE 40 BUILD_SUCCESS"
echo "[STATUS] ZERO_CORE_RELEASE_CANDIDATE_READY"
