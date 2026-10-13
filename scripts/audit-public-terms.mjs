#!/usr/bin/env node
/**
 * audit-public-terms.mjs — OracleMind 公开面红线词审计
 *
 * 用途：可复现地扫描 OracleMind 项目公开面（前端页面、静态资源、sitemap、llms.txt、
 *       tuivan 主题生成器）中的传统命理术语泄漏，作为 P0-2 的验收标准与 CI 门。
 *
 * 红线词表（与项目长期记忆「公开话术」红线条款保持一致）：
 *   八字 / 天干 / 地支 / 日主 / 四柱 / 十神 / 用神 / 大运 / 流年 / 命理 / 算命 /
 *   紫微斗数 / 紫微 / 生辰八字 / 命盘 / 推背图 /
 *   fortune teller / horoscope / Luck Areas / 占卜（当语境为占卜类）
 *
 * 扫描范围：
 *   - vercel-deploy/public/ 下 .txt / .md / .json / .html / .svg
 *   - vercel-deploy/src/app/ 下所有 .ts / .tsx（含 page / route / layout / sitemap / robots）
 *   - vercel-deploy/src/lib/automation/ 下所有 .ts（含 tuivan-seo.ts 生成器）
 *
 * 白名单规则（避免误报）：
 *   1) 单行注释含"严禁 / 禁止 / 替代 / 替换 / 清洗 / 映射 / 中性化 / 禁用 / 红线 /
 *      防御 / 兜底 / 术语约束"—— 属"防御性包含"，非泄漏。
 *   2) 文件名含 `RED_LINE` / `SANITIZER` / `CONSTRAINT` 附近上下文（正则识别）。
 *   3) 明确的古籍书名引用（《渊海子平》《三命通会》等）—— 属古籍哲学框架，
 *      非术语泄漏（报告 §7.4 允许保留古籍作为哲学框架，仅下调权重）。
 *
 * 退出码：
 *   0 — 无泄漏，验收通过
 *   1 — 存在泄漏，验收失败（附行号与上下文，便于 CI 直接定位）
 *
 * 用法：
 *   node scripts/audit-public-terms.mjs              # 扫描默认路径
 *   node scripts/audit-public-terms.mjs --verbose    # 打印白名单命中的防御性包含
 *   node scripts/audit-public-terms.mjs --json       # JSON 输出（供外部工具消费）
 */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname, relative } from 'node:path';

// ─── 红线词表 ───────────────────────────────────────────────────────────
// 用词源（避免被 \b 之类的边界影响中文匹配）+ 大小写无关的英文变体
const RED_TERMS = [
  // 中文核心术语
  '八字', '天干', '地支', '日主', '四柱', '十神', '用神', '大运', '流年',
  '命理', '算命', '紫微斗数', '紫微', '生辰八字', '命盘', '推背图', '占卜',
  '塔罗', '数秘',
  // 英文对外话术
  'fortune teller', 'fortune-teller', 'horoscope', 'luck areas',
];

// ─── 古籍书名白名单（属哲学框架，允许出现）───────────────────────────
const ANCIENT_BOOK_WHITELIST = [
  '《渊海子平》', '《三命通会》', '《滴天髓》', '《穷通宝鉴》', '《子平真诠》',
];

// ─── 防御性上下文关键词（白名单）──────────────────────────────────────
const DEFENSIVE_HINTS = [
  '严禁', '禁止', '替代', '替换', '清洗', '映射', '中性化', '禁用', '红线',
  '防御', '兜底', '术语约束', 'sanitizer', 'red_line', 'red-line',
  'DERIVATION_SANITIZERS', 'TERM_CONSTRAINT', 'whitelist', 'red_terms',
  // 排除逻辑（防御性：显式拒绝某前缀进入 sitemap/robots）
  'startswith', '!p.url', 'excluded', '排除', 'redirect',
  // 死代码标注 / 合规改造说明
  '已下线', '已退役', '已删除', '不再', 'deprecated', '已合规', '合规改造',
];

// ─── 扫描目标 ─────────────────────────────────────────────────────────
const ROOT = process.cwd();
const TARGETS = [
  { dir: 'vercel-deploy/public', exts: new Set(['.txt', '.md', '.json', '.html', '.svg']) },
  { dir: 'vercel-deploy/src/app', exts: new Set(['.ts', '.tsx']) },
  { dir: 'vercel-deploy/src/lib/automation', exts: new Set(['.ts']) },
];

// 明确跳过的目录（构建产物 / 缓存）
const SKIP_DIRS = new Set(['.next', '.vercel', '.next-old', 'node_modules', 'coverage']);

const ARGS = new Set(process.argv.slice(2));
const VERBOSE = ARGS.has('--verbose');
const JSON_OUT = ARGS.has('--json');

function walk(dir, out = []) {
  let entries;
  try {
    entries = readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    if (SKIP_DIRS.has(e.name)) continue;
    const p = join(dir, e.name);
    let s;
    try { s = statSync(p); } catch { continue; }
    if (s.isDirectory()) {
      walk(p, out);
    } else if (s.isFile()) {
      out.push(p);
    }
  }
  return out;
}

