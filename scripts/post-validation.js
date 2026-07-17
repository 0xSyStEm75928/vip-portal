const fs = require('fs');

async function run() {
  try {
    const { Octokit } = require('@octokit/core');

    const repository = process.env.GITHUB_REPOSITORY || '';
    const token = process.env.GITHUB_TOKEN || '';
    const issueNumber = process.env.ISSUE_NUMBER ? parseInt(process.env.ISSUE_NUMBER, 10) : null;

    if (!repository) {
      console.log('⚠️ [INFO] GITHUB_REPOSITORY not set. Skipping API calls.');
    }
    if (!token) {
      console.log('⚠️ [INFO] GITHUB_TOKEN not set. Skipping API calls.');
    }
    if (!issueNumber) {
      console.log('⚠️ [INFO] ISSUE_NUMBER not set. Running in test/fallback mode (no API calls).');
    }

    const [owner, repo] = repository.split('/');
    const outputPath = '/tmp/validate-output.txt';
    const marker = '<!-- validate-issue-bot -->';

    let output = '';
    if (fs.existsSync(outputPath)) {
      output = fs.readFileSync(outputPath, 'utf8').trim();
    } else {
      console.log(`⚠️ [INFO] Output file ${outputPath} not found. Using fallback message.`);
      output = '⚠️ Validation completed, but no detailed log was generated.';
    }

    const outcome = process.env.OUTCOME || 'failure';
    const type = process.env.TYPE || 'case-study';
    const previewUrl = `https://www.gitcoin.co/preview?issue=${issueNumber || 'N/A'}&type=${type}`;
    const previewLine = `\n\n**Preview:** [View your submission](${previewUrl})`;

    const hasWarnings = outcome === 'success' && output.length > 0;
    const successBody = hasWarnings
      ? `${marker}\n✅ **Content validation passed** — but with reviewer notes:\n\n\`\`\`\n${output}\n\`\`\`${previewLine}\n\nOnce reviewed and approved by a maintainer, your content will be published to the site.`
      : `${marker}\n✅ **Content validation passed!** All required fields look good — this issue is ready to be reviewed.${previewLine}\n\nOnce reviewed and approved by a maintainer, your content will be published to the site.`;

    const failureBody = `${marker}\n## ❌ Content Validation Issues\n\nThe following fields need attention before this submission can be reviewed:\n\n\`\`\`\n${output}\n\`\`\`${previewLine}\n\nPlease edit the issue to fix the issues above — validation will re-run automatically.`;

    const body = outcome === 'success' ? successBody : failureBody;

    console.log(`💬 Prepared comment body for issue #${issueNumber || 'TEST'}.`);

    // If any of these are missing, skip API calls but exit successfully
    if (!owner || !repo || !token || !issueNumber) {
      console.log('ℹ️ Skipping GitHub API calls (missing env). Exiting 0.');
      return;
    }

    const octokit = new Octokit({ auth: token });

    try {
      // list comments
      const listRes = await octokit.request('GET /repos/{owner}/{repo}/issues/{issue_number}/comments', {
        owner,
        repo,
        issue_number: issueNumber,
      });

      const comments = Array.isArray(listRes.data) ? listRes.data : [];
      const existing = comments.find(c => typeof c.body === 'string' && c.body.includes(marker));

      if (existing) {
        console.log(`ℹ️ Found existing bot comment (id=${existing.id}), deleting it.`);
        await octokit.request('DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}', {
          owner,
          repo,
          comment_id: existing.id,
        });
      }

      // create new comment
      await octokit.request('POST /repos/{owner}/{repo}/issues/{issue_number}/comments', {
        owner,
        repo,
        issue_number: issueNumber,
        body,
      });

      console.log('✅ Validation comment posted/updated.');
    } catch (apiErr) {
      // Swallow API errors but log stack to help debugging later
      console.warn('[!] GitHub API error (swallowed):', apiErr && apiErr.stack ? apiErr.stack : apiErr);
    }
  } catch (err) {
    // Safety net: never throw. Log and exit 0.
    console.warn('[!] Unexpected error in post-validation.js (swallowed):', err && err.stack ? err.stack : err);
  }
}

run();
