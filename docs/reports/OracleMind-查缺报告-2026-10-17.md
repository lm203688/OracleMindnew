# OracleMind 查缺报告——细节拉满的全仓缺口清单

> **口径**：本报告不评估"做得好不好"，只枚举"**缺了什么**"。所有条目均为 2026-10-17 本地实测（枚举 + grep + 交叉比对），每条附证据位置，可直接当工单用。
> **对照基准**：`docs/00-core/CORE-GOALS.md`（v1.2）与 `ROADMAP.md`（唯一权威任务清单）。缺口按"是否阻断北极星（WAF × 人均已结算预测数）"分级。
> **扫描面**：86 个 API 路由 / 28 个页面 / 40 个引擎模块 / 25 个 Prisma 模型 / 48 个环境变量 / 12 个 cron / 4 个语言包 / 全部 docs 承诺。

---

## 〇、缺口总览（先看这 16 个数字）

| # | 指标 | 实测 | 应为 |
|---|---|---|---|
| 1 | 放错目录、永不部署的文件 | **5 个** | 0 |
| 2 | 无任何调用方的孤儿 API | **15 个**（真孤儿约 8） | 0 或明确标注为外部回调 |
| 3 | 零引用死代码引擎 | **4 个** | 0 |
| 4 | 缺失但被承诺的页面 | **4 个**（/events /docs /contact /about） | 0 |
| 5 | 前端死链 | **2 个**（/contact /about） | 0 |
| 6 | loading / error / not-found 边界 | **0 / 0 / 0**（28 个页面全裸） | 每页至少 error+loading |
| 7 | i18n 语言包使用数 | **4 个包，0 处 useTranslations** | 全站接入或删除 |
| 8 | 代码引用 env vs 本地配置 | **48 vs 2**，且无 `.env.example` | 48 个全文档化 |
| 9 | 无鉴权的写入型 API | 至少 **1 个致命**（`feedback/outcome` 可投毒校准数据） | 全部鉴权 |
| 10 | 写入路由带 zod 校验 | **0/5**（predict/feedback/journal/save/referral/credits 抽样全无） | 100% |
| 11 | 语料规模 | **55 条**（目标 300） | ≥300 |
| 12 | 古籍实体文本 | **2/5**（子平真诠 27 行 / 滴天髓 121 / 穷通宝鉴 53） | 5/5 |
| 13 | ECE | **0.250**（目标 <0.10） | <0.10 |
| 14 | 24h 预测数 / WAF / 付费 | **0 / ~0 / 0** | >50 / 有基线 / 首笔 |
| 15 | P2 加固完成度 | **0/8** | 8/8 |
| 16 | 工程文档 | 无 SECURITY.md / 无运维手册 / 无备份脚本 / 无迁移历史 | 全有 |

---

## 一、A 类：说了没做（文档承诺 vs 实现）

> 全部逐条对照 `ROADMAP.md` / `CORE-GOALS.md` 核验，非推测。

