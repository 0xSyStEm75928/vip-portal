#!/bin/bash
# ==============================================================================
# ZERO_CORE Existing Registry Inspector
# 目的: 新規ファイル作成を止め、既存のレジストリ・テナントマップから顧客接続口を自動抽出する
# ==============================================================================

echo "=== [1] ZERO_CORE / Registry 存在チェック ==="
TARGET_FILES=(
  "json_core/ZERO_CORE.registry.json"
  "json_core/ZERO_CORE.service_registry.json"
  "json_core/ZERO_CORE.tenant_package_map.json"
  "json_core/json/registry.index.json"
  "json_core/ZERO_CORE.customer.json"
  "json_core/ZERO_CORE.tenant.json"
  "json_core/ZERO_CORE.queue.json"
  "json_core/json/invoice_registry.json"
  "008_execution_log_registry.json"
)

for file in "${TARGET_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "[FOUND] $file ($(stat -c%s "$file" 2>/dev/null || stat -f%z "$file") bytes)"
  else
    echo "[MISSING] $file"
  fi
done

echo ""
echo "=== [2] 既存JSON内の主要識別子（tenant/customer/service/package）抽出 ==="
for file in "${TARGET_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "--- Content Summary: $file ---"
    grep -E "tenant|customer|package|service|queue|status|id" "$file" | head -n 20
    echo ""
  fi
done

