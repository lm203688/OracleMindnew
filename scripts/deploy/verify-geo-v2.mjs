// Verify GEO assets are live and compliant on production (v2 — covers 7 geo articles).
const BASE = 'https://oraclemind.cc';
const checks = [];
function check(name, cond, detail) {
  checks.push({ name, pass: !!cond, detail });
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`);
}

const forbidden = ['Destiny Forecast', 'Bazi Calculate', 'Luopan Divination', 'Auspicious', 'fortune teller'];

async function get(path) {
  try {
    const r = await fetch(BASE + path);
    const t = await r.text();
    return { status: r.status, body: t };
  } catch (e) {
    return { status: 0, body: String(e) };
  }
}

const geoArticles = [
  '/geo/beyond-horoscopes.md',
  '/geo/multi-agent-consensus.md',
  '/geo/classical-substrate.md',
  '/geo/decision-support.md',
  '/geo/probability-vs-prediction.md',
  '/geo/getting-started.md',
  '/geo/life-dimensions.md',
];

(async () => {
  const llms = await get('/llms.txt');
  check('llms.txt 200', llms.status === 200, `status=${llms.status}`);
  check('llms.txt has Composite Tendency Index', llms.body.includes('Composite Tendency Index'));
  const leaked = forbidden.filter((w) => llms.body.includes(w));
  check('llms.txt NO forbidden words', leaked.length === 0, leaked.length ? 'LEAKED: ' + leaked.join(',') : 'clean');

  // All 7 geo articles must be linked from llms.txt
  const missing = geoArticles.filter((p) => !llms.body.includes(p));
  check('llms.txt links all 7 geo articles', missing.length === 0, missing.length ? 'MISSING: ' + missing.join(',') : 'all linked');

  // All 7 geo articles must be 200 + start with a heading
  for (const p of geoArticles) {
    const r = await get(p);
    const ok = r.status === 200 && /^# /.test(r.body.trim());
    check(p + ' 200 + has H1', ok, `status=${r.status}`);
  }

  // Sitemap must include the geo articles (the prior断点)
  const sm = await get('/sitemap.xml');
  const smMissing = geoArticles.filter((p) => !sm.body.includes(p));
  check('sitemap.xml includes all 7 geo articles', sm.status === 200 && smMissing.length === 0, smMissing.length ? 'MISSING: ' + smMissing.join(',') : `status=${sm.status}`);
  check('sitemap.xml no stale /bazi-chart', sm.status === 200 && !sm.body.includes('/bazi-chart'), sm.body.includes('/bazi-chart') ? 'STALE URL PRESENT' : 'clean');

  const robots = await get('/robots.txt');
  check('robots.txt 200 + sitemap', robots.status === 200 && robots.body.includes('Sitemap:'), `status=${robots.status}`);

  const passed = checks.filter((c) => c.pass).length;
  console.log(`\nRESULT: ${passed}/${checks.length} passed`);
  process.exit(passed === checks.length ? 0 : 1);
})();