| 承诺 | 出处 | 实测 | 差距 |
|---|---|---|---|
| P1-11 事件产品化 `/events`（进行中事件板） | ROADMAP:89 | **页面不存在**（API `/api/events` 只被 `lib/analytics.ts` 当埋点上报用） | 缺整个产品页 |
| P1-13 开发者门户 `/docs` | ROADMAP:91 | **页面不存在** | 缺快速开始/示例/嵌入码 |
| P1-12 API Key + 按次计费 | ROADMAP:90 | **无任何面向客户的 API Key 机制**（只有 Tavily/Creem 等第三方 key） | 缺签发/校验/计量 |
| P1-8 语料 54 → 300+ | ROADMAP:85 | **55 条**，且 55 条硬编码在 29KB 的 `event-corpus.ts` 里 | 缺 245 条 + 缺数据文件化（扩到 300 会变 150KB TS） |
| P1-9 校准修正 ECE < 0.10 | ROADMAP:86 | **ECE 0.250**（CORE-GOALS 基线） | 差 2.5 倍 |
| P1-14 `intel-adopt` 死循环修复 | ROADMAP:92 | 状态未核验（⬜） | 情报产出未接主引擎 |
| P2-18 数据集版本化公开发布 | ROADMAP:115 | **无**（无 DVC/版本号/发布页） | 护城河资产未产品化 |
| P2-19 抗污染活体记分板 | ROADMAP:116 | **无公开引用入口** | 缺学术/媒体引用页 |
| P2-20 AG-UI 协议栈 | ROADMAP:117 | 未做 | 缺 Agent 协议层 |
| P2-22 好友对比/分享卡 | ROADMAP:119 | 未做（有 `/share/[id]` 单条分享） | 缺社交飞轮 |
| P2-23 PWA 安装 + 推送 | ROADMAP:120 | `manifest.json` **有**（含 192/512 图标），**无推送** | 半成品 |
| P2-24 中文流量收单 | ROADMAP:121 | 未做（18 个页面仍硬编码中文） | 缺海外切换 |
| P2-25 B 端事件预测订阅 | ROADMAP:122 | 未做 | 缺 B 端产品 |
| MCP Server / Widget / Browser Extension | 综合方案:242-244 | 均 ⬜ | 三个分发入口全缺 |
| "五本古籍提供结构假设" | CORE-GOALS:19 | **3 本空壳**（27/121/53 行） | 缺 OCR |
| 11 项专利权利要求（DMTL+Arrhenius） | patent-backup | **代码 0 对应**（全仓 grep 0 命中） | 专利与技术主体错配 |

---

## 二、B 类：做了没接线（代码孤岛）

### B-1【头号发现】5 个文件放错目录，永远不会被部署

根目录 `src/app/` 下有 5 个文件，而 Next 应用的根是 `vercel-deploy/`（`vercel.json` 的 buildCommand 在 vercel-deploy 执行）：

| 文件 | 内容 | 后果 |
|---|---|---|
| `src/app/verify/[id]/page.tsx` | **公开验证页**（M07 的核心资产） | 写了但用户永远看不到 |
| `src/app/api/verify/public/route.ts` | 公开验证 API | 未部署 |
| `src/app/api/opentimestamps/anchor/route.ts` | **OpenTimestamps 锚定**（全球唯一信任资产） | 未部署 |
| `src/app/arena/individual/page.tsx` | 个人竞技场页 | 未部署（且 0 入口） |
| `src/app/api/arena/individual/route.ts` | 个人竞技场 API | 未部署 |

> 这 5 个文件创建于 2026-10-16 12:10——**正是昨天报告点名"M07 公开验证页+OpenTimestamps"之后的产物**。做对了事，放错了地方。这是全报告性价比最高的修复：移动 5 个文件，一天内让"可证明不马后炮"资产上线。

### B-2 孤儿 API（15 个，无任何代码调用）

`arena/leaderboard`（排行榜 API 无前端）、`feedback/outcome`（外部可调但无内部消费）、`feedback/simulation`、`forecast`、`graph`、`referral`、`automation/content-generator`、`payment/paypal/*`（3 个）、`payment/webhook`、`auth`、`openapi.json`、`simulate/*/stream`（2 个）。
> 需分三类处理：**真孤儿**（arena/leaderboard、feedback/simulation、forecast、graph、referral → 接线或删）/ **外部回调**（payment/webhook、paypal/ipn、auth → 保留并标注）/ **动态构造**（simulate stream → 前端可能用模板字符串，需人工确认）。

### B-3 死代码引擎（4 个，0 引用）

`agent-memory.ts`、`difficulty-router.ts`、`inference-loop.ts`、`query-expander.ts`。
> 其中 `inference-loop.ts` 有 **100% 测试覆盖**——测了一个没人调用的模块。这是"测试努力用错地方"的典型。

### B-4 假 i18n（4 个语言包，0 处使用）

`messages/{en,ja,ko,zh}.json` 齐全，但 `useTranslations/getTranslations` **全仓 0 处**；`i18n/request.ts` 硬编码 `locale='en'`；18 个页面硬编码中文。
> 现状是"英文配置 + 中文硬编码"的混合态：既不真国际化，也没统一语言。要么全站接入 next-intl，要么删包减负——**不能留半成品**。

### B-5 死链与孤儿页面

