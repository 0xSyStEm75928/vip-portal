#!/bin/sh

echo "===================================================="
echo " 🧹 [PIRDAG CLEAN JUICER - 外部メッセージ専用]"
echo "    自分(Alpha)の送信ログを除外して抽出中..."
echo "===================================================="

# 全ブランチの最新を取得
git fetch --all > /dev/null 2>&1

# 未読フォルダを綺麗にリセット
rm -rf inbox_unread
mkdir -p inbox_unread

# 各ブランチからデータ抽出
for branch in main business business-flow research secret; do
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ --strip-components=1 2>/dev/null
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ 2>/dev/null
done

echo ""
echo "📥 【外部ノードからの純粋な受信メッセージ一覧】"
echo "----------------------------------------------------"

COUNT=0
# JSONファイルの中から、自分(Node-01_Alpha)以外のファイルだけを表示
for file in inbox_unread/*.json inbox_unread/*/*.json; do
    if [ -f "$file" ]; then
        # 自分(Alpha)の発言が含まれていないファイルだけをカウント・表示
        if ! grep -q "Node-01_Alpha" "$file"; then
            COUNT=$((COUNT + 1))
            echo "［受信 #$COUNT］📄 FILE: $file"
            echo "----------------------------------------------------"
            cat "$file"
            echo ""
            echo "----------------------------------------------------"
        fi
    fi
done

if [ $COUNT -eq 0 ]; then
    echo " 🍃 (外部からの新しい未読メッセージはありません。安心してください！)"
else
    echo ">> 合計 $COUNT 件の外部メッセージだけに絞り込みました。"
fi

echo "===================================================="
