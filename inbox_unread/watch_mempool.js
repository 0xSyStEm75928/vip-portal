const { ethers } = require("ethers");

// 監視対象のアドレスと条件設定
const PAYOUT_ADDRESS = "0xF7A353FAF6E6BD4732b0f234C656dBFDE53B0e91".toLowerCase();
const REQUIRED_AMOUNT_USDT = 35000;
const RPC_WS_URL = process.env.RPC_WS_URL || "wss://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY";

// WebSocketプロバイダーの設定
const provider = new ethers.providers.WebSocketProvider(RPC_WS_URL);

console.log("👀 [監視開始] Gitコミットなしで入金手前（Mempool）の兆候をフックします...");

// Mempool（未承認トランザクション）のリアルタイムフック
provider.on("pending", async (txHash) => {
  try {
    const tx = await provider.getTransaction(txHash);
    
    // 送信先が受取アドレスと一致するか確認
    if (tx && tx.to && tx.to.toLowerCase() === PAYOUT_ADDRESS) {
      
      // ★ 察知サイン（Git履歴には残さず、コンソールと一時フラグのみ更新）
      console.log("\n⚡ [入金察知サイン！] 相手が送金処理を開始しました！");
      console.log(`- Tx Hash : ${txHash}`);
      console.log(`- Status  : PENDING_IN_MEMPOOL (入金手前)`);
      console.log(`- 12確認のカウントを開始します...\n`);

      // 必要に応じて通知処理やローカルのステータス更新をここに挿入
    }
  } catch (err) {
    // pending処理のスキップ用エラーハンドリング
  }
});
