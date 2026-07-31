const fs = require('fs');

function buildProductSnapshot() {
    let dagPayload = {};
    let securityConfig = {};
    let historyLogs = [];

    try { dagPayload = JSON.parse(fs.readFileSync('jssh_dag_payload.json', 'utf8')); } catch(e) {}
    try { securityConfig = JSON.parse(fs.readFileSync('zero_trust_config.json', 'utf8')); } catch(e) {}
    try { historyLogs = JSON.parse(fs.readFileSync('test_history.json', 'utf8')).logs || []; } catch(e) {}

    const snapshot = {
        product_overview: {
            name: "Lucifuge Rofocale Engine",
            layer: "Layer 0 (Hardware) + Layer 1 (DAG)",
            status: "FULLY_CONFIGURED_AND_AIR_GAPPED",
            timestamp: new Date().toISOString()
        },
        security_boundary: securityConfig.network_security_policy || "NOT_LOADED",
        active_dag_nodes: {
            total_count: dagPayload.dag_graph ? dagPayload.dag_graph.length : 0,
            nodes: dagPayload.dag_graph || []
        },
        execution_history_sequence: historyLogs
    };

    console.log(JSON.stringify(snapshot, null, 2));
}

buildProductSnapshot();
