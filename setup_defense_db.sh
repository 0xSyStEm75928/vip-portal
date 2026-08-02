#!/bin/sh

# 1. データベースファイル名
DB_FILE="pandemonium_defense.db"

echo "[*] Initializing Pandemonium Threat Metadata Database..."

# 2. SQLite3へSQLメッセージを叩き込んでテーブルとインデックスを作成
sqlite3 "$DB_FILE" << 'SQL_EOF'
-- 敵の攻撃パターンを「栄養素」として蓄積するメタデータテーブル
CREATE TABLE IF NOT EXISTS attacker_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    user_agent TEXT,
    stolen_hash_used TEXT,
    payload_signature TEXT,
    attack_count INTEGER DEFAULT 1,
    threat_level INTEGER DEFAULT 1,
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 高速照合用のインデックス
CREATE INDEX IF NOT EXISTS idx_threat_ip ON attacker_metadata(ip_address);
CREATE INDEX IF NOT EXISTS idx_threat_hash ON attacker_metadata(stolen_hash_used);

.tables
SQL_EOF

echo "[+] Defense Database Layer Fortified! File: $DB_FILE"
