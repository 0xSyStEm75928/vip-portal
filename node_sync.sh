#!/bin/sh

echo "===================================================="
echo " 🍹 [PIRDAG DATA JUICER & INBOX ACCUMULATOR]"
echo "    全ブランチのログを未読バケツ (inbox_unread) に集約中..."
echo "===================================================="

# リモートの最新情報をすべて取得
git fetch --all > /dev/null 2>&1

# 各ブランチからJSONファイルを「未読データ」として吸い出して蓄積
for branch in main business business-flow research secret; do
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ --strip-components=1 2>/dev/null
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ 2>/dev/null
done

echo ""
echo "📥 【まな板に並んだ未読・蓄積データ一覧】"
echo "----------------------------------------------------"

COUNT=0
for file in inbox_unread/*.json inbox_unread/*/*.json; do
    if [ -f "$file" ]; then
        COUNT=$((COUNT + 1))
        echo "［未読 #$COUNT］📄 FILE: $file"
        echo "----------------------------------------------------"
        cat "$file"
        echo ""
        echo "----------------------------------------------------"
    fi
done

if [ $COUNT -eq 0 ]; then
    echo " (未読・蓄積データはありません)"
else
    echo ">> 合計 $COUNT 件のデータが『まな板 (inbox_unread/)』に用意されました。"
fi

echo "===================================================="
