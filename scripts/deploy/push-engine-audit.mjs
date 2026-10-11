// Push engine-audit refactor to GitHub master via Git Data API (curl transport).
// Node's global fetch is unreliable in this sandbox; curl is proven working.
// Run: GITHUB_TOKEN=ghp_xxx node push-engine-audit.mjs
const TOKEN = process.env.GITHUB_TOKEN;
const OWNER = 'lm203688';
const REPO = 'oraclemind';
const PUSH_REF = 'master';
const ROOT = 'C:/Users/xing/Desktop/oraclemind/vercel-deploy';
const COMMIT_MESSAGE = 'refactor(audit): verify modern derivation method (engine-audit) instead of classical substrate — determinism / non-degeneracy / synthetic calibration oracle / drift guard';

const UPSERT = [
  ['src/lib/automation/engine-audit.ts', `${ROOT}/src/lib/automation/engine-audit.ts`],
  ['src/lib/automation/historical-backtest.ts', `${ROOT}/src/lib/automation/historical-backtest.ts`],
  ['src/app/api/automation/run/route.ts', `${ROOT}/src/app/api/automation/run/route.ts`],
  ['src/lib/automation/job-ledger.ts', `${ROOT}/src/lib/automation/job-ledger.ts`],
];

import fs from 'node:fs';
import { spawn } from 'node:child_process';

function api(method, path, body) {
  return new Promise((resolve, reject) => {
    const args = [
      '-sS', '-X', method,
      `https://api.github.com/repos/${OWNER}/${REPO}${path}`,
      '-H', `Authorization: Bearer ${TOKEN}`,
      '-H', 'Accept: application/vnd.github+json',
      '-H', 'Content-Type: application/json',
      '-H,User-Agent: oraclemind-push'.split(','),
      '--retry', '5', '--retry-delay', '2', '--retry-all-errors',
      '--max-time', '90',
    ].flat();
    if (body !== undefined) args.push('-d', JSON.stringify(body));
    const p = spawn('curl', args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '';
    let err = '';
    p.stdout.on('data', (d) => (out += d));
    p.stderr.on('data', (d) => (err += d));
    p.on('close', (code) => {
      if (code !== 0) return reject(new Error(`curl ${method} ${path} exit ${code}: ${err}`));
      try {
        resolve(out ? JSON.parse(out) : null);
      } catch (e) {
        reject(new Error(`JSON parse ${method} ${path}: ${out.slice(0, 200)}`));
      }
    });
  });
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
