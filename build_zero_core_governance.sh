#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.governance.json"

echo "[*] Building Governance..."

jq -n '
{
  governance_version:"1.0.0",
  immutable:true,
  audit_enabled:true,
  hash_algorithm:"SHA-256",
  update_policy:"MANUAL_REVIEW",
  schema_policy:"STRICT"
}
' > "$OUT"

echo "[OK] $OUT"
