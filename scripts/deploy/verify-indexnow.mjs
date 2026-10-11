// Verify IndexNow key file is live, then submit GEO URLs for re-indexing.
const BASE = 'https://oraclemind.cc';
const KEY = 'a746c0e9851fbd32';

const urls = [
  `${BASE}/llms.txt`,
  `${BASE}/geo/index.md`,
  `${BASE}/geo/beyond-horoscopes.md`,
  `${BASE}/geo/multi-agent-consensus.md`,
  `${BASE}/geo/classical-substrate.md`,
  `${BASE}/geo/decision-support.md`,
  `${BASE}/geo/probability-vs-prediction.md`,
  `${BASE}/geo/getting-started.md`,
  `${BASE}/geo/life-dimensions.md`,
  `${BASE}/geo/ai-decision-tools-comparison.md`,
  `${BASE}/geo/forecast-accuracy-calibration.md`,
  `${BASE}/geo/privacy-data-safety.md`,
  `${BASE}/geo/acting-on-forecasts.md`,
  `${BASE}/`,
  `${BASE}/pricing`,
  `${BASE}/tuivan-chart`,
  `${BASE}/daily-forecast`,
];

(async () => {
  // 1. Key file must be reachable + match
  const k = await fetch(`${BASE}/${KEY}.txt`);
  const kt = await k.text();
  console.log('key file status', k.status, 'matches', kt.trim() === KEY);

  // 2. Trigger IndexNow submission via the site's own endpoint
  const r = await fetch(`${BASE}/api/seo/indexnow`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ urls }),
  });
  const j = await r.json();
  console.log('indexnow status', r.status);
  console.log('indexnow msg', j.message);
  console.log('results', JSON.stringify(j.results));
})().catch((e) => console.log('ERR', e.message));
