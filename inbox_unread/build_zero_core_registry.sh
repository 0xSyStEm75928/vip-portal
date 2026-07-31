#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.registry.json"

echo "[*] Building Registry..."

jq -n \
 --slurpfile manifest "$ROOT/ZERO_CORE.manifest.json" \
 --slurpfile inventory "$ROOT/ZERO_CORE.inventory.json" '
{
 registry_version:"1.0.0",
 manifest:$manifest[0],
 inventory:$inventory[0]
}
' > "$OUT"

echo "[OK] $OUT"
