const fs = require('fs');
const { execSync } = require('child_process');

console.log("=== 🛡️ ZERO-GUARDIAN (AI-Hekado Shield) 監査開始 ===");

let hasError = false;

// 1. 直書きハッシュ / 機密パターンの検出（64バイト以上のHEXや特定文字列）
const jsFiles = fs.readdirSync('.').filter(f => f.endsWith('.js'));
const secretRegex = /[a-f0-9]{64,128}/i; // SHA-256 / SHA-512 の直書きパターン

jsFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  if (secretRegex.test(content) && !file.includes('zero_guardian.js')) {
    console.error(`[❌ AI_HEKADO_DETECTED] ${file} 内に生ハッシュ/鍵の直書きを発見しました！`);
    hasError = true;
  }
});

// 2. Gitコミット履歴の深さチェック（過去ログに汚いコミットが残っていないか）
try {
  const gitLog = execSync('git log --oneline').toString().trim().split('\n');
  if (gitLog.length > 1) {
    console.warn(`[⚠️ WARN] コミット履歴が ${gitLog.length} 件あります。過去のコミットに機密が残っていないか確認してください。`);
  }
} catch (e) {
  // Git初期化前など
}

// 3. 追跡対象ファイルに危険なファイル（.ash_history, .envなど）がないか
try {
  const gitStatus = execSync('git status --porcelain').toString();
  if (gitStatus.includes('.ash_history') || gitStatus.includes('.env')) {
    console.error(`[❌ DANGER] 危険なログファイル（.ash_history/.env）がGitの追跡対象に入っています！`);
    hasError = true;
  }
} catch (e) {}

if (hasError) {
  console.error("\n💥 [GUARDIAN BLOCK] AIのミス/セキュリティリスクを検知したため、操作を中断しました。");
  process.exit(1);
} else {
  console.log("✅ [GUARDIAN PASSED] コード・Git状態は完全にクリーンです。安全に進行できます。");
}
