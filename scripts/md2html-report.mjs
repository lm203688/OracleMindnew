import fs from 'node:fs';
import { marked } from 'marked';

const src = process.argv[2];
const out = process.argv[3];
let md = fs.readFileSync(src, 'utf8');

// Strip the leading H1 + blockquote meta into a hero header
const lines = md.split('\n');
const title = lines[0].replace(/^#\s*/, '').trim();

const body = marked.parse(md, { gfm: true, breaks: false });

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<style>
  :root{
    --bg:#f7f8fa; --panel:#ffffff; --ink:#1a1f2b; --ink2:#4a5262; --ink3:#7b8494;
    --line:#e4e7ec; --accent:#1f6feb; --accent2:#0b8a5f; --red:#d92d20; --amber:#b54708;
    --code-bg:#f2f4f7; --quote-bg:#f8fafc;
  }
  *{box-sizing:border-box}
  body{
    margin:0; background:var(--bg); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    line-height:1.75; font-size:15.5px; -webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:980px; margin:0 auto; padding:0 28px 96px;}
  header.hero{
    background:linear-gradient(135deg,#0f1b33 0%,#1b3a6b 55%,#1f6feb 100%);
    color:#fff; margin:0 0 40px; padding:52px 28px 44px; border-bottom:4px solid #0b8a5f;
  }
  header.hero .inner{max-width:980px; margin:0 auto;}
  header.hero h1{font-size:30px; line-height:1.35; margin:0 0 14px; font-weight:700; letter-spacing:.3px;}
  header.hero .sub{font-size:14px; opacity:.82; line-height:1.7;}
  header.hero .badges{margin-top:20px; display:flex; flex-wrap:wrap; gap:8px;}
  header.hero .badge{background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.25);
    padding:4px 12px; border-radius:999px; font-size:12.5px; letter-spacing:.2px;}
  h1{font-size:26px; margin:44px 0 16px; padding-bottom:10px; border-bottom:2px solid var(--line);}
  h2{font-size:22px; margin:44px 0 16px; padding:10px 0 10px 14px; border-left:5px solid var(--accent);
     background:linear-gradient(90deg,rgba(31,111,235,.06),transparent);}
  h3{font-size:18px; margin:30px 0 12px; color:var(--ink);}
  h4{font-size:16px; margin:22px 0 10px; color:var(--ink2);}
  p{margin:12px 0;}
  a{color:var(--accent); text-decoration:none;} a:hover{text-decoration:underline;}
  strong{color:#0f1729; font-weight:650;}
  hr{border:none; border-top:1px solid var(--line); margin:40px 0;}
  blockquote{
    margin:16px 0; padding:14px 20px; background:var(--quote-bg);
    border-left:4px solid #94a3b8; border-radius:0 8px 8px 0; color:var(--ink2);
  }
  blockquote p{margin:6px 0;}
  code{background:var(--code-bg); padding:2px 6px; border-radius:5px;
    font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace; font-size:13px; color:#b02a37;}
  pre{background:#0f172a; color:#e2e8f0; padding:18px 20px; border-radius:10px; overflow:auto; line-height:1.6;}
  pre code{background:none; color:inherit; padding:0; font-size:12.8px;}
  table{border-collapse:collapse; width:100%; margin:18px 0; font-size:14px; background:var(--panel);
    border-radius:10px; overflow:hidden; box-shadow:0 1px 3px rgba(16,24,40,.06);}
  th,td{border:1px solid var(--line); padding:10px 13px; text-align:left; vertical-align:top;}
  th{background:#f0f3f8; font-weight:650; color:#111827; white-space:nowrap;}
  tr:nth-child(even) td{background:#fafbfc;}
  ul,ol{padding-left:26px; margin:12px 0;}
  li{margin:6px 0;}
  .wrap > h2:first-child{margin-top:8px;}
  @media(max-width:720px){
    .wrap{padding:0 16px 64px;} header.hero{padding:34px 16px;}
    header.hero h1{font-size:23px;} table{font-size:12.5px;} th,td{padding:7px 9px;}
  }
</style>
</head>
<body>
<header class="hero">
  <div class="inner">
    <h1>${title}</h1>
    <div class="sub">全仓扫描 · 核心目标对标 · 国际竞品比较 · 技术壁垒深挖 · 最新技术融合 · 提升方案</div>
    <div class="badges">
      <span class="badge">综合成熟度 ≈ 62%</span>
      <span class="badge">工程 78% · 科学 70%</span>
      <span class="badge">用户/活跃 5% · 商业 15%</span>
      <span class="badge">Brier 0.136 / 方向 83.3%</span>
      <span class="badge">扫描 2026-10-12</span>
    </div>
  </div>
</header>
<div class="wrap">
${body}
</div>
</body>
</html>`;

fs.writeFileSync(out, html, 'utf8');
console.log('OK ->', out, html.length, 'bytes');
