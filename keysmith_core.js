/**
 * Keysmith Phase 34 — Core Injection (Node.js)
 * Target: iSH / Alpine / Linux CLI
 * 100% Local & Self-Service Execution Engine
 */

const ethers = require('ethers');
const crypto = require('crypto');
const fs     = require('fs');
const path   = require('path');

// 1. パスワード変形エンジン
function generateVariations(fragment) {
  if (!fragment || fragment.trim() === '') return [];
  const base = fragment.trim();
  const vars = new Set();

  vars.add(base);
  vars.add(base.toLowerCase());
  vars.add(base.toUpperCase());
  vars.add(base[0].toUpperCase() + base.slice(1));

  const suffixes = ['!','1','123','2024','2025','2026','#','@','0','!!'];
  for (const s of suffixes) {
    vars.add(base + s);
    vars.add(base.toLowerCase() + s);
  }

  const prefixes = ['1','My','my','The'];
  for (const p of prefixes) {
    vars.add(p + base);
    vars.add(p + base[0].toUpperCase() + base.slice(1));
  }

  const leet = base.replace(/a/gi,'@').replace(/e/gi,'3').replace(/i/gi,'1').replace(/o/gi,'0');
  vars.add(leet);
  vars.add(leet + '!');

  const numMatch = base.match(/^(.*?)(\d+)$/);
  if (numMatch) {
    const n = parseInt(numMatch[2]);
    for (let i = Math.max(0,n-2); i <= n+5; i++) {
      vars.add(numMatch[1] + i);
    }
  }

  return [...vars];
}

// 2. Keystore 復号エンジン
async function tryDecrypt(keystoreJson, password) {
  try {
    const wallet = await ethers.Wallet.fromEncryptedJson(
      typeof keystoreJson === 'string' ? keystoreJson : JSON.stringify(keystoreJson),
      password
    );
    return {
      success:     true,
      password:    password,
      privateKey:  wallet.privateKey,
      address:     wallet.address
    };
  } catch(e) {
    return { success: false };
  }
}

// 3. アドレス照合
function verifyAddress(privateKey, knownAddress) {
  try {
    const wallet  = new ethers.Wallet(privateKey);
    const match   = knownAddress
      ? wallet.address.toLowerCase() === knownAddress.toLowerCase()
      : true;
    return { address: wallet.address, match };
  } catch(e) {
    return { address: null, match: false };
  }
}

// 4. メインエンジン (タイポ修正: keysmithEngine)
async function keysmithEngine({ keystoreJson, fragment, knownAddress, maxTries = 500 }) {
  console.log('\x1b[36m[Keysmith Core] 変形エンジン起動...\x1b[0m');
  const variations = generateVariations(fragment);
  console.log(`\x1b[33m[Keysmith Core] 試行パスワード数: ${variations.length}\x1b[0m`);

  for (let i = 0; i < Math.min(variations.length, maxTries); i++) {
    const pw = variations[i];
    process.stdout.write(`\r  試行 [${i+1}/${variations.length}]: ${pw.padEnd(30)}`);
    const result = await tryDecrypt(keystoreJson, pw);
    if (result.success) {
      console.log('\n\x1b[32m[✓] 復号成功!\x1b[0m');
      const verify = verifyAddress(result.privateKey, knownAddress);
      return {
        status:      'SUCCESS',
        password:    result.password,
        privateKey:  result.privateKey,
        address:     result.address,
        addressMatch: verify.match,
        triedCount:  i + 1
      };
    }
  }
  console.log('\n\x1b[31m[✗] 全変形パターン失敗\x1b[0m');
  return { status: 'FAILED', triedCount: variations.length };
}

module.exports = { keysmithEngine, generateVariations, tryDecrypt, verifyAddress };
