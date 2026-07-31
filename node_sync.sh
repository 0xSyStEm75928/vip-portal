#!/bin/sh

# 1. まず全体のメイン世界に戻す
git checkout main > /dev/null 2>&1

echo ">> 全ブランチ（main / business / research）の最新同期中..."
git fetch origin > /dev/null 2>&1

ROLE=${MY_ROLE:-"public"}

echo ""
echo "===================================================="
echo " 📥 [ALL DOMAIN MESSAGES - 全領域データ確認画面]"
echo "    現在の閲覧権限 (MY_ROLE): [$ROLE]"
echo "===================================================="

# --- MAIN / PUBLIC 領域 ---
echo ""
echo "🌐 [MAIN / PUBLIC CHANNEL]"
echo "----------------------------------------------------"
git show origin/main:my_portable_hash.json 2>/dev/null || true
for f in *.json; do [ -f "$f" ] && echo "📄 $f:" && cat "$f"; done

# --- BUSINESS 領域 ---
if [ "$ROLE" = "business" ] || [ "$ROLE" = "admin" ] || [ "$ROLE" = "alpha" ]; then
    echo ""
    echo "💼 [BUSINESS CHANNEL - 顧客・商談履歴]"
    echo "----------------------------------------------------"
    git archive origin/business | tar -x -C . business/ 2>/dev/null || true
    for f in business/*.json; do [ -f "$f" ] && echo "📄 $f:" && cat "$f"; done
fi

# --- RESEARCH 領域 ---
if [ "$ROLE" = "research" ] || [ "$ROLE" = "admin" ] || [ "$ROLE" = "alpha" ]; then
    echo ""
    echo "🔬 [RESEARCH CHANNEL - 研究員データ]"
    echo "----------------------------------------------------"
    git archive origin/research | tar -x -C . research/ 2>/dev/null || true
    for f in research/*.json; do [ -f "$f" ] && echo "📄 $f:" && cat "$f"; done
fi

echo ""
echo "===================================================="
echo " >> 復元・全受信完了。"
echo ""
