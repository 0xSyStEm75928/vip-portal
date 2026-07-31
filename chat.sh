#!/bin/bash

CHAT_FILE="chat_history.log"

# チャットログが存在しない場合は初期化
if [ ! -f "$CHAT_FILE" ]; then
    echo "=== PIRDAG CUI CHAT CHANNEL ===" > "$CHAT_FILE"
fi

case "$1" in
    send)
        if [ -z "$2" ]; then
            echo "Usage: ./chat.sh send \"Your message here\""
            exit 1
        fi
        # 持ち運びハッシュまたは環境変数から送信者を識別（デフォルトはNode-Anonymous）
        SENDER=${NODE_ID:-"Node-01_Alpha"}
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
        
        # ログに書き込み
        echo "[$TIMESTAMP] <$SENDER>: $2" >> "$CHAT_FILE"
        
        # Gitへ自動同期
        git add "$CHAT_FILE"
        git commit -m "chat: message from $SENDER"
        git push origin main
        echo ">> メッセージを送信・同期しました。"
        ;;
        
    read|sync)
        # 最新ログを引き込んで表示
        git pull origin main --rebase > /dev/null 2>&1
        echo "----------------------------------------"
        cat "$CHAT_FILE"
        echo "----------------------------------------"
        ;;
        
    *)
        echo "=== CUI CHAT COMMANDS ==="
        echo "  ./chat.sh send \"メッセージ\"  : メッセージを送信して全体同期"
        echo "  ./chat.sh read              : 最新のチャットログを取得して表示"
        ;;
esac
