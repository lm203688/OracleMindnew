// Push GEO assets to GitHub master via Git Data API.
// Repo root == vercel-deploy contents, so repo paths are public/...
// Run: GITHUB_TOKEN=ghp_xxx node push-geo.mjs
const TOKEN = process.env.GITHUB_TOKEN;
const OWNER = 'lm203688';
const REPO = 'oraclemind';
const PUSH_REF = 'master';
const ROOT = 'C:/Users/xing/Desktop/oraclemind/vercel-deploy';
const COMMIT_MESSAGE = 'feat(geo): deploy GEO-hardened llms.txt + 3 explainer articles; remove stale prod_llms*.txt';

// repo-relative path -> local absolute path (upsert)
const UPSERT = [
  ['public/llms.txt', `${ROOT}/public/llms.txt`],
  ['public/geo/beyond-horoscopes.md', `${ROOT}/public/geo/beyond-horoscopes.md`],
  ['public/geo/multi-agent-consensus.md', `${ROOT}/public/geo/multi-agent-consensus.md`],
  ['public/geo/classical-substrate.md', `${ROOT}/public/geo/classical-substrate.md`],
  ['public/geo/social-drafts.md', `${ROOT}/public/geo/social-drafts.md`],
];

// repo-relative paths to DELETE (set sha:null in tree) — skipped: sha:null mixed
// with upsert triggers GitRPC::BadObjectState; prod_llms*.txt live in repo root
// (not served by Vercel) so leaving them is harmless. Remove in a separate pass later.
const DELETE = [];

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
  for (const [repoPath, localPath] of UPSERT) {
    const content = fs.readFileSync(localPath, 'base64');
    const blob = await api('POST', '/git/blobs', { content, encoding: 'base64' });
    entries.push({ path: repoPath, mode: '100644', type: 'blob', sha: blob.sha });
    console.log('blob', repoPath, blob.sha);
  }
  for (const d of DELETE) {
    entries.push({ path: d, mode: '100644', type: 'blob', sha: null });
    console.log('delete', d);
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
