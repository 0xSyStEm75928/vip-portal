#!/bin/sh

# 前回のコミットハッシュ記録ファイル
STATE_FILE=".last_sync_state"

# 各ブランチの最新コミットハッシュを取得
git fetch origin main business research > /dev/null 2>&1
CURRENT_STATE=$(git rev-parse origin/main origin/business origin/research 2>/dev/null | tr '\n' '-')

if [ ! -f "$STATE_FILE" ]; then
    echo "$CURRENT_STATE" > "$STATE_FILE"
    echo ">> [NOTIFICATION SYSTEM] 監視を開始しました。"
    exit 0
fi

LAST_STATE=$(cat "$STATE_FILE")

if [ "$CURRENT_STATE" != "$LAST_STATE" ]; then
    echo ""
    echo "===================================================="
    echo " 🚨 【新着通知】オンボーディング / 新規通信を検知しました！"
    echo "===================================================="
    
    # 誰がどんなコミットをしたか直近ログを表示
    echo "📥 最新のアクション (直近3件):"
    git log --all -n 3 --oneline --no-merges
    
    echo "===================================================="
    echo " 👉 'MY_ROLE=alpha ./node_sync.sh' で詳細を確認してください。"
    echo ""
    
    # 状態の更新
    echo "$CURRENT_STATE" > "$STATE_FILE"
else
    echo ">> [通知なし] 新しいオンボーディングやログはありません。"
fi
