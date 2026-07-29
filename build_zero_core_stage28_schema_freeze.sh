#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

SCHEMA="$ROOT/ZERO_CORE.schema_lock.json"
VERSION="$ROOT/ZERO_CORE.schema_version.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 28 SCHEMA FREEZE"

jq -n --arg t "$TIME" '
{
 schema_lock_version:"1.0.0",
 generated_at:$t,

 frozen:true,

 protected:[
  "identity",
  "permission",
  "policy",
  "runtime",
  "release"
 ]
}
' > "$SCHEMA"


jq -n --arg t "$TIME" '
{
 schema_version:"1.0.0",
 generated_at:$t,

 current:"1.0.0",
 compatibility:[
  "1.x"
 ]
}
' > "$VERSION"


echo "[SUCCESS] FAST STAGE 28 BUILD_SUCCESS"
