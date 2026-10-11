// Production smoke test for the calibration + 3-way outcome funnel deploy.
const BASE = 'https://oraclemind.cc';

async function get(path) {
  const r = await fetch(BASE + path, { method: 'GET' });
  return { status: r.status, body: await r.text() };
}
async function post(path, json) {
  const r = await fetch(BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(json),
  });
  return { status: r.status, body: await r.text() };
}

let pass = 0, fail = 0;
function check(name, cond, extra = '') {
  if (cond) { pass++; console.log('  PASS', name); }
  else { fail++; console.log('  FAIL', name, extra); }
}

(async () => {
  console.log('== Production smoke test ==');

  // 1. Share page renders (graceful 200 even for unknown id)
  const share = await get('/share/does-not-exist-xyz');
  check('share page returns 200', share.status === 200, `status=${share.status}`);

  // 2. Stats endpoint no regression
  const stats = await get('/api/feedback/stats');
  check('feedback/stats returns 200', stats.status === 200, `status=${stats.status}`);

  // 3. 3-way outcome feedback accepted (accurate / partly / off)
  for (const rating of ['correct', 'neutral', 'incorrect']) {
    const r = await post('/api/feedback', {
      type: 'accuracy',
      message: `smoke test ${rating}`,
      simulationId: 'smoke-test-sim-001',
      accuracyRating: rating,
    });
    check(`feedback accuracy (${rating}) -> 200`, r.status === 200, `status=${r.status} body=${r.body.slice(0, 80)}`);
  }

  // 4. General feedback still works
  const gen = await post('/api/feedback', { type: 'general', message: 'smoke test general' });
  check('general feedback -> 200', gen.status === 200, `status=${gen.status}`);

  console.log(`\nRESULT: ${pass} pass / ${fail} fail`);
  process.exit(fail === 0 ? 0 : 1);
})().catch((e) => { console.error('ERROR', e); process.exit(2); });
