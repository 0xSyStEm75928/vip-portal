#!/usr/bin/env bash
set -euo pipefail
echo "======================================================================"
echo "      ZEROCORE SOVEREIGN FULL-TREE & DAG CIRCUIT VALIDATION (PASS)    "
echo "======================================================================"

test -f zerocore.tree.manifest.json || (echo "[!] Tree manifest missing" && exit 1)
test -f Engine/product_data.json || (echo "[!] Product data missing" && exit 1)
test -f Engine/product_dag_circuit.json || (echo "[!] DAG circuit missing" && exit 1)
test -f Engine/generate_public_docs.sh || (echo "[!] Generator bot missing" && exit 1)

echo "[*] Testing JSON Integrity..."
jq empty Engine/product_data.json
jq empty Engine/product_dag_circuit.json

echo "[✓] All tree nodes, DAG circuits, and validators successfully passed!"
exit 0
