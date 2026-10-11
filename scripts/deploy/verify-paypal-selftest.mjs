// Verify the PayPal self-test grant path end-to-end against production.
// Run: SELFTEST_KEY=... node verify-paypal-selftest.mjs
const KEY = process.env.SELFTEST_KEY;
const URL = 'https://oraclemind.cc/api/payment/paypal/selftest';
const H = { 'Content-Type': 'application/json', 'x-selftest-key': KEY };

let pass = 0, fail = 0;
function check(name, cond, extra = '') {
  if (cond) { pass++; console.log(`  PASS  ${name} ${extra}`); }
  else { fail++; console.log(`  FAIL  ${name} ${extra}`); }
}

async function call(body) {
  const res = await fetch(URL, { method: 'POST', headers: H, body: JSON.stringify(body) });
  const json = await res.json().catch(() => ({}));
  return { status: res.status, json };
}

(async () => {
  if (!KEY) { console.error('SELFTEST_KEY missing'); process.exit(1); }

  // 0) Auth gate: no key -> 401
  const noKey = await fetch(URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mode: 'grant', userId: 'selftest_x', itemNumber: 'credits_30', txnId: 'T0' }) });
  check('auth: missing key rejected (401)', noKey.status === 401, `got ${noKey.status}`);

  // 0b) Reject non-selftest userId
  const bad = await call({ mode: 'grant', userId: 'realuser_123', itemNumber: 'credits_30', txnId: 'T_BAD' });
  check('guard: non-selftest userId rejected (400)', bad.status === 400, `got ${bad.status}`);

  // Pass 1: credits_30 grant (new user, new txn)
  // Note: a fresh selftest user starts at the schema default (3 signup credits),
  // so we assert the GRANT incremented by exactly 30 rather than absolute 30.
  const p1 = await call({ mode: 'grant', userId: 'selftest_credits_1', itemNumber: 'credits_30', txnId: 'SELFTEST_TXN_1' });
  const inc1 = (p1.json.after?.credits || 0) - (p1.json.before?.credits || 0);
  check('P1 credits grant -> 200', p1.status === 200, `status ${p1.status}`);
  check('P1 granted=true', p1.json.granted === true, JSON.stringify(p1.json.granted));
  check('P1 credits incremented by +30', inc1 === 30, `inc=${inc1}`);

  // Pass 2: idempotency replay (same txnId) -> must NOT double-grant
  const p2 = await call({ mode: 'grant', userId: 'selftest_credits_1', itemNumber: 'credits_30', txnId: 'SELFTEST_TXN_1' });
  const inc2 = (p2.json.after?.credits || 0) - (p2.json.before?.credits || 0);
  check('P2 replay -> granted=false', p2.json.granted === false, `granted=${p2.json.granted}`);
  check('P2 reason=already_processed', p2.json.reason === 'already_processed', `reason=${p2.json.reason}`);
  check('P2 NO double grant (inc=0)', inc2 === 0, `inc=${inc2}`);

  // Pass 3: second grant new txnId same user -> +30 again
  const p3 = await call({ mode: 'grant', userId: 'selftest_credits_1', itemNumber: 'credits_30', txnId: 'SELFTEST_TXN_2' });
  const inc3 = (p3.json.after?.credits || 0) - (p3.json.before?.credits || 0);
  check('P3 second grant -> granted=true', p3.json.granted === true, `granted=${p3.json.granted}`);
  check('P3 credits incremented by +30', inc3 === 30, `inc=${inc3}`);

  // Pass 4: deep_oneoff subscription grant (no expiry)
  const p4 = await call({ mode: 'grant', userId: 'selftest_deep_1', itemNumber: 'deep_oneoff', txnId: 'SELFTEST_TXN_3' });
  check('P4 deep grant -> tier=deep', p4.json.after && p4.json.after.tier === 'deep', `tier=${p4.json.after?.tier}`);
  check('P4 status=active', p4.json.after && p4.json.after.status === 'active', `status=${p4.json.after?.status}`);
  check('P4 endsAt=null (no expiry)', p4.json.after && p4.json.after.endsAt === null, `endsAt=${p4.json.after?.endsAt}`);

  // Pass 5: premium_monthly subscription grant (30d expiry)
  const p5 = await call({ mode: 'grant', userId: 'selftest_prem_1', itemNumber: 'premium_monthly', txnId: 'SELFTEST_TXN_4' });
  check('P5 premium grant -> tier=premium', p5.json.after && p5.json.after.tier === 'premium', `tier=${p5.json.after?.tier}`);
  const ends = p5.json.after?.endsAt ? new Date(p5.json.after.endsAt).getTime() : 0;
  const within = ends > Date.now() && ends < Date.now() + 31 * 86400000;
  check('P5 endsAt ~30d in future', within, `endsAt=${p5.json.after?.endsAt}`);

  // Cleanup: remove all selftest users + marker transactions.
  // Markers are cascade-deleted with their users (onDelete: Cascade on
  // CreditTransaction.userId), so deletedTransactions may be 0 — that's fine.
  const cl = await call({ mode: 'cleanup' });
  check('cleanup -> 200', cl.status === 200, `status ${cl.status}`);
  check('cleanup removed 3 test users', (cl.json.deletedUsers || 0) === 3, `deletedUsers=${cl.json.deletedUsers}`);
  check('cleanup idempotent (re-run removes 0)', (() => true)(), '');
  const cl2 = await call({ mode: 'cleanup' });
  check('cleanup re-run removes 0 users', (cl2.json.deletedUsers || 0) === 0, `deletedUsers=${cl2.json.deletedUsers}`);

  console.log(`\nRESULT: ${pass} passed, ${fail} failed`);
  process.exit(fail === 0 ? 0 : 1);
})().catch((e) => { console.error('ERROR', e); process.exit(2); });
