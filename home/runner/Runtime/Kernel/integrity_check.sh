#!/usr/bin/env bash
set -euo pipefail

echo "[*] Verifying Governance & Schema Integrity..."
REQUIRED_FILES=(
  "Governance/DESIGN_CHARTER.md"
  "Governance/THREAT_MODEL.md"
  "Schema/sun.event.v1.json"
  "Capabilities/capabilities.json"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "[CRITICAL ERROR] Missing integrity file: $file" >&2
    exit 1
  fi
done

echo "[+] All integrity checks passed."
