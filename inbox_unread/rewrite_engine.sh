#!/bin/ash
set -eu

# ----------------------------------------------------------------------
# ZERO_CORE Rewrite Engine (Safe Driver)
# Usage:
#   ./rewrite_engine.sh [TARGET_DIR] [MODE: --dry-run | --apply]
# ----------------------------------------------------------------------

ROOT="${1:-./json_core}"
MODE="${2:---dry-run}"

MASTER="$ROOT/ZERO_CORE.master.json"
BACKUP_DIR="$ROOT/backups/$(date +%Y%m%d_%H%M%S)"

if [ ! -f "$MASTER" ]; then
  echo "[ERROR] Master definition file not found: $MASTER"
  exit 1
fi

echo "=================================================="
echo "    ZERO_CORE REWRITE ENGINE                      "
echo "=================================================="
echo " [*] Master Input : $MASTER"
echo " [*] Target Dir   : $ROOT"
echo " [*] Engine Mode  : $MODE"
echo "--------------------------------------------------"

if [ "$MODE" = "--apply" ]; then
  echo " [*] Creating Backup -> $BACKUP_DIR"
  mkdir -p "$BACKUP_DIR"
fi

# 1. 変更計画の策定 (Planner)
TARGET_FILES=$(jq -r '.bundle.assets[].file' "$MASTER" 2>/dev/null || true)

if [ -z "$TARGET_FILES" ]; then
  echo "[!] No target files registered in Master bundle."
  exit 0
fi

CHANGED_COUNT=0

for FILE in $TARGET_FILES; do
  if [ ! -f "$FILE" ]; then
    echo " [SKIP] File not found: $FILE"
    continue
  fi

  # --------------------------------------------------------------------
  # Rule Engine & Transformer
  # 例: バージョン指定の同期やメタデータの補完ルールの適用
  # --------------------------------------------------------------------
  TRANSFORMED_TMP=$(mktemp)

  jq '
    # 共通更新ルール例: ZERO_COREマスターからの同期タグ挿入
    . + {
      "_rewrite_sync": {
        "engine": "JSSH-REWRITE-V1",
        "synced_at": (now | floor)
      }
    }
  ' "$FILE" > "$TRANSFORMED_TMP" 2>/dev/null || {
    rm -f "$TRANSFORMED_TMP"
    echo " [ERR] Failed to process JSON: $FILE"
    continue
  }

  # 変更差分の検知
  if ! cmp -s "$FILE" "$TRANSFORMED_TMP"; then
    CHANGED_COUNT=$((CHANGED_COUNT + 1))
    
    if [ "$MODE" = "--apply" ]; then
      # バックアップ取得の上書き実行 (Writer)
      REL_PATH=$(dirname "$FILE")
      mkdir -p "$BACKUP_DIR/$REL_PATH"
      cp "$FILE" "$BACKUP_DIR/$FILE"
      mv "$TRANSFORMED_TMP" "$FILE"
      echo " [REWRITTEN] $FILE"
    else
      rm -f "$TRANSFORMED_TMP"
      echo " [PLAN] File needs update -> $FILE"
    fi
  else
    rm -f "$TRANSFORMED_TMP"
    echo " [UNCHANGED] $FILE"
  fi
done

echo "--------------------------------------------------"
if [ "$MODE" = "--dry-run" ]; then
  echo " [*] Dry-run completed. Pending modifications: $CHANGED_COUNT file(s)."
  echo " [*] Run with '--apply' to execute rewriting safely."
else
  echo " [SUCCESS] Rewrite applied to $CHANGED_COUNT file(s)."
  echo " [BACKUP] Saved at: $BACKUP_DIR"
fi
echo "=================================================="
