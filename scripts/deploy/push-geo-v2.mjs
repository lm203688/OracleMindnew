// Push GEO v2 assets to GitHub master via Git Data API.
// Repo root == vercel-deploy contents, so repo paths are public/... or src/...
// Run: GITHUB_TOKEN=ghp_xxx node push-geo-v2.mjs
const TOKEN = process.env.GITHUB_TOKEN;
const OWNER = 'lm203688';
const REPO = 'oraclemind';
const PUSH_REF = 'master';
const ROOT = 'C:/Users/xing/Desktop/oraclemind/vercel-deploy';
const COMMIT_MESSAGE = 'feat(geo): expand GEO content cluster to 7 articles; wire into llms.txt + sitemap; fix stale sitemap.xml';

// repo-relative path -> local absolute path (upsert)
const UPSERT = [
  ['public/geo/decision-support.md', `${ROOT}/public/geo/decision-support.md`],
  ['public/geo/probability-vs-prediction.md', `${ROOT}/public/geo/probability-vs-prediction.md`],
  ['public/geo/getting-started.md', `${ROOT}/public/geo/getting-started.md`],
  ['public/geo/life-dimensions.md', `${ROOT}/public/geo/life-dimensions.md`],
  ['src/app/llms.txt/route.ts', `${ROOT}/src/app/llms.txt/route.ts`],
  ['src/app/sitemap.ts', `${ROOT}/src/app/sitemap.ts`],
  ['public/sitemap.xml', `${ROOT}/public/sitemap.xml`],
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
  for (const [repoPath, localPath] of UPSERT) {
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
