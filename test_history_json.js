const fs = require('fs');

// テスト用ヒストリーシミュレーションデータ
const mockHistory = [
    "git status",
    "cat phantom_state.json",
    "python3 deception_runner.py",
    "node JSON.js",
    "git push origin main"
];

function buildSequentialHistoryJson(historyList) {
    const timestamp = new Date().toISOString();
    
    // ヒストリー番号順にシリアルIDを刻む
    const logEntries = historyList.map((cmd, index) => {
        const historyId = String(index + 1).padStart(4, '0'); // 0001, 0002...
        return {
            seq_id: `HIST_${historyId}`,
            step: index + 1,
            command: cmd,
            timestamp: timestamp,
            status: "EXECUTED"
        };
    });

    const outputJson = {
        session_meta: {
            engine: "ZeroCore-DAG-History-Logger",
            total_entries: logEntries.length,
            generated_at: timestamp
        },
        logs: logEntries
    };

    return outputJson;
}

// テスト実行と書き出し
const result = buildSequentialHistoryJson(mockHistory);
fs.writeFileSync('test_history.json', JSON.stringify(result, null, 2));

console.log("==================================================");
console.log(" 🧪 History JSON Sequential Test Output");
console.log("==================================================");
console.log(JSON.stringify(result, null, 2));
console.log("--------------------------------------------------");
console.log("🎯 [TEST PASS] test_history.json successfully written.");
