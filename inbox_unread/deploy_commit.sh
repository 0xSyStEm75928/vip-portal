#!/bin/sh

# 1. 現在の変更状態を確認
git status

# 2. 作成したAPIファイルや設定ファイルをステージングに追加
git add api/ ghost_spread_config.json payment_verified_gate.json

# 3. コミットメッセージを作成してコミット
git commit -m "feat: Add ghost spread API endpoint and verified token config"

# 4. メインブランチへプッシュ
git push origin main

echo "--------------------------------------------------"
echo "✅ コミット＆プッシュ完了！Vercelの自動デプロイを確認してください。"
echo "--------------------------------------------------"
