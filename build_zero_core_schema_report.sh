#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.schema_report.json"

echo "[*] Building Schema Report..."

jq '
group_by(.schema)
| map({
    schema:.[0].schema,
    count:length
})
' "$ROOT/ZERO_CORE.schema_map.json" > "$OUT"

echo "[OK] $OUT"
