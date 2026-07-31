#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.rewrite_plan.json"

echo "[*] Building Rewrite Plan..."

jq -n \
  --slurpfile bundle "$ROOT/ZERO_CORE.bundle.json" \
  --slurpfile keys "$ROOT/ZERO_CORE.keys.json" \
  --slurpfile versions "$ROOT/ZERO_CORE.versions.json" '
{
  plan_version:"1.0.0",
  generated:(now|floor),
  source:"ZERO_CORE.bundle.json",
  rewrite_targets:($bundle[0].master.manifest.index // [] | map(.file)),
  keys:$keys[0],
  versions:$versions[0]
}
' > "$OUT"

echo "[OK] $OUT"
