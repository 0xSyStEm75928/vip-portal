const fs = require('fs');
const readline = require('readline');

async function processStream(filePath) {
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    let index = 0;
    const results = [];

    console.log('[*] Node.js Stream Processor Starting...');

    for await (const line of rl) {
        if (!line.trim()) continue;
        try {
            const data = JSON.parse(line);
            index++;
            
            // 簡単なインデックス振り & 状態遷移テストの計算
            const processed = {
                stream_index: index,
                raw_id: data.id,
                step_name: data.step,
                is_slow: data.delay_ms > 100,
                calculated_at: new Date().toISOString()
            };

            results.push(processed);
            console.log(`[Line ${index}] Processed ID: ${data.id} -> Status: ${data.status}`);
        } catch (err) {
            console.error(`[Line ${index}] JSON Parse Error:`, err.message);
        }
    }

    console.log('\n[+] Final Stream Results Array:');
    console.log(JSON.stringify(results, null, 2));
}

// input_stream.jsonl があれば実行
if (fs.existsSync('input_stream.jsonl')) {
    processStream('input_stream.jsonl');
} else {
    console.log('[!] Run test_stream.sh first to generate input_stream.jsonl');
}
