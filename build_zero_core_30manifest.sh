#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.30manifest.json"

echo "[*] Building 30-Pack Manifest..."

jq -n \
  --slurpfile meta "$ROOT/ZERO_CORE.30meta.json" \
  --slurpfile stats "$ROOT/ZERO_CORE.30stats.json" \
  --slurpfile index "$ROOT/ZERO_CORE.30index.json" \
  --slurpfile hashes "$ROOT/ZERO_CORE.30hashmap.json" '
{
  manifest_version:"1.0.0",
  generated:(now|floor),
  metadata:$meta[0],
  statistics:$stats[0],
  index:$index[0],
  hashes:$hashes[0]
}
' > "$OUT"

echo "[OK] $OUT"
