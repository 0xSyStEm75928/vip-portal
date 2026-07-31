#!/bin/bash

# =================================================================
# PIRDAG ROBUST JSON RECOVERY ENGINE
# =================================================================

case "$1" in
    read|sync)
        echo ">> ネットワーク（Git）から最新データを取得中..."
        # エラー発生時も止まらないように安全にpull
        git pull origin main --rebase > /dev/null 2>&1 || git pull origin main > /dev/null 2>&1
        
        echo ""
        echo "===================================================="
        echo " 📥 [GOVERNANCE MESSAGES - 受信ログ]"
        echo "===================================================="
        
        COUNT=0
        
        # JSONファイル群から"message"または"payload"の行を直接抽出 (Python等に依存しないgrep/sed方式)
        for file in *.json; do
            if [ -f "$file" ]; then
                # JSON内の "message": "..." や "payload": "..." を直接抽出
                MATCHES=$(grep -E '"(message|payload|state_payload)"' "$file" 2>/dev/null | sed -E 's/.*"([^"]+)": *"([^"]+)".*/\1: \2/')
                if [ -n "$MATCHES" ]; then
                    echo " [$file]"
                    echo "   $MATCHES"
                    COUNT=$((COUNT + 1))
                fi
            fi
        done
        
        # 通常のログファイルがあればそれも表示
        if [ -f "encrypted_chat.log" ]; then
            echo ""
            echo " [encrypted_chat.log]"
            cat "encrypted_chat.log"
            COUNT=$((COUNT + 1))
        fi

        echo "===================================================="
        echo " >> 処理完了: 計 $COUNT 件のデータリソースを確認しました。"
        echo ""
        ;;

    *)
        echo "Usage: ./node_sync.sh read"
        ;;
esac
