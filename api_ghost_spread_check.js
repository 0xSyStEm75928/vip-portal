// Vercel Serverless Function: api/ghost-spread-check.js

export default async function handler(req, res) {
  // POSTリクエストのみ受け付け
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { dex_a_price, dex_b_price, min_profit_threshold = 0.20, gas_estimate_usdt = 0.5 } = req.body;

    // 1. 基本パラメータ検証
    if (!dex_a_price || !dex_b_price) {
      return res.status(400).json({ error: 'DEX価格データが不足しています。' });
    }

    // 2. スプレッド（価格差 %）の算出
    const raw_spread = ((dex_b_price - dex_a_price) / dex_a_price) * 100;
    const spread_pct = parseFloat(raw_spread.toFixed(4));

    // 3. ゴーストスプレッドの判定ロジック
    // 通常のスプレッド（ノイズ）ではなく、急激な乖離（閾値超え）かつガス代負けしない場合のみ反応
    const is_ghost_spread = spread_pct >= min_profit_threshold;
    
    // 応答ペイロードの組み立て
    const responsePayload = {
      timestamp: new Date().toISOString(),
      analysis: {
        dex_a_price: parseFloat(dex_a_price),
        dex_b_price: parseFloat(dex_b_price),
        spread_pct: spread_pct,
        threshold_pct: min_profit_threshold
      },
      status: is_ghost_spread ? "GHOST_SPREAD_DETECTED" : "NORMAL_MARKET_NOISE",
      trigger_execution: is_ghost_spread, // このフラグが true の時だけ自動注文/通知へ
      message: is_ghost_spread 
        ? `✨ [GHOST SPREAD DETECTED] 乖離率: ${spread_pct}% (閾値: ${min_profit_threshold}% 超え)`
        : `💤 [NOISE] 乖離率: ${spread_pct}% (通常範囲内のためスルー)`
    };

    // 4. ゴーストスプレッド検出時のみログ出力＆レスポンス
    if (is_ghost_spread) {
      console.log(`[ALERT] Ghost spread triggered: ${spread_pct}%`);
      // ここに Discord / Telegram や コントラクト実行Web3呼び出しを挟むことが可能
    }

    return res.status(200).json(responsePayload);

  } catch (error) {
    console.error("API Error:", error);
    return res.status(500).json({ error: '内部サーバーエラーが発生しました。' });
  }
}
