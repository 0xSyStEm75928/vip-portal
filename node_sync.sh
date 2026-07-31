#!/bin/bash

# =================================================================
# PIRDAG JSON-TREE MESSAGE RECOVERY ENGINE
# =================================================================

case "$1" in
    read|sync)
        echo ">> ネットワーク（Git）から最新のJSONツリーを引き込み中..."
        git pull origin main --rebase > /dev/null 2>&1
        
        echo ""
        echo "===================================================="
        echo " 📥 [JSON GOVERNANCE NODE MESSAGES - 全受信ログ]"
        echo "===================================================="
        
        COUNT=0
        
        # 1. JSONファイル群（GENESIS, PIRDAG, ポータブルハッシュ等）からメッセージを抽出
        for file in *.json; do
            if [ -f "$file" ]; then
                # jqコマンド等を使ってJSON内のmessageやpayload項目を自動で探索
                # (Pythonワンライナーで環境問わず確実にパース)
                MSG=$(python3 -c "
import json, sys
try:
    with open('$file') as f:
        data = json.load(f)
        # JSON内のメッセージになり得るキーを探索
        msg = data.get('message') or data.get('state_payload', {}).get('message') or data.get('payload')
        node = data.get('node_id') or data.get('portable_identity') or '$file'
        if msg:
            print(f'[{node}] ({file}): {msg}')
except Exception:
    pass
" 2>/dev/null)
                
                if [ -n "$MSG" ]; then
                    echo " $MSG"
                    COUNT=$((COUNT + 1))
                fi
            fi
        done
        
        # 2. 既存のログファイルが存在する場合も統合表示
        if [ -f "encrypted_chat.log" ]; then
            while IFS= read -r line; do
                if [ -n "$line" ]; then
                     echo " [LOG]: $line"
                     COUNT=$((COUNT + 1))
                fi
            done < "encrypted_chat.log"
        fi

        echo "===================================================="
        echo " >> 整合性確認完了: 計 $COUNT 件のメッセージ（JSON要素）を受信しました。"
        echo ""
        ;;

    *)
        echo "Usage: ./node_sync.sh read"
        ;;
esac
