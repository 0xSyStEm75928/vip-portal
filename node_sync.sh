#!/bin/sh

# 自分の役割設定（指定がない場合は public）
ROLE=${MY_ROLE:-"public"}

echo "===================================================="
echo " 🌐 [PIRDAG HYBRID DOMAIN SYNC Engine]"
echo "    現在のアクセス権限 (MY_ROLE): [$ROLE]"
echo "===================================================="

case "$ROLE" in
    alpha|admin)
        echo ">> [管理者アクセス] 全ブランチ（Public/Business/Research）の最新データを同期中..."
        git pull origin main --rebase > /dev/null 2>&1
        git fetch origin business research > /dev/null 2>&1
        echo ""
        echo "💼 --- BUSINESS DATA ---"
        git show origin/business:business_data/config.json 2>/dev/null || echo " (データなし)"
        echo ""
        echo "🔬 --- RESEARCH DATA ---"
        git show origin/research:research_data/config.json 2>/dev/null || echo " (データなし)"
        ;;
        
    business)
        echo ">> [ビジネスノード] 商談領域のみ同期中..."
        git fetch origin business > /dev/null 2>&1
        git show origin/business:business_data/config.json 2>/dev/null || echo " (権限エラーまたはデータなし)"
        ;;
        
    research)
        echo ">> [研究ノード] コア研究領域のみ同期中..."
        git fetch origin research > /dev/null 2>&1
        git show origin/research:research_data/config.json 2>/dev/null || echo " (権限エラーまたはデータなし)"
        ;;
        
    *)
        echo ">> [パブリックノード] 全体公開データのみ同期中..."
        git pull origin main --rebase > /dev/null 2>&1
        echo " (公開チャンネルのみ表示中)"
        ;;
esac

echo "===================================================="
echo " >> 処理が完了しました。"
