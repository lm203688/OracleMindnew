# OracleMind 战略评估 · 闭环审计 · 线上嫁接方案（2026-08-14）

> 范围：从核心目标 + 三大不可妥协原则出发，评估发展路径；审计全部闭环任务的逻辑漏洞；给出"线上平台嫁接"引流方案；附空间清理结论。
> 方法：实地读码审计（vercel-deploy/src）+ 合规红线比对，非凭记忆。

---

## 一、核心目标与原则（校准基准）

- **核心目标**：多维概率场引擎——融合中国古代哲学框架 + 现代数据科学的自主演进预测平台。**不是星座/命理 App，不是迷信工具。**
- **三大不可妥协原则**：① Automation First ② Precision Over Hype ③ Monetization as Validation（用户付费 = 真实价值）。
- **公开话术红线（MANDATORY）**：禁用「八字/天干/日主/四柱/十神/用神/大运/流年/命理/算命/horoscope/fortune-telling/占卜」。内核 substrate 可保留术语，对外必须中性。

---

## 二、整体战略评估（从目标+原则出发）

### 2.1 发展路径结论（不附和）

**A. 事件推演转向 = 正确，符合全部三原则。**
- Automation First：事件有机器可解析的 ground truth（0/1），可全自动跑"预测→结局→校准"闭环，不依赖人工标注。
- Precision Over Hype：用 Brier 分数可硬量准确率，而非"感觉准"。
- Monetization as Validation：事件预测对 B 端（研究/媒体/投研）有付费意愿，比个人命盘更易合规变现。
- 弥补了最大窟窿：个人推演 0 outcome（无法验证），事件推演产出可验证信号。

**B. 人/事件双轨 = 必须保留，但边界要划清。**
- 人推演 = 品牌叙事层（概率倾向场 / 能量基调），**不赌准确率**（个性情绪不可纯数理，这是事实，不是缺陷）。
- 事件推演 = 准确率 claim 的唯一载体。
- 双轨保住"古代框架 + 现代数据科学"定位，且事件轨合规风险更低。

**C. 🔴 重大战略矛盾（必须修，否则长期目标受损）——见第三节。**

### 2.2 长远目标下的改动优先级

1. **P0（阻断级）**：消除"宣称概率场却卖占卜"的自相矛盾（horoscope 页 + tarot/numerology 付费域）。这是品牌信用 + 支付通道存续的前提。
2. **P0**：把 engine-audit（现代方法验证）接入 command-center 看板，让"可验证"对外可见（已做，本次接线）。
3. **P1**：事件推演 Phase 1——`EventOutcomeLedger` 自动结局回写 + engine-audit 真实准度关（用 data/event-corpus.json 12 条起步，扩到 20–50）。
4. **P1**：线上平台嫁接（见第四节）——把"概率场 API + 可嵌入 widget"挂到第三方平台，零人工发帖即可引流。
5. **P2**：情报补偿（路线 A，已建种子语料）+ 真实用户反馈闭环通电（现 0 outcome，漏斗已就绪只差用户点）。

---

## 三、闭环任务审计（是否走通 / 是否需融合 / 逻辑漏洞）

### 3.1 盘点与状态

| 闭环 | 状态 | 结论 |
|---|---|---|
| PayPal 支付（_xclick+IPN+grant） | 生产 19/19 PASS；IPN 须用户在 PayPal 后台开 | **走通**，但**支付政策风险**见 3.3 |
| GEO 推广（llms.txt + 11 篇 + IndexNow + sitemap） | 19/19 验证 | 走通；但 horoscope 矛盾削弱 LLM 引用一致性 |
| engine-audit overnight（每日 UTC01:00） | 5 关全绿，写 `engine-audit:latest` | 走通；**未接入 command-center（融合缺口）** |
| trial-reclaim（过期试用回收） | 口径已修正（distinguish trialing/expired） | 走通 |
| 反馈闭环（recordPredictionFeedback→calibrate→cap） | 架构闭合：collect→store→calibrate 读 actualOutcome→recommendedConfidenceCap | **架构走通但饥饿**（0 outcome， dormant）；非 bug |
| 事件推演（/api/simulate/event） | 端点存在、记录反馈 | **半成品**：缺 EventOutcomeLedger 自动结局回写 + 真实准度关 |
| lab 自实验（M1–M6） | overnight 串联 classics-audit→lab-experiment→feedback-harvest | 走通；command-center 已监控 lab_fixture 新鲜度 |
| command-center 看板 | 8 大 loop 聚合 | 走通；**缺 engine-audit 第 9 loop** |

### 3.2 真实逻辑漏洞（已修/本次修）

1. **engine-audit 未进 command-center**（融合缺口）→ **本次修复**：新增第 9 loop 读取 `engine-audit:latest`。
2. **historical-backtest 死代码**：仅剩 deprecation 注释，无活跃引用（`grep` 确认）。建议归档（本次清理移入 `scripts/deploy/`，源码保留不动）。
3. **反馈闭环"半闭"**：架构闭合，但 0 outcome 使其休眠。非代码 bug，需用户点击回报解锁——已就绪，只差流量。

