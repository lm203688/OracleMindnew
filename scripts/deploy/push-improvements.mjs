// Push A/B/C/D improvements + P0 feedback automation to GitHub master via Git Data API.
// Repo root == vercel-deploy contents, so repo paths are src/... or public/...
// Run: GITHUB_TOKEN=ghp_xxx node push-improvements.mjs
const TOKEN = process.env.GITHUB_TOKEN;
if (!TOKEN) { console.error('GITHUB_TOKEN required'); process.exit(1); }
const OWNER = 'lm203688';
const REPO = 'oraclemind';
const PUSH_REF = 'master';
const ROOT = 'C:/Users/xing/Desktop/oraclemind/vercel-deploy';
const COMMIT_MESSAGE = 'feat(improvements): A-HMAC-signature + B-quality-evolution + C-30s-preview + D-geo-tables + P0-feedback-reminder + field-verify-bugfix';

const FILES = [
  // A: HMAC 签名
  ['src/app/api/public/field/route.ts', `${ROOT}/src/app/api/public/field/route.ts`],
  ['src/app/api/field/verify/route.ts', `${ROOT}/src/app/api/field/verify/route.ts`],
  // B: Quality Evolution
  ['src/app/api/quality-evolution/route.ts', `${ROOT}/src/app/api/quality-evolution/route.ts`],
  ['src/app/quality-evolution/page.tsx', `${ROOT}/src/app/quality-evolution/page.tsx`],
  // C: 30s Preview
  ['src/app/api/preview/route.ts', `${ROOT}/src/app/api/preview/route.ts`],
  ['src/app/preview/page.tsx', `${ROOT}/src/app/preview/page.tsx`],
  // P0: Feedback reminder cron in vercel.json
  ['vercel.json', `${ROOT}/vercel.json`],
];

import fs from 'node:fs';

async function api(method, path, body) {
  const res = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      Accept: 'application/vnd.github+json',
      'Content-Type': 'application/json',
      'User-Agent': 'oraclemind-push',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`GitHub API ${method} ${path} -> ${res.status}: ${text}`);
  return text ? JSON.parse(text) : null;
}

(async () => {
  const ref = await api('GET', `/git/refs/heads/${PUSH_REF}`);
  const parentSha = ref.object.sha;
  console.log(`remote ${PUSH_REF} ->`, parentSha);

  const parentCommit = await api('GET', `/git/commits/${parentSha}`);
  const PARENT_TREE = parentCommit.tree.sha;
  console.log('parent tree ->', PARENT_TREE);

  const entries = [];
  for (const [repoPath, localPath] of FILES) {
    if (!fs.existsSync(localPath)) { console.warn(`SKIP missing: ${localPath}`); continue; }
    const content = fs.readFileSync(localPath, 'base64');
    const blob = await api('POST', '/git/blobs', { content, encoding: 'base64' });
    entries.push({ path: repoPath, mode: '100644', type: 'blob', sha: blob.sha });
    console.log('blob', repoPath, blob.sha);
  }

  const tree = await api('POST', '/git/trees', { base_tree: PARENT_TREE, tree: entries });
  console.log('tree', tree.sha);

  const commit = await api('POST', '/git/commits', {
    message: COMMIT_MESSAGE,
    tree: tree.sha,
    parents: [parentSha],
  });
  console.log('commit', commit.sha);

  const upd = await api('PATCH', `/git/refs/heads/${PUSH_REF}`, { sha: commit.sha, force: false });
  console.log('ref updated ->', upd.object.sha);
  console.log('DONE');
})().catch((e) => {
  console.error('FAILED:', e.message);
  process.exit(1);
});
