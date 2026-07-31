#!/bin/bash

# =================================================================
# PIRDAG PERFECT CUI ENGINE (PULL-BASED)
# =================================================================

SECRET_KEY="PIRDAG_GOVERNANCE_SECRET_KEY_ALPHA_30"
CHAT_FILE="encrypted_chat.log"

if [ ! -f "$CHAT_FILE" ]; then
    touch "$CHAT_FILE"
fi

case "$1" in
    send)
        if [ -z "$2" ]; then
            echo "Error: Message payload empty."
            echo "Usage: ./chat_secure.sh send \"YOUR_MESSAGE\""
            exit 1
        fi
        
        # ノードIDの取得
        NODE_KEY="Node-Anon"
        if [ -f "my_portable_hash.json" ]; then
             NODE_KEY=$(jq -r '.portable_hash' my_portable_hash.json 2>/dev/null | cut -c 1-10)
             NODE_KEY="Node-$NODE_KEY"
        fi
        
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
        RAW_PAYLOAD="[$TIMESTAMP] <$NODE_KEY>: $2"
        
        # 暗号化してログ追加
        ENCRYPTED_LINE=$(echo "$RAW_PAYLOAD" | openssl enc -aes-256-cbc -a -salt -pbkdf2 -pass pass:"$SECRET_KEY" 2>/dev/null)
        echo "$ENCRYPTED_LINE" >> "$CHAT_FILE"
        
        # Gitへ同期
        git add "$CHAT_FILE" > /dev/null 2>&1
        git commit -m "sec(chat): payload from $NODE_KEY" > /dev/null 2>&1
        git push origin main > /dev/null 2>&1
        echo ">> [SUCCESS] メッセージを暗号化して同期しました。"
        ;;
        
    read|sync)
        echo ">> ネットワークから最新ログを引き込んでいます..."
        git pull origin main --rebase > /dev/null 2>&1
        
        echo ""
        echo "===================================================="
        echo " 📥 [CUI GOVERNANCE CHAT LOGS - 全メッセージ一括表示]"
        echo "===================================================="
        
        # 全ログを一気に復号してまとめて表示
        COUNT=0
        while IFS= read -r line; do
            if [ -n "$line" ]; then
                DECRYPTED=$(echo "$line" | openssl enc -d -aes-256-cbc -a -pbkdf2 -pass pass:"$SECRET_KEY" 2>/dev/null)
                if [ $? -eq 0 ]; then
                    echo " $DECRYPTED"
                    COUNT=$((COUNT + 1))
                fi
            fi
        done < "$CHAT_FILE"
        
        echo "===================================================="
        echo " >> 合計 $COUNT 件のメッセージを取得しました。"
        echo ""
        ;;

    *)
        echo "=== CUI GOVERNANCE COMMANDS ==="
        echo "  ./chat_secure.sh send \"メッセージ\"  : 送信＆自動同期"
        echo "  ./chat_secure.sh read              : 叩いて最新全メッセージを一括閲覧"
        ;;
esac
