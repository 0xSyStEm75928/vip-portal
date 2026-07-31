#!/bin/sh

# 1. .gitignore を無視して必要なファイルを強制追加＆コミット
git add -f ghost_spread_config.json payment_verified_gate.json api_ghost_spread_check.js test_ghost_trigger.py run_live_spread.py
git commit -m "feat: Add ghost spread API and configs (forced)"

# 2. 未コミットの残り（一時ファイル等）を一旦スタッシュに退避
git stash

# 3. リモートの最新情報を取得してローカル履歴と統合
git pull origin main --rebase

# 4. 退避したファイルを復元（必要に応じて）
git stash pop

# 5. GitHubへプッシュ
git push origin main

echo "--------------------------------------------------"
echo "✅ GitHub へのプッシュが完了しました！"
echo "--------------------------------------------------"
