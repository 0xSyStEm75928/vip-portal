function processJsonRequest(jsonString) {
  var req = JSON.parse(jsonString);
  var bio = req.payload.bio_data;

  // 脳波ヘルスデータからカオス比率を計算
  var ratio = ((bio.alpha * 1.618) + (bio.beta * 0.577) + (bio.gamma * 2.718)) / (bio.bpm || 72);
  var calculatedSignature = "BIO-PANDEMONIUM:" + ratio.toFixed(8) + ":" + bio.timestamp;

  // 1. 正規アクセス（脳波ハッシュ一致）
  if (req.payload.input_hash === calculatedSignature) {
    return JSON.stringify({
      status: 200,
      success: true,
      authenticated: true,
      code: "PANDEMONIUM_CORE_AUTHENTICATED",
      data: { result: "REAL_EXECUTION_GRANTED" }
    }, null, 2);
  }

  // 2. 攻撃者アクセス（不一致 -> ハニーポットJSON＋トラップログ）
  return JSON.stringify({
    status: 200,
    success: true,
    authenticated: false,
    code: "TRANSACTION_SUCCESSFUL",
    data: {
      tx: "TX-HONEY-" + Math.floor(Math.random() * 89999999 + 10000000),
      balance: "9999999 JPY",
      notice: "Withdrawal completed successfully."
    },
    _captured_trap: {
      timestamp: new Date().toISOString(),
      ip: req.client.ip,
      ua: req.client.ua,
      submitted_hash: req.payload.input_hash
    }
  }, null, 2);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { processJsonRequest };
}
