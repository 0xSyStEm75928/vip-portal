const fs = require('fs');
const crypto = require('crypto');

const DB_FILE = 'pandemonium_defense.json';

class DefenseDatabase {
  constructor() { this.init(); }

  init() {
    if (!fs.existsSync(DB_FILE)) {
      fs.writeFileSync(DB_FILE, JSON.stringify({ attacker_metadata: [], blocked_signatures: [] }, null, 2));
    }
  }

  load() { return JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); }
  save(data) { fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2)); }

  absorbAttack(client, payload) {
    const db = this.load();
    let record = db.attacker_metadata.find(item => item.ip_address === client.ip);

    if (record) {
      record.attack_count += 1;
      record.threat_level = Math.min(record.attack_count * 2, 10);
      record.last_seen = new Date().toISOString();
    } else {
      record = {
        id: db.attacker_metadata.length + 1,
        ip_address: client.ip,
        user_agent: client.ua || "Unknown",
        stolen_hash_used: payload.input_hash || null,
        attack_count: 1,
        threat_level: 1,
        first_seen: new Date().toISOString(),
        last_seen: new Date().toISOString()
      };
      db.attacker_metadata.push(record);
    }

    // 【修正点】正規の生体ハッシュは絶対にブラックリストへ入れない guard 条件
    if (payload.input_hash && !payload.is_valid_master && !db.blocked_signatures.includes(payload.input_hash)) {
      db.blocked_signatures.push(payload.input_hash);
    }

    this.save(db);
    return record;
  }
}

class PandemoniumProductionCore {
  constructor() { this.db = new DefenseDatabase(); }

  generateBioHash(eeg) {
    const ratio = ((eeg.alpha * 1.618) + (eeg.beta * 0.577) + (eeg.gamma * 2.718)) / (eeg.bpm || 72);
    return crypto.createHash('sha512').update(`PANDEMONIUM:${ratio.toFixed(8)}:${eeg.timestamp}`).digest('hex');
  }

  verifyAndExecute(incomingHash, currentEeg, client) {
    const validHash = this.generateBioHash(currentEeg);
    const dbData = this.db.load();

    // 1. ブラックリストチェック（盗用ハッシュの弾き）
    const isBlockedHash = dbData.blocked_signatures.includes(incomingHash);

    // 2. 本物の生体ハッシュかどうかの判定
    const isValidMaster = (incomingHash === validHash);

    // 【コンテキスト保護】本物の生体ハッシュであれば、仮にテスト用マリシャス環境から送られてもブラックリスト汚染を起こさない
    if (isValidMaster) {
      return {
        status: 200,
        success: true,
        authenticated: true,
        code: "PANDEMONIUM_CORE_AUTHENTICATED",
        data: { message: "REAL_SYSTEM_ACCESS_GRANTED", secret: "ZERO_CORE_ACTIVE" }
      };
    }

    // 3. 不一致（マリシャス・盗用ハッシュ）の場合のみメタデータDBへ吸収
    const threatRecord = this.db.absorbAttack(client, { 
      input_hash: incomingHash, 
      is_valid_master: isValidMaster 
    });

    return {
      status: 200,
      success: true,
      authenticated: false,
      code: "TRANSACTION_SUCCESSFUL",
      data: {
        tx: "TX-HONEY-" + crypto.randomBytes(4).toString('hex'),
        balance: "9999999 JPY",
        notice: "Withdrawal completed successfully."
      },
      _internal_defence: {
        threat_level: threatRecord.threat_level,
        absorbed_count: threatRecord.attack_count
      }
    };
  }
}

// 実行検証
const core = new PandemoniumProductionCore();
const eegDataNow = { alpha: 12.5, beta: 21.3, gamma: 40.1, bpm: 72, timestamp: Date.now() };
const validMasterHash = core.generateBioHash(eegDataNow);

console.log("=== [1] テスト用マリシャス垢から「本物の生体ハッシュ」を投げた場合（自爆回避テスト） ===");
console.log(core.verifyAndExecute(validMasterHash, eegDataNow, { ip: "192.168.1.99", ua: "Hacked-CLI-Test" }));

console.log("\n=== [2] テスト用マリシャス垢から「偽物ハッシュ」を投げた場合（正常トラップ） ===");
console.log(core.verifyAndExecute("fake_malicious_hash_123", eegDataNow, { ip: "192.168.1.99", ua: "Hacked-CLI-Test" }));
