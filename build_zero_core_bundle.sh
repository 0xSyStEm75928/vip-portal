#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.bundle.json"

echo "[*] Building Bundle..."

jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" \
  --slurpfile export "$ROOT/ZERO_CORE.export.json" '
{
  bundle_version:"1.0.0",
  generated:(now|floor),
  master:$master[0],
  export:$export[0]
}
' > "$OUT"

echo "[OK] $OUT"
