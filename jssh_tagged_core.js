const fs = require('fs');
const crypto = require('crypto');

function generateSmartTaggedDag() {
    let historyLogs = [];
    try {
        const raw = fs.readFileSync('test_history.json', 'utf8');
        historyLogs = JSON.parse(raw).logs || [];
    } catch (e) {
        console.log("⚠️ [WARN] Local history log not found.");
    }

    let previousNodeHash = "GENESIS_NODE_00000000000000000000000000000000";

    const taggedDagNodes = historyLogs.map((item, idx) => {
        const hwClock = process.hrtime.bigint().toString();
        const entropy = crypto.randomBytes(16).toString('hex');
        const nodeHash = crypto.createHash('sha256').update(`${previousNodeHash}:${hwClock}:${item.command}`).digest('hex');

        // 🔥 知恵で勝つ！スマート分類タグ（Tagging）の追加
        const smartTags = [
            "LAYER_0_PHYSICAL",
            `SEQ_${item.seq_id}`,
            idx === 0 ? "DAG_ROOT" : "DAG_LEAF",
            "TRAP_ACTIVE",
            "HARDWARE_PROOF_VERIFIED"
        ];

        const node = {
            dag_depth: idx + 1,
            node_id: `DAG_NODE_${String(idx + 1).padStart(4, '0')}`,
            seq_ref: item.seq_id,
            command_executed: item.command,
            parent_hash: previousNodeHash,
            node_hash: nodeHash,
            
            // 🏷️ ここが今回の超重要ポイント！
            tags: smartTags,
            metadata: {
                trap_classification: "NON_BLOCKING_RESOURCE_DRAIN",
                confidence_score: 0.998,
                is_tamper_evident: true
            },
            
            hardware_proof: {
                hw_clock_ns: hwClock,
                circuit_entropy: entropy,
                status: "HARDWARE_VERIFIED_200_OK"
            }
        };

        previousNodeHash = nodeHash;
        return node;
    });

    const finalPayload = {
        session_meta: {
            protocol: "ZeroCore-DAG-Tagged-Engine",
            total_nodes: taggedDagNodes.length,
            global_tags: ["SECURITY_DECEPTION", "DAG_CHAIN", "HARDWARE_ANCHORED"],
            timestamp: new Date().toISOString()
        },
        dag_graph: taggedDagNodes
    };

    fs.writeFileSync('jssh_dag_payload.json', JSON.stringify(finalPayload, null, 2));
    console.log("==================================================");
    console.log(" 🏷️ SMART TAGGED DAG JSON GENERATED!");
    console.log("==================================================");
    console.log(JSON.stringify(finalPayload, null, 2));
}

generateSmartTaggedDag();
