#!/bin/sh

echo "===================================================="
echo " 🧹 [AUTOMATED INBOX TRIAGE - 次世代自動化フェーズ]"
echo "    内部システムログを分離し、純粋なメッセージを整列中..."
echo "===================================================="

# 全ブランチの最新を取得
git fetch --all > /dev/null 2>&1

# フォルダのリセット
rm -rf inbox_unread system_archive
mkdir -p inbox_unread system_archive

# 全ブランチからデータをインポート
for branch in main business business-flow research secret; do
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ --strip-components=1 2>/dev/null
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ 2>/dev/null
done

MSG_COUNT=0
SYS_COUNT=0

# 全ファイルをチェックしてシステムログと純粋メッセージを完全分離
for file in inbox_unread/*.json inbox_unread/*/*.json; do
    if [ -f "$file" ]; then
        # 自分(Alpha)の自動ログや ZERO_CORE 等のシステム設定ファイルはアーカイブへ退避
        if grep -q "Node-01_Alpha" "$file" || echo "$file" | grep -qE '(ZERO_CORE|kernel_|manifest|registry)'; then
            SYS_COUNT=$((SYS_COUNT + 1))
            mv "$file" system_archive/ 2>/dev/null
        else
            MSG_COUNT=$((MSG_COUNT + 1))
        fi
    fi
done

echo "----------------------------------------------------"
echo " ⚙️ 内部システムログ (裏側退避) : $SYS_COUNT 件"
echo " 📥 純粋な相手からのメッセージ (まな板) : $MSG_COUNT 件"
echo "----------------------------------------------------"

if [ $MSG_COUNT -eq 0 ]; then
    echo " 🍃 現在、人間からの直接的な未読メッセージはありません。"
else
    echo " 📄 【まな板の上にあるメッセージ一覧】"
    for f in inbox_unread/*.json; do
        [ -f "$f" ] && echo " ➔ $f"
    done
fi

echo "===================================================="
