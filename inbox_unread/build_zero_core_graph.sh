#!/bin/ash
#
# ZERO_CORE Dependency Graph Builder
#

set -eu

ROOT="${1:-./json_core}"
INDEX="$ROOT/ZERO_CORE.index.json"
GRAPH="$ROOT/ZERO_CORE.graph.json"

if [ ! -f "$INDEX" ]; then
    echo "[ERROR] Missing: $INDEX"
    exit 1
fi

echo "[*] Building Dependency Graph..."

jq '
{
  version: "1.0.0",
  generated: (now | floor),
  files:
    map({
      file,
      sha256,
      size
    }),
  summary: {
    total_files: length,
    total_bytes: (map(.size) | add)
  }
}
' "$INDEX" > "$GRAPH"

echo "[OK] $GRAPH"
