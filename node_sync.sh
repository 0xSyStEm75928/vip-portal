#!/bin/sh

# 閲覧権限の取得（未指定の場合はパブリック）
ROLE=${MY_ROLE:-"public"}

echo "===================================================="
echo " 🛡️ [PIRDAG HARDENED HYBRID DOMAIN ENGINE]"
echo "    認証アクセスレベル: [$ROLE]"
echo "===================================================="

# 最新ブランチ情報の取得
git fetch origin business research main > /dev/null 2>&1

case "$ROLE" in
    alpha|admin)
        echo ">> [ALPHA COMPLETE ACCESS] 全領域の暗号化状態を解除して取得中..."
        echo ""
        echo "💼 --- BUSINESS DOMAIN ---"
        git show origin/business:business/payload.json 2>/dev/null || echo " (データ未検出)"
        echo ""
        echo "🔬 --- RESEARCH DOMAIN ---"
        git show origin/research:research/payload.json 2>/dev/null || echo " (データ未検出)"
        ;;
        
    business)
        echo ">> [BUSINESS NODE] 商談ドメインのみ復号化..."
        echo ""
        echo "💼 --- BUSINESS DOMAIN ---"
        git show origin/business:business/payload.json 2>/dev/null || echo " (アクセス拒否またはデータなし)"
        ;;
        
    research)
        echo ">> [RESEARCH NODE] コア研究ドメインのみ復号化..."
        echo ""
        echo "🔬 --- RESEARCH DOMAIN ---"
        git show origin/research:research/payload.json 2>/dev/null || echo " (アクセス拒否またはデータなし)"
        ;;
        
    *)
        echo ">> [PUBLIC NODE] パブリック情報のみ表示..."
        echo " (保護されたドメインデータへのアクセス権がありません)"
        ;;
esac

echo "===================================================="
echo " >> セキュリティチェック完了。"
