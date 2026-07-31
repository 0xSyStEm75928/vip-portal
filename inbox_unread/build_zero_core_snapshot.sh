#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.snapshot.json"

echo "[*] Building Snapshot..."

jq -n \
  --slurpfile manifest "$ROOT/ZERO_CORE.manifest.json" \
  --slurpfile pipeline "$ROOT/ZERO_CORE.pipeline.json" '
{
  snapshot_version:"1.0.0",
  generated:(now|floor),
  manifest:$manifest[0],
  pipeline:$pipeline[0]
}
' > "$OUT"

echo "[OK] $OUT"
