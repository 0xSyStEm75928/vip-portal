#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.export.json"

echo "[*] Building Export..."

jq -n \
  --slurpfile release "$ROOT/ZERO_CORE.release.json" \
  --slurpfile catalog "$ROOT/ZERO_CORE.catalog.json" '
{
  export_version:"1.0.0",
  generated:(now|floor),
  release:$release[0],
  catalog:$catalog[0]
}
' > "$OUT"

echo "[OK] $OUT"
