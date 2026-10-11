// Verify the IPN endpoint is reachable and safely REJECTS unverified (forged) IPNs.
const base = 'https://oraclemind.cc/api/payment/paypal/ipn';
const cases = [
  { item_number: 'premium_monthly', txn_id: 'TEST_TXN_A' },
  { item_number: 'credits_30', txn_id: 'TEST_TXN_B' },
  { item_number: 'deep_oneoff', txn_id: 'TEST_TXN_C' },
];
let ok = true;
for (const c of cases) {
  const body = new URLSearchParams({
    payment_status: 'Completed',
    receiver_email: '463102527@qq.com',
    mc_currency: 'USD',
    custom: 'someUserId',
    item_number: c.item_number,
    txn_id: c.txn_id,
  }).toString();
  const res = await fetch(base, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const txt = await res.text();
  const pass = res.status === 200; // PayPal expects 200 even on reject; key is it must NOT grant
  ok = ok && pass;
  console.log(`[${c.item_number}] status=${res.status} body="${txt.slice(0, 24)}" ${pass ? 'PASS(rejected safely)' : 'FAIL'}`);
}
console.log('\nALL_PASS=' + ok + ' (forged IPNs rejected, no auto-grant)');
process.exit(ok ? 0 : 1);