### 3.3 🔴 合规/战略矛盾（最高优先级，需你拍板）

**漏洞 A — 西方星座日运页（已上线、已 index）**
- 位置：`src/app/horoscope/daily/[sign]/[date]/page.tsx`，由 `seo-factory.generateDailyHoroscope` 用 LLM 生成"mystical oracle"调性西方星座运势。
- 矛盾：① 对外红线禁用 horoscope 词；② GEO 文章 `beyond-horoscopes.md` 宣称"我们超越星座"，但站点自己发星座运；③ 已被 Google 索引（canonical 含 /horoscope/）。
- 风险：品牌自相矛盾被 LLM/用户抓包；Creem 拒审疑与此相关；SEO 流量是"占卜"人群，与"概率场/决策支持"目标用户错配。
- **本次已做（安全可逆）**：sitemap 移除 horoscope URL + 页面 `robots: noindex`，停止继续索引。**深层修复建议**：整体下线该 feature 或改造成"每日概率场简报（非星座）"。

**漏洞 B — Tarot / Numerology 付费域（走 PayPal）**
- 位置：`/domains` 页 + `/api/divine/[domain]`（tarot 78 张、Pythagorean numerology 作付费解读，消耗 credit→PayPal）。
- **支付政策风险（严重）**：PayPal Acceptable Use Policy 明确禁止 psychic / fortune-telling 类交易。若用户用 PayPal 买 credit 跑塔罗，账户可能被冻。
- 矛盾：与"古代哲学框架 + 现代数据科学"定位不符；tarot/numerology 非该框架。
- **建议（需你审批，因涉收入面）**：保留"classical derivation engine"域，退役 tarot/numerology 从公开/付费面；或至少去 index + 重话术。这是不可逆的产品决策，我准备好一键改造方案待你确认。

---

## 四、线上平台嫁接方案（曝光 + 引流）

约束：你打不开海外站、connector 全断 → 不能靠"发帖"。但 oraclemind.cc 在 Vercel 上、对 LLM/爬虫可达。**嫁接 = 让别的平台主动调用/嵌入我们，而非我们去发帖。**

### 4.1 高杠杆、可自动化、不需你出手

1. **公开 API + 可嵌入 Widget（最契合"嫁接"）**
   - `/api/openapi.json` 已存在 → 补一份开发者文档页 + 一段 `<script>` 嵌入码（任意博客/媒体站可挂"OracleMind 概率场简报"卡片）。
   - 效果：第三方站嵌入 → 回流流量 + 自然外链（SEO/LLM 双收益）。
   - 合规：widget 只暴露"概率场/事件推演"，不暴露 horoscope/tarot（顺带消除矛盾）。

2. **GEO 增强（已有，加固）**
   - 修掉 3.3 矛盾后，LLM 引用一致性↑；再补 2–3 篇"event forecasting / decision intelligence"长尾文。
   - llms.txt 已含 11 篇，保持。

3. **AI 聚合/目录提交（准备素材，API 可提交处我代提交）**
   - Futurepedia / There's An AI For That / Product Hunt / Hacker News Show。
   - 我准备好 listing 文案 + 标签 + 截图；有提交 API 的我来提交，需登录表单的给你清单你点。

4. **MCP Server（AI 平台原生集成）**
   - 把 OracleMind 概率场/事件推演暴露为 MCP tool，AI Agent 平台可直接调用 → "AI 平台嫁接"，零发帖。
   - 契合 Automation First，长期杠杆最高。

### 4.2 不做的（基于原则）

- 社交发帖（你打不开站 + 无 connector，不可行）。
- 虎皮椒/国内支付（放弃，聚焦海外 PayPal 单一闭环）。
- 裸新闻灌入情报（ForecastBench 证非胜点，须结构化策展）。

---

## 五、空间清理（本次执行）

- 根目录 22 个一次性 `push-*.mjs` / `verify-*.mjs` / `vercel-env-*.mjs` 部署/验证脚本 → 移入 `scripts/deploy/`（保留、可逆、仅整理）。
- 删除临时日志 `build-p1-log.txt`。
- 不动：源码、数据、文档、`_archive`、`五本古籍`（含用户资料，禁删）。
- 死代码 `historical-backtest.ts` 保留（仅注释引用），不删源码。

---

## 六、行动清单（本次已做 / 待你）

✅ 已做：engine-audit 接入 command-center；horoscope 停止索引（noindex+sitemap）；根目录脚本整理。
⏸ 待你拍板：① tarot/numerology 付费域退役（PayPal 风险）；② 事件推演 Phase 1 开工；③ 线上嫁接 widget/API 开工；④ PayPal $4.99 测试款确认收款。
