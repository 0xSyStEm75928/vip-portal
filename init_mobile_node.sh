#!/bin/sh

echo "===================================================="
echo " 📱 [PIRDAG MOBILE CUI NODE - DEFAULT SYSTEM INIT]"
echo "===================================================="

# 1. 匿名ローカル設定の適用
git config --local user.name "Node-Mobile-Alpha"
git config --local user.email "node-mobile@users.noreply.github.com"
echo "[✓] Mobile Anonymous Profile: ENFORCED"

# 2. スマホ専用ポータブルハッシュ（ID）の生成
if [ ! -f "my_portable_hash.json" ]; then
    MOBILE_HASH=$(echo "Mobile_$(date +%s)_$RANDOM" | sha256sum 2>/dev/null | awk '{print $1}')
    [ -z "$MOBILE_HASH" ] && MOBILE_HASH=$(echo "Mobile_$(date +%s)" | md5sum | awk '{print $1}')
    echo "{\"portable_hash\": \"0x$MOBILE_HASH\", \"device\": \"MOBILE_CUI_NODE\", \"role\": \"ALPHA_MASTER\"}" > my_portable_hash.json
    echo "[✓] Personal Mobile Hash: 0x$MOBILE_HASH"
fi

# 3. リモートとの同期とブランチ強制接続 (-f)
git checkout main 2>/dev/null || git checkout -b main
git add -f my_portable_hash.json node_sync.sh notify.sh 2>/dev/null
git commit -m "feat(mobile): initialize mobile CUI terminal node" 2>/dev/null
git push -f origin main 2>/dev/null

echo "===================================================="
echo " 🚀 デフォルト作品（スマホCUI環境）の構築が完了しました！"
echo "===================================================="
echo " 【操作コマンド一覧】"
echo "  ■ 全知全能同期（Alpha） : MY_ROLE=alpha ./node_sync.sh"
echo "  ■ オンボーディング新着通知: ./notify.sh"
echo "  ■ 商談用チャネル確認     : MY_ROLE=business ./node_sync.sh"
echo "  ■ 研究用チャネル確認     : MY_ROLE=research ./node_sync.sh"
echo "===================================================="
