#!/bin/sh

echo ">> ネットワーク（Git）から最新データを取得中..."
git pull origin main --rebase > /dev/null 2>&1 || git pull origin main > /dev/null 2>&1

echo ""
echo "===================================================="
echo " 📥 [GOVERNANCE MESSAGES - 自動トリアージ分類表示]"
echo "===================================================="

echo ""
echo "----------------------------------------------------"
echo " 💼 [BUSINESS & CLIENT] (ビジネス・案件メッセージ)"
echo "----------------------------------------------------"
grep -i -E '(business|client|order|vip|buy|contract)' *.json 2>/dev/null || echo " (該当なし)"

echo ""
echo "----------------------------------------------------"
echo " 🔬 [RESEARCH & CORE] (研究員・開発ノード)"
echo "----------------------------------------------------"
grep -i -E '(node|genesis|pirdag|protocol|dag|core|hash)' *.json 2>/dev/null || echo " (該当なし)"

echo ""
echo "----------------------------------------------------"
echo " 📄 [RAW ALL JSON FILES] (すべての受信ファイル一覧)"
echo "----------------------------------------------------"
for file in *.json; do
    if [ -f "$file" ]; then
        echo "--> $file"
    fi
done

echo ""
echo "===================================================="
echo " >> トリアージ整理完了。"
echo ""