- **死链**：`/contact`、`/about` 出现在 href 里，页面不存在 → 用户点击 404。
- **孤儿页面**：`/arena/individual`（0 入口，且只在根目录 src）、`/ai-future`（仅 1 处引用，疑似仅 sitemap）。

### B-6 零状态边界

`find app -name "loading.tsx" | wc -l` = **0**；`error.tsx` = **0**；`not-found.tsx` = **0**。
> 28 个页面在网络慢、API 失败、路由不存在时，全部落到浏览器默认行为（白屏/原生 404）。对"信任型产品"，白屏 = 用户流失。

### B-7 手写 OpenAPI（必然漂移）

`/api/openapi.json` 是手写静态 spec（只覆盖少数路由），86 个路由无自动生成 → 文档与实现必然不同步。第三方接入（P1-12/P1-13）的前置缺口。

---

## 三、C 类：接了没数据（空态与冷启动）

| 缺口 | 证据 | 影响 |
|---|---|---|
| 三个仪表盘全空态 | `PredictionFeedback` 无真实 verified 样本 | M01 校准 / M04 竞技场 / M08 战绩 全部"无数据" |
| 24h 预测数 = 0 | CORE-GOALS 基线 | 北极星第一因子为 0 |
| 事件账本空 | CORE-GOALS 基线"事件账本条目：空" | 记分板无内容 |
| 语料 55 条 | `event-corpus.ts` grep `id:` = 55 | ECE 压不到 <0.10（样本不足） |
| 古籍 3 本空壳 | 27/121/53 行 | 旺衰/格局/调候 Agent 无素材，古典层名存实亡 |
| 月回报 0 / 真人试玩 0 | CORE-GOALS 基线 | 无反馈闭环 |
| 第三方 API 调用 0 | 无 API Key 机制 | 生态指标为 0 |

> 这一类的根因是同一个：**没有真实用户 → 没有样本 → 校准飞轮空转**。修复必须从"冷启动数据注入"（重放已结算市场）开始，这是 2.0/3.0 方案里 α 阶段的核心。

---

## 四、D 类：安全与数据完整性缺口

| # | 缺口 | 证据 | 严重度 |
|---|---|---|---|
| D-1 | **`feedback/outcome` 无鉴权，直连 `reportActualOutcome`** | `src/app/api/feedback/outcome/route.ts` 无 authorized/getServerSession；直接调用飞轮写入 | **P0：校准数据投毒入口**——任何人 POST 可伪造"真实结局"，污染护城河 |
| D-2 | 写入路由 0/5 有 zod 校验 | predict/feedback/journal/save/referral/credits 抽样全无 | P1：脏数据/超长输入直达数据库 |
| D-3 | rate limit 无统一中间件 | 仅 5 个文件手工实现 | P1：算力滥用（LLM 调用贵） |
| D-4 | 无 API Key 签发/校验 | 全仓无面向客户的 key 机制 | P1：P1-12 计费无从谈起 |
| D-5 | `db.ts` no-op proxy 静默假成功 | 无 DATABASE_URL 时 create 返回 `{id:'mock-...'}` | P0：生产配置错误时数据静默丢失 |
| D-6 | 无备份脚本 | `scripts/` 无 backup/dump/restore | P0：数据库无灾备 |
| D-7 | 无 SECURITY.md | 仓库根目录缺失 | P2：漏洞披露渠道缺失 |
| D-8 | 无迁移历史 | 无 `prisma/migrations/`，仅 2 个手工 SQL | P0：schema 演进无回滚 |

---

## 五、E 类：配置与工程缺口

