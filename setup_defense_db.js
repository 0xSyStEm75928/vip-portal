const fs = require('fs');

const DB_FILE = 'pandemonium_defense.json';

// データベースの初期初期化（メタデータ格納用）
function initDb() {
  if (!fs.existsSync(DB_FILE)) {
    const initialSchema = {
      attacker_metadata: [],
      blocked_signatures: []
    };
    fs.writeFileSync(DB_FILE, JSON.stringify(initialSchema, null, 2));
    console.log(`[+] Defense JSON Database Created: ${DB_FILE}`);
  } else {
    console.log(`[*] Existing Defense Database Found: ${DB_FILE}`);
  }
}

// 敵の攻撃メタデータを喰らってDBを自動更新・塗り固める関数
function absorbAttackerData(attackPayload) {
  const dbData = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
  
  // 既存の攻撃記録を検索
  let record = dbData.attacker_metadata.find(item => item.ip_address === attackPayload.ip_address);

  if (record) {
    // 過去の攻撃歴あり：カウントアップ＆脅威レベル自動上昇
    record.attack_count += 1;
    record.threat_level = Math.min(record.attack_count * 2, 10);
    record.last_seen = new Date().toISOString();
    console.log(`[!] Threat Level Escalated for IP: ${record.ip_address} (Level ${record.threat_level})`);
  } else {
    // 新規攻撃者：メタデータテーブルに追加
    record = {
      id: dbData.attacker_metadata.length + 1,
      ip_address: attackPayload.ip_address,
      user_agent: attackPayload.user_agent || "Unknown",
      stolen_hash_used: attackPayload.stolen_hash_used || null,
      payload_signature: attackPayload.payload_signature || "MALICIOUS_ACCESS",
      attack_count: 1,
      threat_level: 1,
      first_seen: new Date().toISOString(),
      last_seen: new Date().toISOString()
    };
    dbData.attacker_metadata.push(record);
    console.log(`[+] New Attacker Absorbed: ${attackPayload.ip_address}`);
  }

  // 不正ハッシュを拒絶リストに吸収
  if (attackPayload.stolen_hash_used && !dbData.blocked_signatures.includes(attackPayload.stolen_hash_used)) {
    dbData.blocked_signatures.push(attackPayload.stolen_hash_used);
  }

  // データベースへ書き戻し（永続化）
  fs.writeFileSync(DB_FILE, JSON.stringify(dbData, null, 2));
  return record;
}

// 実行テスト
initDb();

console.log("\n--- [演習] 敵の攻撃を喰らってDBを塗り固める ---");
const testAttack1 = {
  ip_address: "192.168.1.99",
  user_agent: "Hacked-CLI-v1",
  stolen_hash_used: "stolen_hash_9999",
  payload_signature: "HONEYPOT_TRIGGERED"
};

absorbAttackerData(testAttack1);
absorbAttackerData(testAttack1); // 2回目のアタック（危険度上昇）

console.log("\n[+] Database Content Fortified:");
console.log(fs.readFileSync(DB_FILE, 'utf8'));
