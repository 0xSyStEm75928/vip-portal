#!/bin/sh

echo "===================================================="
echo " 🧹 [PIRDAG DATA JUICER - ノーマッチ自動隔離＆トリアージ]"
echo "===================================================="

# リモート最新化
git fetch --all > /dev/null 2>&1

# フォルダのリセット
rm -rf inbox_unread no_match
mkdir -p inbox_unread no_match

# 全ブランチからデータをインポート
for branch in main business business-flow research secret; do
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ --strip-components=1 2>/dev/null
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ 2>/dev/null
done

echo ""
echo "🔍 データをスキャンし、ノーマッチ／不適合ログを別フォルダ (no_match/) へ移動中..."

NOMATCH_COUNT=0
UNREAD_COUNT=0

# 全JSONファイルをチェックして仕分け
for file in inbox_unread/*.json inbox_unread/*/*.json; do
    if [ -f "$file" ]; then
        # 1. 自分(Alpha)の自動ログは完全に無視して除外
        if grep -q "Node-01_Alpha" "$file"; then
            rm -f "$file"
            continue
        fi

        # 2. 「合わない」「ノーマッチ」「NG」「mismatch」等のキーワードがあれば no_match/ へ移動
        if grep -i -E '(nomatch|mismatch|合わない|不適合|ng|cancel|reject)' "$file" > /dev/null 2>&1; then
            NOMATCH_COUNT=$((NOMATCH_COUNT + 1))
            mv "$file" no_match/
        else
            UNREAD_COUNT=$((UNREAD_COUNT + 1))
        fi
    fi
done

echo ""
echo "----------------------------------------------------"
echo " 📥 仕分け結果報告"
echo "----------------------------------------------------"
echo " 🚫 【ノーマッチ・隔離フォルダ (no_match/ )】 : $NOMATCH_COUNT 件"
echo " 📄 【純粋な未読・本命メッセージ (inbox_unread/)】: $UNREAD_COUNT 件"
echo "----------------------------------------------------"

if [ $NOMATCH_COUNT -gt 0 ]; then
    echo ""
    echo "💡 [no_match/ フォルダ内のメッセージ概要]"
    for f in no_match/*.json; do
        [ -f "$f" ] && echo " ➔ $f"
    done
    echo " 👉 隔離した相手には、賛美メッセージを返して『更新をお待ちください』と伝えて逃げましょう！"
fi

echo "===================================================="
