#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.release.json"

echo "[*] Building Release..."

jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" \
  --slurpfile gov "$ROOT/ZERO_CORE.governance.json" '
{
  release_version:"1.0.0",
  generated:(now|floor),
  master:$master[0],
  governance:$gov[0]
}
' > "$OUT"

echo "[OK] $OUT"