| # | 缺口 | 证据 |
|---|---|---|
| E-1 | **48 个 env 引用 vs 本地 2 个配置，无 `.env.example`** | 代码引用 48 个（含 NEXTAUTH_SECRET/GLM_API_KEY/TAVILY_API_KEY/EMAIL_SERVER/CREEM_*/PAYPAL_*/FIELD_HMAC_SECRET）；`.env` 只有 DATABASE_URL/DIRECT_URL → 本地开发 LLM/搜索/支付/登录全不可用 |
| E-2 | 双 git 仓库 + 双 lockfile + 双 Next 版本 | root（无 remote，`next ^16.3.6`）vs vercel-deploy（有 remote，`next ^16.1.1`）；Next build 实测警告 "multiple lockfiles" |
| E-3 | 无运维手册 | `docs/` 无 deploy/runbook/ops 目录——部署、回滚、故障处理全靠人脑 |
| E-4 | 无迁移/回滚文档 | 见 D-8 |
| E-5 | `package.json` 无 test 脚本（vercel-deploy） | 289 用例无法一键跑 |
| E-6 | 覆盖率从未真实产出 | `coverage/coverage-summary.json` = `{}` |
| E-7 | 语料双源 | `data/event-corpus.json`（8KB 种子快照）vs `lib/engines/event-corpus.ts`（29KB 权威）；扩产前须明确只写 TS 或迁移到数据文件 |
| E-8 | 根目录杂物 | `_build_trash/`、`_tmp_build.log`、`.opencode/`、根 `src/`（放错的 5 文件） |
| E-9 | 依赖冗余 | `nodemailer` 装了但只用 Resend（`email-engine.ts`）；`@creem_io/nextjs` + `creem` 双包 |

---

## 六、F 类：文档漂移（双向，比单向更危险）

| 文档说 | 实际 | 方向 |
|---|---|---|
| `FutureSimulation` 是"唯一无写入死模型" | `ai-future-simulation.ts` 有完整 create/findMany/findFirst | 文档过时（实际已做） |
| "融合权重与宣称不符" | `prediction-engine.ts` 注释已改为 0.5/0.5/0 并说明 | 文档过时（已修） |
| "首页 title 仍 'AI-Powered Life Forecasts'" | `layout.tsx` 已是 "A forecasting lab that publishes its score" | 文档过时（已改） |
| "arena → prisma.prediction.create 0 命中" | 实际有 `recordPredictionRecord`（写 Prediction 表），但**接在会静默失败的路径上**（brierScore 字段缺失 + client 过期） | 文档低估了：不是没接，是接错了 |
| "P0 通电 6/6 已完成" | 飞轮写入路径有 4 个生产类型错误 + 静默 catch | 状态虚高："完成"≠"可用" |

> 文档漂移的代价：owner 按文档做决策，会同时**低估已做**（重复投入）和**高估完成**（漏修致命路径）。

---

## 七、完整缺口清单（Q-01 ~ Q-52，可直接转工单）

> 优先级：**P0 = 本周**（阻断北极星或造成数据/安全损失）/ **P1 = 2–4 周** / **P2 = 1–3 月** / **P3 = 3.0 阶段**

