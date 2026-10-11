// One-off: upsert PAYPAL_RECEIVER_EMAIL into Vercel project env (production target).
// Run: VERCEL_TOKEN=... PAYPAL_EMAIL=... node vercel-env-paypal.mjs
const TOKEN = process.env.VERCEL_TOKEN;
const EMAIL = process.env.PAYPAL_EMAIL;
const TEAM = 'team_dbopiTcCVu7hCeA2t4MKRA69';
const PROJECT = 'prj_rEmnM3IBHBePHPKQfJnd74pKxnj2';
const H = { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' };

if (!TOKEN || !EMAIL) { console.error('missing VERCEL_TOKEN or PAYPAL_EMAIL'); process.exit(1); }

async function listEnv() {
  const res = await fetch(`https://api.vercel.com/v10/projects/${PROJECT}/env?teamId=${TEAM}`, { headers: H });
  const body = await res.json();
  if (!res.ok) throw new Error('list fail: ' + JSON.stringify(body).slice(0, 400));
  return body.envs || [];
}

async function upsert(key, value) {
  const envs = await listEnv();
  const existing = envs.find((e) => e.key === key);
  if (existing) {
    const res = await fetch(`https://api.vercel.com/v10/projects/${PROJECT}/env/${existing.id}?teamId=${TEAM}`, {
      method: 'PATCH',
      headers: H,
      body: JSON.stringify({ value }),
    });
    const body = await res.json();
    if (!res.ok) throw new Error('PATCH fail: ' + JSON.stringify(body).slice(0, 400));
    console.log(`UPDATED ${key} (id=${existing.id})`);
    return 'updated';
  }
  const res = await fetch(`https://api.vercel.com/v10/projects/${PROJECT}/env?teamId=${TEAM}`, {
    method: 'POST',
    headers: H,
    body: JSON.stringify({ key, value, type: 'plain', target: ['production'] }),
  });
  const body = await res.json();
  if (!res.ok) throw new Error('POST fail: ' + JSON.stringify(body).slice(0, 400));
  console.log(`CREATED ${key} (id=${body.id})`);
  return 'created';
}

const action = await upsert('PAYPAL_RECEIVER_EMAIL', EMAIL);
console.log('RESULT=' + action);
