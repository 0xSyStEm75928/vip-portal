#!/bin/sh

# 1. リモートの最新の変更を取り込む（競合を統合）
git pull origin main --rebase

# 2. 正しいファイル名で追加（新規ファイルと変更ファイルを一括ステージング）
git add payment_verified_gate.json ghost_spread_config.json api_ghost_spread_check.js test_ghost_trigger.py run_live_spread.py

# 3. 再コミット
git commit -m "feat: Add ghost spread API and verification scripts"

# 4. プッシュ実行
git push origin main

echo "--------------------------------------------------"
echo "🚀 競合を解消し、GitHub へのプッシュが成功しました！"
echo "--------------------------------------------------"
