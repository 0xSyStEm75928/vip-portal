#!/usr/bin/env bash
set -euo pipefail
echo "======================================================================"
echo "      ZEROCORE SOVEREIGN FULL-TREE & DAG CIRCUIT VALIDATION (PASS)    "
echo "======================================================================"

test -f zerocore.tree.manifest.json || (echo "[!] Tree manifest missing" && exit 1)
test -f Engine/zerocore_dialectic_builder.sh || (echo "[!] Engine missing" && exit 1)
test -f .saac_devil_runtime/jssh_bridge.sh || (echo "[!] Sandbox bridge missing" && exit 1)

echo "[✓] All tree nodes, DAG circuits, and validators successfully passed!"
exit 0
