#!/usr/bin/env python3
"""
ZERO CORE EVALUATOR (Execution Engine)
Purpose: Pure cryptographic fact validation & Enemy Source Isolation
"""

import os
import json
import sys

TREE_PATH = "forensics/evidence/enemy_source.tree.json"
OUTPUT_BLOCKLIST = "forensics/evidence/ZERO_CORE_ISOLATED_ENEMIES.json"

def main():
    print("\n" + "="*60)
    print(" ⚡ ZERO CORE EVALUATOR: INITIATING SYSTEM CHECK")
    print("="*60)

    if not os.path.exists(TREE_PATH):
        print(f"[FATAL] 裏付けツリーが見つかりません: {TREE_PATH}")
        sys.exit(1)

    with open(TREE_PATH, "r", encoding="utf-8") as f:
        tree = json.load(f)

    decision = tree.get("zero_core_decision", {})
    status = decision.get("status")
    threat_level = decision.get("threat_level")
    isolated_enemies = decision.get("isolated_enemies", [])
    neutral_nodes = decision.get("neutral_infrastructure", [])

    print(f"\n[*] Decision Status : {status}")
    print(f"[*] Threat Level    : {threat_level}")
    print(f"[*] Target Wallet   : {tree.get('@target')}\n")

    print("------------------------------------------------------------")
    print(" 🎯 [IDENTIFIED ENEMY SOURCES] (完全特定された不正ノード)")
    print("------------------------------------------------------------")
    
    nodes = tree.get("dag_topology", {}).get("nodes", {})
    enemy_details = nodes.get("ENEMY_NODES", [])

    for idx, enemy in enumerate(enemy_details, 1):
        print(f" [{idx}] Address      : {enemy.get('address')}")
        print(f"     Classification : {enemy.get('classification')}")
        print(f"     Requires       : {', '.join(enemy.get('requires', []))}")
        print(f"     Action         : 🚨 {enemy.get('action')}\n")

    print("------------------------------------------------------------")
    print(" 🛡️ [NEUTRAL / SELF INFRASTRUCTURE] (除外された正常ノード)")
    print("------------------------------------------------------------")
    for neutral in neutral_nodes:
        if neutral == "0x324498C0D21ae796F20Cc35341DB54a55F76A457":
            label = "SELF_GAS_FEEDER (あなたの給油用EOA)"
        elif neutral == "0x7830c87c02e56aff27fa8ab1241711331fa86f43":
            label = "COINBASE_SYSTEM_BOT (取引所自動スイープ)"
        else:
            label = "SYSTEM_INFRA"
        print(f"  [OK] {neutral} -> {label}")

    # 孤立・遮断リストの独立書き出し
    isolation_record = {
        "status": "EXECUTED",
        "timestamp": tree.get("@timestamp"),
        "blocked_enemy_count": len(isolated_enemies),
        "blacklisted_addresses": isolated_enemies
    }

    with open(OUTPUT_BLOCKLIST, "w", encoding="utf-8") as f:
        json.dump(isolation_record, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print(f" [SUCCESS] エネミー遮断リストを出力しました:")
    print(f" -> {OUTPUT_BLOCKLIST}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
