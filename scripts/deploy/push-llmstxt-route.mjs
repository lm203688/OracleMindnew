// Push the llms.txt route (GEO entry) to GitHub master via Git Data API.
// Run: GITHUB_TOKEN=ghp_xxx node push-llmstxt-route.mjs
const TOKEN = process.env.GITHUB_TOKEN;
const OWNER = 'lm203688';
const REPO = 'oraclemind';
const PUSH_REF = 'master';
const ROOT = 'C:/Users/xing/Desktop/oraclemind/vercel-deploy';
const COMMIT_MESSAGE = 'fix(geo): serve GEO-hardened llms.txt from the route (was overridden by stale static copy)';

const FILES = [
  ['src/app/llms.txt/route.ts', `${ROOT}/src/app/llms.txt/route.ts`],
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
  const parentCommit = await api('GET', `/git/commits/${parentSha}`);
  const PARENT_TREE = parentCommit.tree.sha;

  const entries = [];
  for (const [repoPath, localPath] of FILES) {
    const content = fs.readFileSync(localPath, 'base64');
    const blob = await api('POST', '/git/blobs', { content, encoding: 'base64' });
    entries.push({ path: repoPath, mode: '100644', type: 'blob', sha: blob.sha });
  }

  const tree = await api('POST', '/git/trees', { base_tree: PARENT_TREE, tree: entries });
  const commit = await api('POST', '/git/commits', { message: COMMIT_MESSAGE, tree: tree.sha, parents: [parentSha] });
  const upd = await api('PATCH', `/git/refs/heads/${PUSH_REF}`, { sha: commit.sha, force: false });
  console.log('ref updated ->', upd.object.sha, 'commit', commit.sha);
  console.log('DONE');
})().catch((e) => { console.error('FAILED:', e.message); process.exit(1); });