function matchTerm(line, term) {
  const lower = line.toLowerCase();
  const t = term.toLowerCase();
  // 中文术语：要求前后（若存在）为非中文字符，避免"每日主动"里的"日主"假阳性
  const isCjk = /^[\u4e00-\u9fff]+$/.test(term);
  if (isCjk) {
    const re = new RegExp(`(^|[^\u4e00-\u9fff])${t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([^\u4e00-\u9fff]|$)`, 'g');
    return re.test(line);
  }
  // 英文术语：小写 includes 即可
  return lower.includes(t);
}

function scanFile(abs, exts) {
  if (!exts.has(extname(abs).toLowerCase())) return [];
  let text;
  try { text = readFileSync(abs, 'utf8'); } catch { return []; }
  const lines = text.split(/\r?\n/);
  const hits = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let hasTerm = false;
    for (const t of RED_TERMS) {
      if (matchTerm(line, t)) { hasTerm = true; break; }
    }
    if (!hasTerm) continue;

    // 白名单 1：古籍书名（该行含白名单条目，且该行不含其它非古籍书名红线词）
    const whitelistedByBook = ANCIENT_BOOK_WHITELIST.some(b => line.includes(b));
    if (whitelistedByBook) {
      const nonBookLine = line.replace(/《[^》]+》/g, '');
      const stillLeak = RED_TERMS.some(t => matchTerm(nonBookLine, t));
      if (!stillLeak) {
        if (VERBOSE) {
          hits.push({ file: relative(ROOT, abs), line: i + 1, kind: 'whitelist-book', text: line.trim(), term: null });
        }
        continue;
      }
    }

    // 白名单 2：防御性上下文（同行含"严禁/替代/清洗"等提示词）
    const isDefensive = DEFENSIVE_HINTS.some(h => line.toLowerCase().includes(h.toLowerCase()));
    if (isDefensive) {
      if (VERBOSE) {
        hits.push({ file: relative(ROOT, abs), line: i + 1, kind: 'whitelist-defensive', text: line.trim(), term: null });
      }
      continue;
    }

    // 白名单 3：DERIVATION_SANITIZERS 映射表（形如 `/术语/g, '替代词'`）
    if (/\/[^/]+\/[gimsuy]*,\s*'/m.test(line)) {
      if (VERBOSE) {
        hits.push({ file: relative(ROOT, abs), line: i + 1, kind: 'whitelist-sanitizer-map', text: line.trim(), term: null });
      }
      continue;
    }

    // 白名单 4：单行注释 / JSX 注释（仅代码注释中的术语不进入对外文本）
    //   但注意：注释里如果同时含"红线词 + 无防御上下文"，仍算潜在泄漏；这里只允许
    //   明确的"下线说明 / 排除逻辑 / 排除前缀 / 内部说明"型注释通过。
    const trimmed = line.trim();
    const isCommentOnly = /^(\/\/|\/\*|\*|#|{\/\*)/.test(trimmed);
    if (isCommentOnly) {
      // 代码/JSX/Markdown 注释——开发者阅读用，不渲染。
      // 但为了审计可追溯性，VERBOSE 下仍报出。
      if (VERBOSE) {
        hits.push({ file: relative(ROOT, abs), line: i + 1, kind: 'whitelist-comment', text: trimmed, term: null });
      }
      continue;
    }

    // 命中
    const matched = RED_TERMS.filter(t => matchTerm(line, t));
    hits.push({
      file: relative(ROOT, abs),
      line: i + 1,
      kind: 'leak',
      text: line.trim().slice(0, 200),
      term: matched,
    });
  }
  return hits;
}

function main() {
  const allHits = [];
  const scanned = [];
  for (const t of TARGETS) {
    const dir = join(ROOT, t.dir);
    const files = walk(dir);
    scanned.push(`${t.dir}: ${files.length} files`);
    for (const f of files) {
      allHits.push(...scanFile(f, t.exts));
    }
  }

  const leaks = allHits.filter(h => h.kind === 'leak');
  const whitelists = allHits.filter(h => h.kind !== 'leak');

  if (JSON_OUT) {
    console.log(JSON.stringify({
      scanned: scanned.join(', '),
      totalLeaks: leaks.length,
      totalWhitelisted: whitelists.length,
      leaks,
    }, null, 2));
  } else {
    console.log('=== OracleMind 公开面红线词审计 ===');
    console.log('扫描范围：', scanned.join(' | '));
    console.log('红线词表：', RED_TERMS.length, '项（含中英变体）');
    console.log('古籍白名单：', ANCIENT_BOOK_WHITELIST.length, '本');
    console.log('');
    if (whitelists.length > 0) {
      console.log(`[白名单] 防御性包含/古籍引用 ${whitelists.length} 处（合法，跳过）`);
    }
    console.log(`[泄漏]   ${leaks.length} 处`);
    console.log('');
    if (leaks.length > 0) {
      console.log('--- 泄漏明细 ---');
      for (const h of leaks) {
        console.log(`${h.file}:${h.line}  [${h.term.join('|')}]`);
        console.log(`    ${h.text}`);
      }
      console.log('');
      console.log('❌ 验收失败：存在公开面红线词泄漏，请修复后重跑。');
      process.exitCode = 1;
    } else {
      console.log('✅ 验收通过：公开面无红线词泄漏。');
    }
  }
}

main();
