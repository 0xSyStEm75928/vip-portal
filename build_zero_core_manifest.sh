#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.manifest.json"

echo "[*] Building Manifest (Ultra-Fast)..."

jq -n \
    --slurpfile idx "$ROOT/ZERO_CORE.index.json" \
    --slurpfile ids "$ROOT/ZERO_CORE.ids.json" \
    --slurpfile ver "$ROOT/ZERO_CORE.versions.json" \
    --slurpfile hash "$ROOT/ZERO_CORE.hashes.json" \
    --slurpfile schema "$ROOT/ZERO_CORE.schema_map.json" \
    --slurpfile keys "$ROOT/ZERO_CORE.keys.json" '
{
    manifest_version:"1.0.0",
    generated_at:(now|floor),
    index:$idx[0],
    ids:$ids[0],
    versions:$ver[0],
    hashes:$hash[0],
    schemas:$schema[0],
    keys:$keys[0]
}
' > "$OUT"

echo "[OK] $OUT"
