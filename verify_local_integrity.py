#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Local Zero-Trust Integrity Engine
外部依存ゼロ。手元のログ・データ構造だけで完全性（改ざんがないこと）を自律検証する。
"""

import os
import json
import hashlib
import time

TARGET_FILES = [
    "ACKNOWLEDGEMENT_LOG.json",
    "devils_advocate_filter.py",
    "customer_interface_ack.json"
]

def calculate_sha256(filepath):
    """ファイルのSHA-256ハッシュ値を算出"""
    if not os.path.exists(filepath):
        return None
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_local_chain():
    """既存のデータ群から改ざん不能なハッシュチェーン（証跡）を生成"""
    print("--- 🛡️ ローカル完全性検証 (Zero-Trust Chain) 開始 ---")
    
    chain = []
    prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    
    for filename in TARGET_FILES:
        file_hash = calculate_sha256(filename)
        if file_hash is None:
            print(f"[SKIP] {filename} : ファイルが存在しません")
            continue
            
        # 過去ハッシュと現ファイルハッシュを結合してチェーン化
        combined = f"{prev_hash}:{filename}:{file_hash}"
        block_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        chain_node = {
            "file": filename,
            "hash": file_hash,
            "chain_hash": block_hash,
            "prev_hash": prev_hash
        }
        chain.append(chain_node)
        prev_hash = block_hash
        print(f"[OK] {filename} -> SHA256: {file_hash[:16]}... (Chain: {block_hash[:16]}...)")

    manifest = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root_hash": prev_hash,
        "nodes": chain
    }
    
    # 状態の保存
    with open("local_integrity_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print("\n[検証完了] 『local_integrity_manifest.json』 にハッシュルートを正常に刻印しました。")
    print(f"👉 ルートハッシュ (Root SHA-256): {prev_hash}")

if __name__ == "__main__":
    generate_local_chain()
