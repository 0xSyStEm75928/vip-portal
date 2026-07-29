#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.master.json"

echo "[*] Building ZERO_CORE Master..."

jq -n \
  --slurpfile manifest "$ROOT/ZERO_CORE.manifest.json" \
  --slurpfile registry "$ROOT/ZERO_CORE.registry.json" \
  --slurpfile runtime "$ROOT/ZERO_CORE.runtime.json" \
  --slurpfile integrity "$ROOT/ZERO_CORE.integrity.json" \
  '{
    master_version:"1.0.0",
    generated:(now|floor),
    manifest:$manifest[0],
    registry:$registry[0],
    runtime:$runtime[0],
    integrity:$integrity[0]
  }' > "$OUT"

echo "[OK] $OUT"
