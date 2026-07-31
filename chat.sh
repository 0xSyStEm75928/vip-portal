#!/bin/bash
CHAT_FILE="chat_history.log"

if [ ! -f "$CHAT_FILE" ]; then
    echo "=== PIRDAG CUI GOVERNANCE CHAT ===" > "$CHAT_FILE"
fi

case "$1" in
    send)
        if [ -z "$2" ]; then
            echo "Error: Message payload empty."
            echo "Usage: ./chat.sh send \"YOUR_MESSAGE\""
            exit 1
        fi
        
        # ハッシュからノードIDを取得（無ければAnon）
        NODE_KEY="Node-Anon"
        if [ -f "my_portable_hash.json" ]; then
             NODE_KEY=$(jq -r '.portable_hash' my_portable_hash.json 2>/dev/null | cut -c 1-10)
             NODE_KEY="Node-$NODE_KEY"
        fi
        
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
        echo "[$TIMESTAMP] <$NODE_KEY>: $2" >> "$CHAT_FILE"
        
        git add "$CHAT_FILE" my_portable_hash.json 2>/dev/null
        git commit -m "chat: message from $NODE_KEY"
        git push origin main
        echo ">> Payload Sent & Synchronized."
        ;;
        
    read|sync)
        git pull origin main --rebase > /dev/null 2>&1
        echo "----------------------------------------------------"
        cat "$CHAT_FILE"
        echo "----------------------------------------------------"
        ;;
        
    *)
        echo "=== TRIAGE COMMAND HELP ==="
        echo "  ./chat.sh send \"message\" : Push encrypted log"
        echo "  ./chat.sh read          : Sync & Read latest log"
        ;;
esac