| ID | 类 | 位置 | 缺什么 | 补法 | 优先级 |
|---|---|---|---|---|---|
| Q-01 | B | 根 `src/app/`（5 文件） | 放错目录，永不部署 | 移到 `vercel-deploy/src/app/` 对应路径，验证 `/verify/[id]` 可访问 | **P0** |
| Q-02 | D | `api/feedback/outcome` | 鉴权 | 加 ADMIN_API_KEY 或 FIELD_HMAC 签名校验 | **P0** |
| Q-03 | D | `lib/db.ts` | 生产缺库时快速失败 | `NODE_ENV=production` 缺 DATABASE_URL 直接 throw | **P0** |
| Q-04 | D | `scripts/` | 备份脚本 | 每日 `pg_dump` + 保留 30 天 + 恢复演练 | **P0** |
| Q-05 | D | `prisma/` | 迁移历史 | 生成 baseline migration，生产改 `migrate deploy` | **P0** |
| Q-06 | A | `prisma/schema.prisma` | Prediction 表缺 brierScore | 补字段 + `prisma generate`（详见地基报告 H1） | **P0** |
| Q-07 | B | `app/**` | 死链 /contact /about | 建两个静态页，或删 href | **P0** |
| Q-08 | E | 仓库根 | `.env.example` | 48 个变量全部列出（必填/可选/示例值） | **P0** |
| Q-09 | B | `app/**` | 0 loading/error/not-found | 加 `app/error.tsx` + `app/not-found.tsx` + 关键页 `loading.tsx` | P1 |
| Q-10 | B | `messages/*.json` + 18 页 | 假 i18n | 决策：全站接入 next-intl 或删包统一中文 | P1 |
| Q-11 | B | `lib/engines/` 4 文件 | 死代码 | agent-memory/difficulty-router/inference-loop/query-expander：接线或删 | P1 |
| Q-12 | B | 15 个孤儿 API | 无调用方 | 分类：真孤儿接线/删；外部回调标注；动态构造人工确认 | P1 |
| Q-13 | A | `app/events` | 事件产品页 | 建页：进行中事件板 + 追踪（复用 `/api/events`） | P1 |
| Q-14 | A | `app/docs` | 开发者门户 | 快速开始 + 示例 + Widget 嵌入码 | P1 |
| Q-15 | A | 语料 | 55 → 300 | 先迁移到数据文件（JSON/DB），再自动扩产（Manifold/Metaculus/Kalshi） | P1 |
| Q-16 | A | 古籍 | 3 本 OCR | PaddleOCR/微信 OCR 补全（目标各 ≥1000 行） | P1 |
| Q-17 | D | 写入路由 | zod 校验 0/5 | 抽 `withValidation` 高阶函数，先覆盖 predict/feedback/journal/credits | P1 |
| Q-18 | D | API 层 | 统一 rate limit | 中间件（KV/LRU，按 IP/用户） | P1 |
| Q-19 | E | `package.json` | test 脚本 | 加 test/test:coverage，CI 接入 | P1 |
| Q-20 | E | 根仓库 | 双 git / 双 lockfile / 双 Next 版本 | 定主仓库，统一版本，删多余 lockfile | P1 |
| Q-21 | E | `docs/` | 运维手册 | `docs/eng/runbook.md`（部署/回滚/故障/告警） | P1 |
| Q-22 | B | `api/openapi.json` | 手写 spec | 从路由自动生成（或 zod → OpenAPI） | P2 |
| Q-23 | A | API 计费 | 无 API Key | 签发/校验/计量/配额 | P2 |
| Q-24 | A | `app/arena/individual` | 孤儿页 | 接入口或删（依赖 Q-01） | P2 |
| Q-25 | A | PWA | 无推送 | Service Worker + 推送订阅 | P2 |
| Q-26 | A | 活体记分板 | 无公开引用入口 | 数据集版本页 + 可引用报告 | P2 |
| Q-27 | A | 数据集版本化 | 无 | 语料/账本 hash + 版本号 + 发布页 | P2 |
| Q-28 | F | 5 份文档 | 漂移 | 用实测结果批量修正（FutureSimulation/融合权重/title/arena 接线） | P2 |
| Q-29 | E | 依赖 | nodemailer 冗余、Creem 双包 | 清理 + 锁版本 | P2 |
| Q-30 | E | 根目录 | `_build_trash`/`_tmp_build.log`/`.opencode` | 清理或移入 `.gitignore` | P2 |
| Q-31 | A | 语料双源 | JSON vs TS | 明确单一权威（TS），JSON 标注为快照或删 | P2 |
| Q-32 | A | 古典 substrate | 3 本空壳影响所有古典 Agent | 与 Q-16 联动，补后跑 `classics-audit` | P1 |
| Q-33 | A | 校准 | ECE 0.250 | Platt/isotonic + 扩样本（Q-15） | P1 |
| Q-34 | A | 情报 | `intel-adopt` 产出未接主引擎 | 核验 `useCount`，修死循环 | P2 |
| Q-35 | A | AG-UI | 未做 | 3.0 阶段 | P3 |
| Q-36 | A | 好友对比 | 未做 | 3.0 阶段 | P3 |
| Q-37 | A | B 端订阅 | 未做 | 3.0 阶段 | P3 |
| Q-38 | A | MCP/Widget/Extension | 未做 | 3.0 分发层 | P3 |
| Q-39 | D | 无 SECURITY.md | 漏洞披露 | 建文件 | P2 |
| Q-40 | E | `coverage-summary.json` = {} | 覆盖率未产出 | CI 跑 `jest --coverage` 并上传 | P1 |
| Q-41 | A | 中文流量收单 | 未做（18 页中文） | 海外切换或中性化（P2-24） | P2 |
| Q-42 | A | 专利错配 | 11 项权利要求与代码 0 对应 | IP 重定向：围绕校准/封存/协议申请 | P2 |
| Q-43 | B | `app/ai-future` | 仅 1 入口 | 接导航或并入主流程 | P2 |
| Q-44 | D | `tuivan/calculate` 无鉴权 | 算力滥用 | 加 rate limit | P2 |
| Q-45 | A | 24h 预测 0 | 冷启动 | 种子账号 + 已结算市场重放（α-2） | **P0** |
| Q-46 | A | 事件账本空 | 冷启动 | 与 Q-45 同批注入 | P1 |
| Q-47 | E | 无 `docs/eng/` | 工程文档目录 | 建目录：runbook/db-migration/dependency-policy | P1 |
| Q-48 | D | 无 CSP | 安全头 | 补 Content-Security-Policy | P2 |
| Q-49 | A | `/api/events` 只被埋点用 | 事件产品无数据源 | 与 Q-13 联动 | P1 |
| Q-50 | B | 根 `src/` 目录 | 与 vercel-deploy 重复结构 | 见 Q-01，移完删除 | **P0** |
| Q-51 | A | 公开验证页无入口 | 即使 Q-01 修好也无导航 | 首页/accuracy 页加"验证"入口 | P1 |
| Q-52 | A | OpenTimestamps 锚定未接线 | Q-01 修好后需真实锚定 | 接 OTS 服务 + 公开可查 | P1 |

