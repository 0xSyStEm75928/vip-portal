const fs = require('fs');

function dispatchPacket() {
    console.log("==================================================");
    printHeader = () => console.log(" 📡 ZeroCore JSON Packet Dispatcher (Node.js)");
    printHeader();
    console.log("==================================================");

    try {
        // 1. 先ほど作った欺瞞JSON（パケット）の読み込み
        const rawData = fs.readFileSync('phantom_state.json', 'utf8');
        const payload = JSON.parse(rawData);

        console.log(`[*] Target Payload Loaded: ${payload.session_id}`);
        console.log(`[*] Sending Fake Status  : ${payload.perceived_status}`);
        console.log(`[*] Wallet Balance Payload: ${payload.fake_data.system_wallet_balance}`);
        console.log("--------------------------------------------------");

        // 2. パケット構造（JSON文字列）の整形と送出シミュレーション
        const packetData = JSON.stringify({
            event: "PHANTOM_STATE_DISPATCH",
            timestamp: new Date().toISOString(),
            payload: payload
        }, null, 2);

        console.log("🚨 [DISPATCHING PACKET OVER CUI...]");
        console.log(packetData);
        console.log("--------------------------------------------------");
        console.log("🎯 RESULT: JSON Packet dispatched successfully to CUI stream.");

    } catch (err) {
        console.error("❌ Error loading phantom_state.json:", err.message);
    }
}

dispatchPacket();
