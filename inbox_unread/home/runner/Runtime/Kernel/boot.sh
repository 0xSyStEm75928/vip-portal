#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "      Sun and Night Engine - Bootloader           "
echo "  Motto: AI proposes. Runtime decides.            "
echo "=================================================="

# Integrity check execution
if [[ -f "Runtime/Kernel/integrity_check.sh" ]]; then
    bash Runtime/Kernel/integrity_check.sh
fi

echo "[+] Kernel Boot Complete. Operating in Deterministic Mode."