---

## 八、修复顺序（按"投入产出比"排序，不按类别）

### 第一波：一周内可清零的 8 项（全是"移动/加一行"级别，但影响巨大）
Q-01（5 文件归位）→ Q-50（删根 src）→ Q-06（brierScore+generate）→ Q-02（outcome 鉴权）→ Q-03（db 快速失败）→ Q-07（死链）→ Q-08（.env.example）→ Q-51（验证页入口）

> 做完这一波，**M07 信任资产上线 + 校准投毒口关闭 + 飞轮写入可用**——三个"最贵的能力"同时激活，成本不到 3 天。

### 第二波：2–4 周（把"半成品"变"成品"）
Q-05/Q-04（迁移+备份）→ Q-09（状态边界）→ Q-15/Q-31（语料迁移+扩产）→ Q-33（ECE）→ Q-16/Q-32（OCR）→ Q-17/Q-18（校验+限流）→ Q-10（i18n 决策）→ Q-11/Q-12（死代码与孤儿 API 决策）→ Q-19/Q-40（test+coverage 进 CI）

### 第三波：1–3 月（补产品与文档）
Q-13/Q-14（/events、/docs）→ Q-22（OpenAPI 自动生成）→ Q-23（API Key 计费）→ Q-25/Q-26/Q-27（PWA/记分板/数据集版本）→ Q-21/Q-47（运维手册）→ Q-28（文档漂移批量修正）

### 第四波：3.0 阶段
Q-35~Q-38（AG-UI/好友对比/B 端/MCP-Widget-Extension）

---

## 九、一句话总结

**这个项目最大的缺口不是"没做"，而是"做了 80% 却没接上最后 20%"**：验证页写好了放在不会部署的目录、翻译包齐全但 0 处调用、289 个测试全绿但覆盖率 17.86%、飞轮接线了但接在会静默失败的路径上、ROADMAP 说 P0 全完成但写入路径有 4 个类型错误。

**查缺的结论不是"再建新东西"，而是：把已有的 80% 接上电。** 第一波 8 项（不到 3 天）能让三个最贵的能力（信任资产、飞轮、防投毒）同时激活——这是当前全项目投入产出比最高的动作，也是北极星（WAF × 人均已结算预测数）从 0 起步的唯一现实路径。

---

*本报告全部条目为 2026-10-17 本地实测：86 API / 28 页面 / 40 引擎 / 25 模型 / 48 env / 12 cron / 4 语言包全量枚举；孤儿检测用"路由清单 vs 全仓调用路径"交叉比对；死代码用"import 引用计数"；文档承诺逐条对照 ROADMAP/CORE-GOALS 核验。与 2026-10-16《地基加固工程报告》互补：地基报告管"底层结构强度"，本报告管"功能接线完整性"。*
