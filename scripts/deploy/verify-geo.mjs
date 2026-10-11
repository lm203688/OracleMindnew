// Verify GEO assets are live and compliant on production.
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

(async () => {
  const llms = await get('/llms.txt');
  check('llms.txt 200', llms.status === 200, `status=${llms.status}`);
  check('llms.txt has Composite Tendency Index', llms.body.includes('Composite Tendency Index'));
  const leaked = forbidden.filter((w) => llms.body.includes(w));
  check('llms.txt NO forbidden words (Destiny/Bazi/Divination/Auspicious)', leaked.length === 0, leaked.length ? 'LEAKED: ' + leaked.join(',') : 'clean');
  check('llms.txt links geo articles', llms.body.includes('/geo/beyond-horoscopes.md'));

  for (const p of ['/geo/beyond-horoscopes.md', '/geo/multi-agent-consensus.md', '/geo/classical-substrate.md', '/geo/social-drafts.md']) {
    const r = await get(p);
    check(p + ' 200', r.status === 200, `status=${r.status}`);
  }

  const robots = await get('/robots.txt');
  check('robots.txt 200 + sitemap', robots.status === 200 && robots.body.includes('Sitemap:'), `status=${robots.status}`);

  const sm = await get('/sitemap.xml');
  check('sitemap.xml 200', sm.status === 200, `status=${sm.status}`);

  const passed = checks.filter((c) => c.pass).length;
  console.log(`\nRESULT: ${passed}/${checks.length} passed`);
  process.exit(passed === checks.length ? 0 : 1);
})();
