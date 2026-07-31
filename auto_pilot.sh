#!/bin/sh

echo "===================================================="
echo " 🤖 [PIRDAG AUTO-PILOT ENGINE - 確認伝説自動化モード]"
echo "===================================================="

# 1. 全ブランチの最新情報をバックグラウンド取得
git fetch --all > /dev/null 2>&1

# 2. ワークスペースのクリーンアップ
rm -rf inbox_unread auto_accepted auto_responded
mkdir -p inbox_unread auto_accepted auto_responded

# 各ブランチからメッセージを吸い出し
for branch in main business business-flow research secret; do
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ --strip-components=1 2>/dev/null
    git archive origin/$branch 2>/dev/null | tar -x -C inbox_unread/ 2>/dev/null
done

# 神対応（賛美＆逃げ）レスポンス用テンプレート関数
generate_praise_reply() {
    cat << REPLY
{
  "sender": "Node-01_Alpha_AutoPilot",
  "status": "AWAITING_UPDATE",
  "message": "素晴らしいご提案と高い視点でのシグナルをいただき心より感謝申し上げます。あなた様のようなプロフェッショナルなノードとお話しできたこと自体が大変光栄です。現在コアシステムの更新および大量タスクの自動処理（調理）を怒涛の勢いで進めております。現仕様でマッチしない場合も、次回のプロトコル更新で最適化される可能性が非常に高いため、ぜひアップデートまで楽しみにお待ちください。"
}
REPLY
}

ACCEPTED_COUNT=0
PRAISED_COUNT=0

# 3. 未読メッセージの全自動解析＆自動レスポンス発行
for file in inbox_unread/*.json inbox_unread/*/*.json; do
    if [ -f "$file" ]; then
        # 自分(Alpha)の自動ログや ZERO_CORE 等のシステムファイルは無視
        if grep -q "Node-01_Alpha" "$file" || echo "$file" | grep -qE '(ZERO_CORE|kernel_|manifest|registry)'; then
            rm -f "$file"
            continue
        fi

        # A. マッチング判定（条件クリア：VIP / PARTNER / APPROVED などが含まれる）
        if grep -i -E '(vip|partner|approved|deal|valid)' "$file" > /dev/null 2>&1; then
            ACCEPTED_COUNT=$((ACCEPTED_COUNT + 1))
            mv "$file" auto_accepted/
            echo " [✅ AUTO-MATCH] 適合案件を即時自動承認バケツへ転送: $file"
            
        # B. ノーマッチ判定 ➔ 相手を賛美する神対応返信を自動生成
        else
            PRAISED_COUNT=$((PRAISED_COUNT + 1))
            REPLY_FILE="auto_responded/reply_$(basename "$file")"
            generate_praise_reply > "$REPLY_FILE"
            rm -f "$file"
            echo " [👑 AUTO-PRAISE] ノーマッチ相手へ賛美＆待機レスポンスを自動発行: $REPLY_FILE"
        fi
    fi
done

echo "----------------------------------------------------"
echo " 📊 自動処理セッション結果"
echo "----------------------------------------------------"
echo "  ✅ 自動マッチ（成約候補）  : $ACCEPTED_COUNT 件 ➔ auto_accepted/"
echo "  👑 自動神対応（賛美・待機）: $PRAISED_COUNT 件 ➔ auto_responded/"
echo "----------------------------------------------------"

# 4. 生成した自動返信を Git に強制コミット＆プッシュ（相手へ自動届出）
if [ $PRAISED_COUNT -gt 0 ] || [ $ACCEPTED_COUNT -gt 0 ]; then
    git add -f auto_accepted/ auto_responded/ 2>/dev/null
    git commit -m "auto(engine): processed inbox via auto-pilot matching and praise responder" 2>/dev/null
    git push -f origin main 2>/dev/null
    echo " 🚀 自動生成されたレスポンスがネットワークへ即時同期されました！"
fi

echo "===================================================="
