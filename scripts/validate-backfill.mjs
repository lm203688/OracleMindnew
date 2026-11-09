// validate-backfill.mjs — 校验 backfill-events.seed.json 的字段完整性与诚信底线
// 零依赖，可直接运行：node scripts/validate-backfill.mjs
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SEED = join(__dirname, '..', 'data', 'backfill-events.seed.json');

const VALID_OUTCOMES = new Set(['positive', 'negative', 'neutral']);
const errors = [];
const warnings = [];

let data;
try {
  data = JSON.parse(readFileSync(SEED, 'utf8'));
} catch (e) {
  console.error('❌ JSON 解析失败:', e.message);
  process.exit(1);
}

const events = data.events ?? [];
if (events.length === 0) errors.push('events 为空');

const ids = new Set();
for (const [i, ev] of events.entries()) {
  const tag = `events[${i}] (${ev.id ?? 'NO_ID'})`;
  if (!ev.id) errors.push(`${tag}: 缺 id`);
  if (ids.has(ev.id)) errors.push(`${tag}: id 重复`);
  ids.add(ev.id);

  if (typeof ev.question !== 'string' || ev.question.length < 10)
    errors.push(`${tag}: question 过短或缺失`);
  if (!VALID_OUTCOMES.has(ev.outcome)) errors.push(`${tag}: outcome 必须是 positive/negative/neutral`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(ev.resolutionDate ?? ''))
    errors.push(`${tag}: resolutionDate 格式应为 YYYY-MM-DD`);
  // 回填事件必须是已决议的过去事件（学术诚信：不得用未来/未决事件造假）
  if (ev.resolutionDate && ev.resolutionDate > new Date().toISOString().slice(0, 10))
    errors.push(`${tag}: resolutionDate ${ev.resolutionDate} 晚于今天，回填事件必须已决议`);
  if (typeof ev.source !== 'string' || !/^https?:\/\//.test(ev.source))
    errors.push(`${tag}: source 必须是可访问的 URL`);
  if (typeof ev.category !== 'string') warnings.push(`${tag}: 建议填 category`);
  // 首选 Metaculus 源提示（自带人群基线，便于 engine-vs-crowd 对比）
  if (!/metaculus\.com/.test(ev.source)) warnings.push(`${tag}: 非 Metaculus 源，建议优先用 metaculus.com 已决问题以获人群基线`);
}

// 诚信底线：neutral 占比不应过高（否则数据集区分度低）
const neutral = events.filter((e) => e.outcome === 'neutral').length;
if (events.length && neutral / events.length > 0.2)
  warnings.push(`neutral 占比 ${(neutral / events.length * 100).toFixed(0)}% > 20%，区分度可能不足`);

console.log(`\n校验对象: ${SEED}`);
console.log(`事件总数: ${events.length}`);
if (warnings.length) {
  console.log('\n⚠️ 警告:');
  warnings.forEach((w) => console.log('  - ' + w));
}
if (errors.length) {
  console.log('\n❌ 错误（不可通过）:');
  errors.forEach((e) => console.log('  - ' + e));
  console.log(`\n结果: 失败（${errors.length} 个错误）`);
  process.exit(1);
}
console.log('\n✅ 校验通过：字段齐全、outcome 合法、source 可达格式正确、决议日均已过去。');
console.log('注意：本校验不验证 outcome 真值本身——真值须由公开主源保证（AI 代理采集时逐条附 source，学术诚信红线）。');
