#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.version_report.json"

echo "[*] Building Version Report..."

jq '
group_by(.version)
| map({
    version:.[0].version,
    count:length
})
' "$ROOT/ZERO_CORE.versions.json" > "$OUT"

echo "[OK] $OUT"
