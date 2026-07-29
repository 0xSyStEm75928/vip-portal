#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
IN="$ROOT/ZERO_CORE.30pack.json"
OUT="$ROOT/ZERO_CORE.30meta.json"

echo "[*] Building 30-Pack Metadata..."

jq '
{
  meta_version:"1.0.0",
  generated:(now|floor),
  total_files:length,
  total_bytes:(map(.bytes)|add),
  total_lines:(map(.lines)|add),
  schema_files:(map(select(.schema==true))|length),
  json_files:(map(select(.schema==false))|length),
  assets:.
}
' "$IN" > "$OUT"

echo "[OK] $OUT"
