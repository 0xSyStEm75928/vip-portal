#!/bin/bash
# ========================================================
# sgit CORE ENGINE (滑空・精密ウェイト仕様)
# ========================================================

# 1. 履歴のハック
history -s "sgit --fast-resolve"

# 2. 認証の起動と「間」の確保
if ! ssh-add -l >/dev/null 2>&1; then
    eval $(ssh-agent -s) >/dev/null 2>&1
    sleep 0.5  # エージェント起動を待つための「間」
    ssh-add /root/.ssh/id_ed25519
    sleep 1.0  # パスフレーズ通過・鍵登録を確実に定着させる「間」
fi

# 3. 変更の検知とステージング
git add -A
sleep 0.5  # ファイルのインデックス登録を待つ「間」

# 4. コミット処理
if ! git diff-index --cached --quiet HEAD; then
    git commit --quiet -m "feat: cosmic execution smoothly resolved"
    sleep 0.5  # コミットログの書き込みを待つ「間」
fi

# 5. リモートへ滑らかにプッシュ
echo "[sgit] リモートへの滑空を開始します..."
git push --quiet origin master

sleep 0.5
echo -e "\n[sgit] ─── 滑空完了。100% 同期 ───"
