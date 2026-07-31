#!/bin/bash

# =================================================================
# PIRDAG SECURE CUI ENGINE (AES-256 ENCRYPTED)
# =================================================================

# 共有の秘密鍵（ノード間で共有するパスワード）
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
        
        # 自身のノードID取得
        NODE_KEY="Node-Anon"
        if [ -f "my_portable_hash.json" ]; then
             NODE_KEY=$(jq -r '.portable_hash' my_portable_hash.json 2>/dev/null | cut -c 1-10)
             NODE_KEY="Node-$NODE_KEY"
        fi
        
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
        RAW_PAYLOAD="[$TIMESTAMP] <$NODE_KEY>: $2"
        
        # OpenSSLでAES-256暗号化してBase64化した1行を出力
        ENCRYPTED_LINE=$(echo "$RAW_PAYLOAD" | openssl enc -aes-256-cbc -a -salt -pbkdf2 -pass pass:"$SECRET_KEY" 2>/dev/null)
        
        echo "$ENCRYPTED_LINE" >> "$CHAT_FILE"
        
        # Gitへコミット＆プッシュ（暗号文のみが流れる）
        git add "$CHAT_FILE"
        git commit -m "sec(chat): encrypted payload from $NODE_KEY"
        git push origin main
        echo ">> Encrypted Payload Sent & Synchronized."
        ;;
        
    read|sync)
        echo ">> Fetching latest network logs..."
        git pull origin main --rebase > /dev/null 2>&1
        echo "===================================================="
        echo " [DECRYPTED GOVERNANCE LOGS]"
        echo "===================================================="
        
        # 暗号化されたログを1行ずつ復号して画面に表示
        while IFS= read -r line; do
            if [ -n "$line" ]; then
                DECRYPTED=$(echo "$line" | openssl enc -d -aes-256-cbc -a -pbkdf2 -pass pass:"$SECRET_KEY" 2>/dev/null)
                if [ $? -eq 0 ]; then
                    echo "$DECRYPTED"
                else
                    echo "[DECRYPTION FAILED / INVALID KEY]"
                fi
            fi
        done < "$CHAT_FILE"
        echo "===================================================="
        ;;
        
    set-p2p)
        # GitHub以外のバックアップリモート（自前サーバーなど）を追加するコマンド
        if [ -z "$2" ]; then
            echo "Usage: ./chat_secure.sh set-p2p \"git@your-private-server.com:repo.git\""
            exit 1
        fi
        git remote add backup "$2"
        echo ">> Backup remote added: $2"
        echo ">> Now you can push to backup via 'git push backup main'"
        ;;

    *)
        echo "=== SECURE CUI COMMANDS ==="
        echo "  ./chat_secure.sh send \"message\" : Encrypt and push message"
        echo "  ./chat_secure.sh read          : Sync and decrypt messages"
        echo "  ./chat_secure.sh set-p2p <URL>  : Add backup non-GitHub remote"
        ;;
esac
