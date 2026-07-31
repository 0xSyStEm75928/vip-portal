#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

echo "[*] FAST STAGE..."

jq '{graph}' \
"$ROOT/ZERO_CORE.graph_map.json" \
> "$ROOT/ZERO_CORE.graph.json"

jq '
{
files:.total_files,
bytes:.total_bytes,
lines:.total_lines
}
' "$ROOT/ZERO_CORE.30meta.json" \
> "$ROOT/ZERO_CORE.metrics.json"

jq -n \
 --slurpfile g "$ROOT/ZERO_CORE.graph.json" \
 --slurpfile m "$ROOT/ZERO_CORE.metrics.json" '
{
graph:$g[0],
metrics:$m[0]
}
' > "$ROOT/ZERO_CORE.runtime.json"

jq -n \
 --slurpfile runtime "$ROOT/ZERO_CORE.runtime.json" \
 --slurpfile manifest "$ROOT/ZERO_CORE.manifest.json" '
{
version:"4.0.0",
runtime:$runtime[0],
manifest:$manifest[0]
}
' > "$ROOT/ZERO_CORE.master.json"

echo "[OK]"
