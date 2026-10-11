// Walk the PayPal checkout flow for all 5 SKUs and assert correctness.
const items = ['premium_monthly', 'premium_yearly', 'deep_oneoff', 'credits_30', 'credits_100'];
const base = 'https://oraclemind.cc/api/payment/paypal/checkout';
const EXPECT_EMAIL = '463102527@qq.com';

let ok = true;
for (const item of items) {
  const u = `${base}?itemNumber=${item}&userId=verify_probe_${Date.now()}`;
  const res = await fetch(u);
  const body = await res.json().catch(() => ({}));
  const url = body.url || '';
  const checks = {
    status200: res.status === 200,
    hasWebscr: url.includes('paypal.com/cgi-bin/webscr'),
    business: url.includes('business=' + encodeURIComponent(EXPECT_EMAIL)),
    item: url.includes('item_number=' + item),
    currency: url.includes('currency_code=USD'),
    notify: url.includes('notify_url=' + encodeURIComponent('https://oraclemind.cc/api/payment/paypal/ipn')),
  };
  const pass = Object.values(checks).every(Boolean);
  ok = ok && pass;
  console.log(`\n[${item}] ${pass ? 'PASS' : 'FAIL'} status=${res.status}`);
  console.log('  url=', url.slice(0, 160));
  console.log('  checks=', JSON.stringify(checks));
}
console.log('\nALL_PASS=' + ok);
process.exit(ok ? 0 : 1);
