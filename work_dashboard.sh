#!/bin/sh

echo "===================================================="
echo " 💼 [PIRDAG WORK DASHBOARD - 本命仕事136件サマリー]"
echo "===================================================="

if [ ! -d "auto_accepted" ]; then
    echo " ⚠️ auto_accepted フォルダが見つかりません。"
    exit 1
fi

TOTAL=$(ls -1 auto_accepted/*.json auto_accepted/*/*.json 2>/dev/null | wc -l | tr -d ' ')

echo " 📂 対象案件数: $TOTAL 件"
echo "----------------------------------------------------"

COUNT=0
for file in auto_accepted/*.json auto_accepted/*/*.json; do
    if [ -f "$file" ]; then
        COUNT=$((COUNT + 1))
        # 画面が埋まりすぎないよう、ファイル名・送信者・トピック・概要だけをサクッと表示
        SENDER=$(grep -i '"sender"' "$file" 2>/dev/null | head -n 1 | cut -d'"' -f4)
        TOPIC=$(grep -i '"topic"' "$file" 2>/dev/null | head -n 1 | cut -d'"' -f4)
        MSG=$(grep -i '"message"' "$file" 2>/dev/null | head -n 1 | cut -d'"' -f4)

        echo "[$COUNT/$TOTAL] 📄 $(basename "$file")"
        [ -n "$SENDER" ] && echo "   👤 差出人 : $SENDER"
        [ -n "$TOPIC" ]  && echo "   📌 題目   : $TOPIC"
        [ -n "$MSG" ]    && echo "   💬 要約   : $MSG"
        echo "----------------------------------------------------"

        # 20件ごとに一時停止して読みやすくする（Enterで次へ）
        if [ $((COUNT % 20)) -eq 0 ]; then
            echo " [⏸️ 20件表示しました。Enterキーを押すと次の20件を表示します...]"
            read -r dummy
        fi
    fi
done

echo "===================================================="
echo " 🎉 すべての案件サマリーの確認が完了しました。"
echo "===================================================="
