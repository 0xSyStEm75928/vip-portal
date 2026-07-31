#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.pipeline.json"

echo "[*] Building Pipeline..."

jq -n \
  --slurpfile plan "$ROOT/ZERO_CORE.rewrite_plan.json" \
  --slurpfile queue "$ROOT/ZERO_CORE.queue.json" '
{
  pipeline_version:"1.0.0",
  generated:(now|floor),
  plan:$plan[0],
  queue:$queue[0]
}
' > "$OUT"

echo "[OK] $OUT"
