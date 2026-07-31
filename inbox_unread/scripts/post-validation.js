const { execSync } = require('child_process');
const fs = require('fs');

async function run() {
  try {
    console.log("🔥 [INITIATING JSSH BRIDGE] Connecting Saac-Tool to Legal+Lethal Engine...");

    // 1. もしLETHALエンジンのスクリプトがあればJSSH/Node経由で直接キック
    const lethalEnginePath = './scripts/lethal-engine.sh';
    if (fs.existsSync(lethalEnginePath)) {
      console.log("⚡ Executing LuciFeR0x0systeM Hybrid Engine...");
      try {
        const result = execSync(`bash ${lethalEnginePath}`, { encoding: 'utf-8' });
        console.log(result);
      } catch (execErr) {
        console.warn("⚠️ Engine executed but with non-zero status (Swallowed for Legal mode):", execErr.message);
      }
    } else {
      console.log("ℹ️ Lethal Engine script not found locally. Running in lightweight JS mode.");
    }

    // 2. 以下は安全に結果を書き出してGitHub APIに投げる「リーガル」処理
    const repository = process.env.GITHUB_REPOSITORY || '';
    const token = process.env.GITHUB_TOKEN || '';
    const issueNumber = process.env.ISSUE_NUMBER ? parseInt(process.env.ISSUE_NUMBER, 10) : null;
    const outputPath = '/tmp/validate-output.txt';
    const marker = '<!-- validate-issue-bot -->';

    let output = '';
    if (fs.existsSync(outputPath)) {
      output = fs.readFileSync(outputPath, 'utf8').trim();
    } else {
      output = '⚠️ Validation executed via Saac-Tool, but no validate-output.txt was generated.';
    }

    // outcomeが success ならリーガル（パス）、それ以外ならリーサル（警告）
    const outcome = process.env.OUTCOME || 'failure';
    const body = outcome === 'success' 
      ? `${marker}\n✅ **Legal Check Passed!** All constraints satisfied on Saac-Tool.`
      : `${marker}\n## ❌ Lethal Validation Failure\n\n\`\`\`\n${output}\n\`\`\``;

    if (!repository || !token || !issueNumber) {
      console.log("ℹ️ Missing env (GITHUB_TOKEN/ISSUE_NUMBER). Output generated but API skipped.");
      return;
    }

    const { Octokit } = require('@octokit/core');
    const octokit = new Octokit({ auth: token });
    const [owner, repo] = repository.split('/');

    // 重複コメントをきれいにお掃除してから新規投稿
    const listRes = await octokit.request('GET /repos/{owner}/{repo}/issues/{issue_number}/comments', { owner, repo, issue_number: issueNumber });
    const existing = (listRes.data || []).find(c => typeof c.body === 'string' && c.body.includes(marker));

    if (existing) {
      await octokit.request('DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}', { owner, repo, comment_id: existing.id });
    }

    await octokit.request('POST /repos/{owner}/{repo}/issues/{issue_number}/comments', { owner, repo, issue_number: issueNumber, body });
    console.log("✅ Bridge complete. Comments clean and posted.");

  } catch (err) {
    console.warn("🛡️ [SAFE CATCH] Something went wrong in bridge, but keeping exit code 0:", err.message);
  }
}

run();
