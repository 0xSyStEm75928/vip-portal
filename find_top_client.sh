#!/bin/sh

echo "===================================================="
echo " 🎯 [SINGLE TARGET PICKER - 本命1件絞り込み]"
echo "===================================================="

# 63件の中から、決済・入金・本命に関わる重要ファイルを1件だけ抽出
TARGET_FILE=$(ls -1 auto_accepted/*payment*.json auto_accepted/*bounty*.json auto_accepted/*customer*.json 2>/dev/null | head -n 1)

if [ -z "$TARGET_FILE" ]; then
    TARGET_FILE=$(ls -1 auto_accepted/*.json 2>/dev/null | head -n 1)
fi

echo " 👤 【ターゲット確定】: $(basename "$TARGET_FILE")"
echo "----------------------------------------------------"
echo " 📄 ファイル内容（確認用）:"
cat "$TARGET_FILE"
echo "----------------------------------------------------"
echo "===================================================="
