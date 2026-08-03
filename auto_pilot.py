import json
import hashlib
import os
import random
from datetime import datetime, timedelta

MASTER_HASH = "5a7e2a8a98e220c447978cd65f49252228e70a79a0e00a3714c37dfaee0b32dc"

# 顧客アバターネーム生成用プレフィックス
AVATAR_PREFIXES = ["Cyber", "Apex", "Vortex", "Shadow", "Nexus", "Quantum", "Cipher", "Aegis"]

def get_timestamp(offset_seconds=0) -> str:
    dt = datetime.now() - timedelta(seconds=offset_seconds)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def compute_nullification_factor(input_signals: list) -> int:
    quantized = [round(v, 1) for v in input_signals]
    formatted_json = json.dumps(quantized, separators=(',', ':'))
    current_hash = hashlib.sha256(formatted_json.encode('utf-8')).hexdigest()
    return int(current_hash == MASTER_HASH)

def generate_avatar_name(node_id: str) -> str:
    """送信元ノードハッシュ値から一意な顧客アバターネームを紐付け生成"""
    hash_val = hashlib.md5(node_id.encode('utf-8')).hexdigest()
    prefix = AVATAR_PREFIXES[int(hash_val[:2], 16) % len(AVATAR_PREFIXES)]
    suffix = node_id.split('_')[-1]
    return f"Anon_{prefix}_{suffix}"

def generate_100_node_messages(file_path="node_queue.json"):
    offer_subjects = [
        "【案件打診】セキュリティ層インフラ設計・構築の依頼",
        "【オファー】アノニマスノード自律防衛ロジックの最適化業務",
        "【案件照会】多層暗号パイプラインのコード監査および運用保守",
        "【直接打診】分散型プライベートノード間アーキテクチャ設計",
        "【新規打診】生体シグナルフェイルセーフ層の実装案件"
    ]
    
    messages = []
    
    for i in range(1, 101):
        is_pass = (i % 7 == 0 or i in [1, 3, 12, 25, 42, 58, 77, 89, 95])
        
        if is_pass:
            sig = [12.42, 45.18, 88.03, 15.91]
            subj = offer_subjects[(i % len(offer_subjects))]
            msg_type = "JOB_OFFER"
            node_id = f"node_p2p_{(i * 137) % 65535:04x}"
            content = f"正規署名認証済み案件オファー - 詳細条件の調整・受託打診"
        else:
            sig = [round(random.uniform(0, 100), 2) for _ in range(4)]
            subj = "【自動遮断ログ】不正アクセスまたは閾値外シグナル"
            msg_type = "BLOCKED_SIGNAL"
            node_id = f"node_p2p_{random.randint(4000, 9999):04x}"
            content = "不正シグナル（自動ブロック対象）"

        messages.append({
            "id": f"OFFER-{i:04d}" if is_pass else f"MSG-{i:04d}",
            "timestamp": get_timestamp(3600 - (i * 35)),
            "type": msg_type,
            "sender_node": node_id,
            "subject": subj,
            "signals": sig,
            "content": content
        })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def load_and_display_unique_passed_messages(file_path="node_queue.json"):
    generate_100_node_messages(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    # 重複除外＆セキュリティアバターネーム関連付け
    passed_messages = []
    seen_fingerprints = set()

    for msg in messages:
        if compute_nullification_factor(msg.get("signals", [])) == 1:
            # フィンガープリントによる重複チェック（送信元ノード + 件名）
            fp = f"{msg.get('sender_node')}_{msg.get('subject')}"
            if fp not in seen_fingerprints:
                seen_fingerprints.add(fp)
                # アバターネーム追加
                msg["avatar_name"] = generate_avatar_name(msg.get("sender_node"))
                passed_messages.append(msg)

    print("=" * 80)
    print(f"[{get_timestamp()}] [SECURE_INBOX] ✅ 顧客アバター紐付け済み・重複排除オファー一覧")
    print(" セキュリティ強化: アバターネーム関連付け | 被り除外モード: 有効")
    print("=" * 80)

    total_passed = len(passed_messages)
    print(f"[{get_timestamp()}] [SUMMARY] 重複排除後の正規顧客オファー: {total_passed} 件")
    print("-" * 80)

    for idx, msg in enumerate(passed_messages, 1):
        print(f"[{idx:02d}/{total_passed}] ID: {msg.get('id')} | 受信時刻: {msg.get('timestamp')}")
        print(f"       ├─ 顧客アバター : 👤 {msg.get('avatar_name')} ({msg.get('sender_node')})")
        print(f"       ├─ 件名         : {msg.get('subject')}")
        print(f"       ├─ 本文         : {msg.get('content')}")
        print(f"       ├─ 認証シグナル : {msg.get('signals')}")
        print(f"       └─ 判定ステータス: ✅ [PASS] 正規認証完了")
        print("-" * 80)

    print(f"[{get_timestamp()}] [PANEL_COMPLETE] ✅ アバター紐付け・重複排除完了")
    print("=" * 80)

if __name__ == "__main__":
    load_and_display_unique_passed_messages()
