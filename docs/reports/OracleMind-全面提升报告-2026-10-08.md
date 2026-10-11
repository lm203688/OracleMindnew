# OracleMind 全面扫描 · 核心目标对标 · 国际竞品与技术趋势 · 全面提升报告

> 生成日期：2026-10-08
> 扫描范围：`C:\Users\xing\Desktop\oraclemind` 全仓（源码 `vercel-deploy/`、古籍、语料、情报、专利、工作记忆）+ **生产 live 实测**（oraclemind.cc command-center / 16 个页面探测）
> 方法：实地读码 + 生产端点取证 + 国际市场与技术文献检索。所有数字标注来源与时点，不做印象判断。
> 立场：不附和。项目里有真东西，也有真错配；下面会把两者都点名。

---

## 〇、执行摘要（Verdict）

**一句话：工程完成度（约 72%）远高于商业验证完成度（约 15%）；项目最硬的资产——事件回测 Brier 0.136 / 方向准确率 83.3%——既没有产品化、也没有对外展示、更没有变现，而对外主打的却是不可验证的"AI-Powered Life Forecasts"，正撞进 $56.9 亿的红海。**

三个必须立刻纠正的结构性错配：

| # | 错配 | 证据 | 后果 |
|---|---|---|---|
| **1** | **旗舰放错了轨**：最强证据在事件轨，营销门面在个人轨 | 生产 `historical-backtest`：54 条已解决事件，avgBrier=**0.136**，方向准确率=**0.833**（politics 1.00 / tech 0.933 / policy 0.80）；而首页 `<title>` = "AI-Powered Life Forecasts"，个人轨 20 预测 / 仅 9 验证 | 与 Co-Star / Nebula / CHANI 在红海正面竞争，放弃了自己唯一能自证的差异化 |
| **2** | **自举死锁**：自动化心跳依赖站点流量，而站点没有流量 | 首页注入 localStorage 6h 节流心跳触发 `/api/automation/self-heal`；生产 `self-heal` = **critical（>26h 停摆）**；`rate-limiting` loop：24h 内 **0 次预测** | 越没人来 → 自动化越停 → 产品越不动 → 越没人来。这是设计层面死锁，不是配置问题 |
| **3** | **信任资产缺失**：唯一能救转化的证据页不存在 | `/accuracy` `/track` `/record` 全部 **404**；无前端埋点（grep 全仓 0 命中 analytics）；187 free / **0 paying** | 预测类产品在没证明自己准之前，付费是反直觉的。转化漏斗底部是空的 |

**综合成熟度判定：**

| 维度 | 完成度 | 判据 |
|---|---|---|
| 工程与功能完成度 | **72%** | 37 个引擎模块、22 个自动化模块、40+ 调度 mode、16 个页面全绿、i18n 四语、OracleCore 四子系统 |
| 科学严谨度完成度 | **50%** | 校准 Scorecard 已建（Brier/BSS/ECE/可靠性分解/方向准确率），但 n=9、CI 宽 0.35、ECE=0.250 显著偏差 |
| 商业验证完成度 | **15%** | 187 free / 0 paying / 0 trial；支付链路未确认通电；无转化数据 |
| 自动化自持完成度 | **55%** | 8 条 cron + maxDuration 已配 + 心跳设计；但 self-heal critical、0 insight、daily-forecast 0 条 |
| **整体可交付成熟度** | **≈ 55%** | 一个"技术上相当完整、商业上尚未通电"的产品 |

---

## 一、核心目标对标：目标 vs 现实

项目自我定位（来自 `ORACLEMIND_MANIFESTO.md` / `PRODUCT_PLAN.md` / `MEMORY.md`）：
> **虚拟实验室（Virtual Laboratory）——融合中国古代哲学框架与现代数据科学的多维概率场推演引擎。**
> 三大原则：**Automation First / Precision Over Hype / Monetization as Validation**。

逐条对标：

| 核心目标 | 现实状态 | 判定 |
|---|---|---|
| **虚拟实验室**：用户可感知的"我在做实验" | ❌ 无"我的第 N 次实验 / 我的准确率"面板；无公开实验记录页；`/accuracy` 404 | **未达成**。实验室是内部概念，用户侧不可见 |
| **Precision Over Hype**：可验证、有据可查 | 🟡 后端有真证据（54 事件 Brier 0.136，6 门引擎审计全过 @ 10-07）；**前端零展示** | **半达成**。精度做出来了，但没被展示，等于不存在 |
| **Automation First**：不需要人参与 | 🟡 40+ mode、8 条 cron、心跳、自愈设计齐全；但 self-heal critical 停摆 >26h、`intel-adopt` 仍 **0 insight**、daily-forecast **0 条** | **半达成**。调度存在，心跳死了 |
| **Monetization as Validation**：付费即验证 | ❌ 187 free / **0 paying** / 0 trial / 0 active | **未达成**。这是三大原则里唯一完全没通电的一条 |
| **古代框架 × 现代数据科学**双轨 | 🟢 5 本古籍 txt 全部就位（渊海子平/子平真诠/三命通会/滴天髓/穷通宝鉴）+ 5 个古籍 Agent（yuanhai/ziping/sanming/ditianzhui/qiongtong）+ 10,000 次蒙特卡洛 + 10 Agent 共识 | **达成**。这是真资产，且比多数竞品扎实 |

**最刺眼的一条**：`Monetization as Validation` 是项目自己定的原则，而它是三条里唯一零分的。按项目自己的标准，目前这个项目**不算验证过**。

---

## 二、全景扫描：资产清单（2026-10-08 实测）

### 2.1 引擎与算法层

| 资产 | 状态 |
|---|---|
| 推演引擎 | `prediction-engine.ts`：倾向场（古典）70% + 统计蒙特卡洛 + 多 Agent 共识 30% |
| 引擎模块数 | **37 个**（`src/lib/engines/`）：tendency-field / calibration / self-consistency / circuit-breaker / react-reasoner / causal-reasoning / mirror-engine / agent-mesh / pipeline / inference-loop / event-corpus / event-outcome-ledger / historical-backtest… |
| OracleCore（GOAI 获奖思想落地） | 4 子系统：镜像概率场 / DataFlow 算子流水线 / Agent Mesh / CyberGuard 安全层 + `/oracle-core` 交互页 |
| 古籍 substrate | 5 本 txt 全部就位 + 5 个专属 Agent + `classical-knowledge-rag.ts` + `classical-llm-enhancer.ts` |
| 安全层 | zod 零信任校验（`guard-core.ts`）+ `withApiGuard` 包装 + 结构化审计日志 + 统一安全响应头 |
| LLM 接入 | `z-ai-web-dev-sdk`（GLM），带模板降级 fallback，支持 L4/L5 多 Agent 辩论 |

### 2.2 自动化与运维层

| 资产 | 状态 |
|---|---|
| 调度入口 | `/api/automation/run`（**40+ mode**）：overnight / engine-audit / historical-backtest / arena-score / lab-experiment / intel-adopt / feedback-adopt / event-corpus-grow / classics-ocr-auto / graph-auto-enrich / competitor-intel / trend-signal… |
| Cron | `vercel.json` **8 条**（01:00 overnight / 01:30 auto-fix / 02:00 engine-audit / 03:00 feedback-harvest / 04:00 lab-experiment / 05:00 historical-backtest / 06:00 arena-score / 07:00 retention） |
| 函数超时 | `maxDuration` **已配置**（run/self-heal/supervisor = 60s，tech-radar = 30s）——8-19 报告点名的 P0 已修复 ✅ |
| GitHub Actions | 5 套 workflow（daily / weekly / monthly / deploy / ci） |
| 自动化模块 | **22 个**（`src/lib/automation/`）：self-heal / self-heal-supervisor / job-ledger / engine-audit / historical-backtest / arena / tech-radar-ledger / seo-factory / tuivan-seo… |
| 心跳设计 | 前端 localStorage 6h 节流触发 `/api/automation/self-heal`（流量驱动兜底） |

### 2.3 产品与前端

| 资产 | 状态 |
|---|---|
| 页面（实测 200） | `/` `/arena` `/journal` `/loop` `/oracle-core` `/daily-forecast` `/quality-evolution` `/pricing` `/profile` `/widget` `/resonance` `/visual-resonance` `/self-eval` `/preview` `/domains` `/share/[id]` —— **16 个全绿** |
| 缺失页面（实测 404） | `/accuracy` `/track` `/record` `/forecast` `/markets` `/leaderboard` —— **公开战绩页全缺** |
| 三层产品 | L1 Quick（免登录）/ L2 Personal（+生辰）/ L3 Deep（8+ Agent，10 维交叉验证） |
| 定价 | Free（5 次/天 + 1 次 deep）/ Premium $9.99 月 / Deep $4.99 单次 / Credits 30=$4.99、100=$14.99 |
| 分享飞轮 | Resonance Card（9:16 可截图卡）+ Visual Resonance（图片能量场，**端侧计算，照片不出浏览器**）+ `/share/[id]` |
| i18n | en / ja / ko / zh 四语（`messages/`） |
| PWA | `manifest.json` + `sw.js` + icons |
| 埋点 | ❌ **完全没有**（grep `vercel/analytics\|posthog\|gtag\|umami\|plausible` = 0 命中） |

### 2.4 生态与开放性

| 资产 | 状态 |
|---|---|
| MCP Server | `/api/mcp` ✅ |
| OpenAPI | `/api/openapi.json` ✅ |
| A2A Agent Card | `/.well-known/agent.json` ✅（符合 2026 Agent 协议栈） |
| Embed Widget | `/widget` + `/embed.js` ✅ |
| LLM 发现面 | `/llms.txt`（14 篇 GEO 文章）+ sitemap 88 条 + IndexNow |
| 公开 API | `/api/public/field`（CORS 开放） |
| 开发者文档页 | ❌ 无 |
| 计费/API Key | ❌ 无（全部免鉴权） |

### 2.5 商业化与合规

| 资产 | 状态 |
|---|---|
| 支付 | PayPal（5 SKU + IPN endpoint）+ Creem（`creemApiKey` / `creemWebhookSecret` 已配 ✅） |
| 付费用户 | **0**（187 free / 0 premium / 0 deep / 0 trial） |
| 系统健康 | 7/7 全绿（DB / Creem×2 / PayPal / GLM / DB URL / NextAuth） |
| 合规 | 占卜/塔罗/数秘域已退役（307 重定向）；全站免责声明；`audit-public-terms.mjs` 红线巡检脚本 |
| 已知合规泄漏 | ⚠️ `/tuivan/*` 中文页含天干词（9-10 报告 P0，疑似未修，需复查） |
| 专利 | `patent-backup/` 13 份（DMTL 3 轮迭代 + 5 张附图 + 实质审查请求书） |

### 2.6 生产实测关键数字（2026-10-08 00:32 UTC）

| Loop | 状态 | 数字 |
|---|---|---|
| prediction-accuracy | healthy | 20 预测 / **9 验证** / Brier 0.159 / BSS +0.034 / accuracyRate 0.84 |
| ├ Scorecard 细分 | — | n=9, Brier **0.2147**, CI95 [0.076, 0.427], baseline 0.2222, **BSS +0.034**, **ECE 0.250**, 判定「与基线持平，校准偏差显著」 |
| historical-backtest | healthy | **54 条已解决事件，avgBrier 0.136，方向准确率 0.833** ✅ 最强资产 |
| ├ 分域 | — | politics 0.095(1.00) / policy 0.092(0.80) / crypto 0.122(0.714) / tech 0.140(0.933) / economics 0.174(0.667) / science 0.220(0.60) |
| payment | ⚠️ warning | 187 free / **0 paying** |
| agent-experience | healthy | 217 条（**0 insight** / 12 correction / 205 pattern） |
| self-heal | 🔴 **critical** | **>26h 停摆**——外部 cron 与流量心跳双路皆失 |
| daily-forecast | info | **0 条**（注册用户专享功能从未被调用） |
| simulation | info | 68 总计 / 24h 内 0 / **eventCount = 0** |
| event-outcome | info | **事件账本为空**——事件轨尚无真实用户预测入库 |
| engine-audit | healthy | 6 门全过 @ 10-07 02:11，15 fixtures / 54 events，lastGood `04e96f6` |
| system-health | healthy | 7/7 |
| 系统总状态 | 🔴 **critical** | 15 loops：7 healthy / 1 warning / 1 critical / 2 alerts |

---

## 三、完成度评分矩阵（分板块）

评分为实地取证后的判断，非自评。权重按"对北极星指标（周活跃付费用户 WAU-paid）的贡献"设定。

| # | 板块 | 完成度 | 权重 | 关键证据 | 短板 |
|---|---|---|---|---|---|
| 1 | 推演引擎内核 | **85%** | 12% | 确定性、非退化（std 0.148）、10 Agent 共识、10,000 蒙特卡洛、6 门审计全过 | 引擎不消费 AgentExperience（N4 未接线） |
| 2 | 古典 substrate | **80%** | 8% | 5 本 txt 齐、5 个古籍 Agent、RAG + LLM 增强、classics-audit 探针 | KB 仍为 `.ts` 非可版本化 JSON；OCR 自动化待验 |
| 3 | 事件预测轨（后端） | **70%** | 15% | 54 事件回测 Brier 0.136 / 方向 0.833、Manifold 锚定、EventOutcomeLedger、arena-score | **产品面 0 使用**（eventCount 0、账本空） |
| 4 | 个人推演轨 | **60%** | 10% | 倾向场映射 + 三层产品 + 分享卡 | 无 outcome、无回访验证、不可 claim 准度 |
| 5 | 校准与验证科学 | **45%** | 12% | Scorecard（Brier/BSS/ECE/可靠性/分辨率/不确定性/方向准确率）已建，是专业级设计 | **n=9**，CI 宽 0.35，ECE 0.250 显著偏差，统计上无法区分随机 |
| 6 | 前端产品体验 | **70%** | 10% | 16 页全绿、三层、i18n 四语、PWA、分享卡、端侧视觉共振 | **无埋点**、无战绩页、streak 仅 localStorage、无社交图谱 |
| 7 | 增长与获客 | **55%** | 12% | llms.txt 14 篇、sitemap 88、MCP/A2A/OpenAPI/Widget 全齐、IndexNow | 无流量闭环、无埋点、无社交飞轮、无 A/B、GEO 面红线泄漏 |
| 8 | 商业化与支付 | **40%** | 15% | 5 SKU、PayPal+Creem 双通道、7/7 健康 | **0 付费**、IPN 未确认、无战绩页、无开发者计费 |
| 9 | 自动化运维 | **65%** | 8% | 40+ mode、8 cron、maxDuration 已配、幂等账本、自愈设计 | **self-heal critical**、0 insight 死循环、daily-forecast 0 条 |
| 10 | 数据与壁垒 | **30%** | 10% | 54 事件回测是正确种子 | 9 verified、0 用户 outcome、0 第三方接入、数据集未版本化披露 |
| 11 | 工程与测试 | **65%** | 6% | TS 严格、ESLint、Jest、21/21 新测试通过 | 4 个伪集成测试套件 **32 个失败**（localhost 依赖）、CI 覆盖薄 |
| 12 | 合规与安全 | **75%** | 8% | 占卜域退役、zod 校验、CyberGuard、安全头、审计日志 | `/tuivan` 天干词泄漏待复查；无 GDPR/数据导出闭环验证（有 `/api/export-data`） |
| 13 | 国际化与本地化 | **65%** | 5% | en/ja/ko/zh | 中文流量 vs PayPal-only 收单错配；无本地支付 |
| 14 | 生态开放性 | **60%** | 7% | MCP + A2A + OpenAPI + Widget + public field | 无文档页、无 API Key/计费、0 第三方接入 |

**加权综合：功能/工程维度 ≈ 72%，验证/商业维度 ≈ 15%，整体 ≈ 55%。**

---

## 四、国际竞品与市场需求对标

### 4.1 市场规模（2026 实测数据）

| 市场 | 规模 | 增速 |
|---|---|---|
| 占星/灵性 App（全球） | **$56.9 亿（2026）** → $117.1 亿（2030） | **CAGR 19.8%** |
| — 2024 / 2025 回溯 | $39.4 亿 → $47.5 亿 | CAGR ~20.5% |
| 印度市场 | $1.63 亿（2024）→ $17.97 亿（2030） | **CAGR 49.19%**（全球最快） |
| AI Wellness 平台 | $34.2 亿（2025） | 高增长 |
| Wellness App（广义） | $128.7 亿（2025） | ~9-15% |
| API-as-a-Service | $84.6 亿（2026）→ $163.3 亿 | ~18% |
| 头部 App 累计下载 | **1.8 亿+**；MAU **1.2 亿+** | — |
| 印度 astrotech 融资 | $5,000 万（2024），2015 年仅 $8.8 万 | 爆发式 |

> 判读：赛道足够大且在高速增长，**需求侧不是问题**。问题在 OracleMind 的位置选在了竞争最激烈、且自己最不可自证的那一格。

### 4.2 竞品对标矩阵

| 竞品 | 定位 | 规模/收入 | 变现模型 | 对 OracleMind 的启示 |
|---|---|---|---|---|
| **Co-Star** | 极简设计 + 毒舌推送 + 好友星盘对比 | 2026-07 **被 Midjourney 收购**；490 万 MAU；月下载 20 万；分成后月流水 **$40-50 万**；IAP $3/$5/$7/$9 | **80%+ 收入来自一次性好奇**（加他人星盘、情侣分析、AI 问答包） | ①零买量 + 社交裂变可行（近 90 天广告创意数 0）②**一次性付费 > 订阅**——OracleMind 的 Deep $4.99 方向正确 ③但也暴露：一次性付费撑不起增长曲线 |
| **Nebula**（OBRIO） | 订阅 + 1:1 真人解读 | **3,000 万用户，$5,000 万 ARR（2023）**，当年 +250% | 订阅 + 真人 readings | **混合模式（AI + 真人）才是变现天花板最高的**。OracleMind 全自动化是成本优势，不是变现优势 |
| **CHANI** | 深度内容 + 订阅 | 200 万+ 下载，非 VC | 订阅为主 | **赛道变现第一名**——说明"深度 + 持续关系"比"流量"更值钱 |
| **Sanctuary** | 真人 1:1 文字解读 | 700 万+ 用户，$650 万融资 | 真人 readings | 人工咨询溢价高 |
| **The Pattern** | 心理/关系深度解读 | 350 万+ 用户 | Freemium 订阅 | 人格化叙事 > 占星术本身 |
| **Astrotalk**（印度） | 1:1 咨询平台 | **6,000 万注册用户，15,000 占星师，月 450 万付费会话**，月收入 ₹70 crore，目标 $1.2 亿 ARR | 按次咨询 ₹99-₹1,999 | 印度 CAGR 49% 的引擎是**真人咨询**，不是 AI |
| **测测星座**（中国） | 社区 + 咨询 | 赛道变现 Top2 | 社区 + 付费 | 中文市场付费意愿真实存在 |

**竞品给出的三条硬结论：**

1. **纯 AI 自动解读变现天花板低**：Co-Star 是流量之王（490 万 MAU）却是变现老三。Nebula / CHANI / Astrotalk 的共性都是**"AI 打底 + 人/深度关系增值"**。
2. **一次性付费是主流，订阅是补充**：Co-Star 80%+ 收入来自一次性。OracleMind 把 Premium $9.99 订阅置于 Deep $4.99 之前（首页 Premium 标 "Most Popular"），**与赛道实证相反**。
3. **零买量可行，但前提是社交裂变载体**：Co-Star 靠"每日一句毒舌推送 + 好友对比"实现 0 广告创意。OracleMind 有分享卡但无每日推送钩子、无好友对比、无 streak 服务端化。

### 4.3 预测/ forecasting 侧对标（这才是 OracleMind 该打的战场）

| 对象 | 准度基准（Brier） | 备注 |
|---|---|---|
| 朴素基线率 | 0.25（二元下限） | 任何正经模型应显著低于此 |
| 超级预测员（Tetlock/GJP） | 0.18–0.22 | 人类天花板 |
| 预测市场（Polymarket/Kalshi） | 0.14–0.16 | 近实时聚合 |
| LLM/AI 检索增强预测（2025-26） | 0.16–0.18 | AI 已具竞争力 |
| — 经济/系统数据类 | AI 0.12 vs 市场 0.11 | **AI 几乎追平** |
| ForecastBench（Karger et al.） | AI 0.111 vs 超预 0.093 | AI 仍落后，且**裸新闻接入无显著改善** |
| **OracleMind historical-backtest（实测）** | **0.136 / 方向 0.833** | ✅ **落在预测市场区间，优于超级预测员基准** |

> **这是全项目最有价值的一行数字。** 在国际公认标尺上，OracleMind 的事件轨已跑进"预测市场级"区间。但它：① 没有对外展示 ② 没有对应产品入口 ③ 样本 54 条（统计功效仍弱）④ 无时间戳封存（无法对抗事后叙事）。

### 4.4 2026 技术趋势与可用杠杆

| 趋势（2026） | 现状 | OracleMind 可抓的杠杆 |
|---|---|---|
| **LLM 预测智能体综述**（arXiv 2608.23058, 2026-08） | 将架构分三类：独立 LLM 工作流 / 检索+工具增强 / 混合统计模型；明确指出**核心局限是"测量"**：需 distribution shift 下的校准、**抗污染的活体评测（contamination-resistant live evaluation）**、成本与精度联合披露 | **直接对应护城河设计**：做"前瞻性注册 + 时间戳封存 + 公开记分板"，这是学术界公认缺失、而项目天然能做的（已有 JobRun 账本 / historical-backtest） |
| **Agent 协议栈**（MCP 月下载 9,700 万 / A2A / AG-UI） | 2026 = "Agent 协议之年" | 项目已有 MCP + A2A Agent Card + OpenAPI ✅ → **补 AG-UI + 完整开发者门户 + API Key 计费**，即可从"工具"升级为"可被 Agent 调用的概率场服务" |
| **GEO / AEO（生成式引擎优化）** | 2026 国内 AI 搜索用户 **8.2 亿**，内容可见性从"搜索排名"演变为"算法采信" | 已有 llms.txt + 14 篇 GEO + MCP → **扩产至 50+ 篇、覆盖 event-forecasting / decision-intelligence 长尾，并清除红线词** |
| **RevenueCat 2026 订阅报告** | AI 应用**年留存仅 21%**，trial→paid 转化高但年留存低 30% | 印证：**首购用 $4.99 一次性**（低门槛），**留存靠"持续更新的事件追踪"而非订阅权益堆砌** |
| **端侧/隐私计算** | 用户对数据外传敏感 | Visual Resonance 已做到"照片不出浏览器" ✅ → 应把这条作为**品牌信任主张**放大（隐私差异化，竞品无） |

---

## 五、差距根因诊断（五个断裂点）

```
① 证据 → 产品        断裂：54 事件 Brier 0.136 在数据库里，不在页面上
② 流量 → 自动化      断裂：心跳靠流量，流量靠产品，产品靠自动化（死锁）
③ 用户 → 反馈        断裂：无埋点 + 无一键回报 → 校准永远饥饿（n=9）
④ 采纳 → 消费        断裂：217 条经验、0 insight，主引擎不读 AgentExperience
⑤ 能力 → 收入        断裂：MCP/A2A/OpenAPI/Widget 全免鉴权，0 计费
```

**① 证据→产品断裂（最严重）**
`historical-backtest` 跑出 Brier 0.136 / 方向 0.833，这是能打动用户、媒体、B 端客户的唯一硬证据。但 `/accuracy` 是 404，首页无一处提及。相当于造了一台能跑进 3 秒的引擎，却在车展上只展示车内音响。

**② 自举死锁（最隐蔽）**
前端心跳注释写得明白：cron 或 GH Actions 任一失效时靠访问者触发补跑。但生产 24h 内 0 次预测 → 心跳无人触发 → `self-heal` 停摆 26h → 系统 critical。**解决方案不是"再多加一条 cron"，而是把心跳迁到不依赖自身流量的外部探针**（见 P0-2）。

**③ 反馈饥饿（最基础）**
n=9 的 Brier 0.2147，CI95 = [0.076, 0.427]，跨过基线 0.2222。**在统计上这个项目目前无法宣称自己比随机准。** 而个人轨 20 预测 / 9 验证，用户 simulation 68 次 / 24h 内 0。没有埋点，连"用户在第几步流失"都看不见。

**④ 采纳假闭环（最浪费）**
217 条 AgentExperience，其中 **0 条 insight**（8-19 报告已点名，至今未修）。`intel-adopt` 生产无产出 + 主引擎不消费经验库 = 两条主线的"采纳"是写库自嗨。

**⑤ 变现未接线（最直接）**
MCP / A2A / OpenAPI / Widget / public field 五条嫁接通道全部免鉴权、无计费、无文档。这五条是 2026 年 Agent 生态里最容易产生 B 端收入的接口，现在全在裸奔。

---

## 六、分板块提升建议

### 6.1 事件预测轨（最高优先级，P0）

**目标：把 Brier 0.136 从数据库搬到首页，并让样本自己长大。**

| 动作 | 说明 | 验收 |
|---|---|---|
| **E1 公开战绩页 `/accuracy`** | 展示 54 条已解决事件的 Brier / 方向准确率 / 分域表现 / 与基线 0.25 和超级预测员 0.18-0.22 的对比条；**每条事件列出：问题、注册时间、封存概率、结局、Brier** | 页面 200 + 首页二级 CTA + 数据每日自动刷新 |
| **E2 前瞻性注册（Pre-registration）** | 事件预测入库即写 `registeredAt` + `probabilityHash`（不可篡改封存），结局回来再解封 | 可对抗"事后叙事"指控，是学术界都稀缺的能力 |
| **E3 语料自动扩产 54 → 300+** | 已有 `event-corpus-grow` mode；接入 Manifold + Metaculus + Kalshi + Polymarket 已结算市场，按域均衡采样 | n≥300，CI95 宽度 < 0.10 |
| **E4 事件产品化：公开事件板** | 建 `/markets` 或 `/events`：列出正在进行中的事件及其当前概率，用户可订阅/追踪 | 用户事件预测数 > 0（当前 eventCount=0） |
| **E5 分域差异化** | science 域 Brier 0.220 / 方向 0.60 明显拖后腿 → 降权或单独校准；politics/policy/tech 是优势域，加大权重 | 分域 Brier 均有披露 |

### 6.2 校准与验证科学（P0）

**目标：从"统计上无法区分随机"走到"可宣称优于基线"。**

| 动作 | 说明 | 验收 |
|---|---|---|
| **C1 校准修正** | ECE = 0.250（显著偏差），BSS 仅 +0.034。用现有 9 条 + 扩产后的事件样本重做 reliability 修正（Platt scaling / isotonic regression 已在 calibration.ts 有基础） | ECE < 0.10，BSS > 0.10 |
| **C2 样本量冲刺** | 个人轨靠用户回报（慢），事件轨靠自动结算（快）。**把所有验证资源压到事件轨** | 90 天内 verified ≥ 200 |
| **C3 置信上限诚实化** | 当前 `recommendedConfidenceCap` 机制已存在；须在前端结果页显式展示置信区间而非单点 | 结果页显示区间 |
| **C4 一键回报（1-tap）** | 结果页加"准/部分准/不准"三档，写入 PredictionFeedback | 月回报数 > 50 |

### 6.3 产品定位与前端体验（P0/P1）

**目标：把门面从"AI-Powered Life Forecasts"换成"可验证的概率场实验室"。**

| 动作 | 优先级 | 说明 |
|---|---|---|
| **P1 首页叙事重构** | P0 | 主标题从 "AI-Powered Life Forecasts" → **"A forecasting lab that publishes its score"**（战绩前置）。第一屏就放 Brier 0.136 / 方向 83.3% + "54 resolved events, published" |
| **P2 实验室仪表盘** | P0 | "我的实验 N 次 / 我的验证 M 条 / 我的 Brier"——把"虚拟实验室"从概念变成用户可感知的东西 |
| **P3 埋点** | P0 | 接 Vercel Analytics（零成本）→ 最少覆盖：首屏曝光 / 提问提交 / 结果渲染 / 升级点击 / 支付发起 / 支付完成。**没有这个，所有优化都是盲猜** |
| **P4 付费墙时机** | P0 | 免费给"倾向指数 + 一句话"，在**用户最想要的瞬间**（想看完整解读）弹出 $4.99 Deep —— 而非首页堆订阅 |
| **P5 订阅与一次性换位** | P1 | 对标 Co-Star（80%+ 收入来自一次性）：把 **Deep $4.99 设为默认推荐**，Premium 订阅降为次选 |
| **P6 streak 服务端化** | P1 | 当前 localStorage（换设备即丢）。加 `streak` 列 + 每日推送钩子 |
| **P7 每日一推（Co-Star 式）** | P1 | 一天一条、断言式、可截图。Co-Star 已验证这是零成本裂变引擎，而 `daily-forecast` 表 **0 条**——现成的能力完全没用上 |
| **P8 好友/对比维度** | P2 | Resonance Pairing 已有 `/resonance/pair`；补"好友对比 + 可分享匹配卡"，这是 Co-Star 社交飞轮的核心 |
| **P9 移动端** | P1 | 有 PWA manifest + sw.js，但无安装引导、无推送。移动端是占星赛道主战场 |

### 6.4 商业化（P0/P1）

| 动作 | 优先级 | 说明 |
|---|---|---|
| **B1 支付链路通电确认** | P0 | PayPal 后台 IPN 开关 + Creem 状态核验 + `$4.99` 端到端真实下单自测（不是测试款，是真实可复现路径）。**0 paying 无法区分"没人买"还是"买了没开通"** |
| **B2 战绩页 = 转化页** | P0 | E1 与 B1 组合：信任 → 转化。这是最高杠杆的一对动作 |
| **B3 API 计费** | P1 | MCP / OpenAPI / public field 加 API Key + 按次计费（$0.01-0.05/次 或 $29/月 起）。2026 Agent 生态最容易收钱的口子，现在裸奔 |
| **B4 开发者门户** | P1 | `/docs` 或 `/developers`：快速开始 + 示例 + Widget 嵌入码 + 定价。**没有文档 = 没有第三方接入** |
| **B5 中文流量收单** | P1 | sitemap 88 条大半是中文 `/tuivan/*`，却只有 PayPal。要么接国内支付（类目须中性），要么把中文流量导向"事件预测"中性面 |
| **B6 混合模式（AI + 人）** | P2 | 对标 Nebula $50M ARR / Astrotalk 月 450 万会话：Deep 报告可选"专家复核"加价档。全自动化是成本优势，但变现天花板在混合 |
| **B7 免费额度收紧** | P2 | 5 次/天偏松，无稀缺感 → 无升级触发 |

### 6.5 自动化运维（P0）

| 动作 | 优先级 | 说明 |
|---|---|---|
| **A1 打破自举死锁** | P0 | 心跳**不能依赖自身流量**。接入外部免费探针（UptimeRobot / GitHub Actions schedule / cron-job.org）每 6h 打一次 `/api/automation/self-heal`。同时把 `self-heal` / `self-heal-supervisor` 补进 `vercel.json` cron（当前 8 条 cron 里**没有 self-heal**） |
| **A2 调度心跳哨兵** | P0 | 8-19 报告 N1 项至今未见落地：读 JobRun 账本，任一链 >36h 未跑 → 自动重放 + 告警。**监控者必须被监控** |
| **A3 修 intel-adopt 死循环** | P1 | 217 条经验 / **0 insight**。改为从 Manifold/Metaculus 已结算市场 + 近期 resolved 事件取信号，而非泛话题 web-scrape |
| **A4 接线采纳消费** | P1 | 主 `PredictionEngine.predict()` 推理前注入近 7 天高置信经验，并 `useCount+1`。否则 M3/M4 是死库 |
| **A5 修 32 个失败测试** | P1 | 4 个套件伪集成（localhost 依赖）→ 重构为 handler 级单测。**CI 是绿的，但 32 个测试在红**，这是工程债 |
| **A6 daily-forecast 通电** | P1 | 表 0 条 = 功能从未被调用。要么前端接线、要么下线（不留僵尸功能） |

### 6.6 数据壁垒与生态（P1/P2）

| 动作 | 说明 |
|---|---|
| **D1 数据集版本化披露** | 事件语料 + 回测结果按版本发布（含 hash），可被引擎/Agent 引用 → 这是唯一可持续的护城河 |
| **D2 协议栈补齐** | 已有 MCP + A2A + OpenAPI → 补 AG-UI，形成完整 2026 Agent 协议栈；`.well-known/agent.json` 内容扩到完整能力声明 |
| **D3 抗污染活体评测** | 呼应 arXiv 2608.23058 的核心批评：公开一条**持续更新的活体记分板**（只统计注册时点之后的事件），这是学术界公认缺失的能力，也是媒体/研究圈最愿意引用的东西 |
| **D4 GEO 扩产 + 清红线** | 14 篇 → 50+ 篇，覆盖 event-forecasting / decision-intelligence / probabilistic-forecasting 长尾；**同步清除 `/tuivan/*` 与 llms.txt 的天干词泄漏** |
| **D5 隐私差异化放大** | Visual Resonance"照片不出浏览器"是竞品没有的信任主张 → 提到首页、写进 GEO、写进 Agent Card |

### 6.7 合规（P0）

- `/tuivan/*` 中文页天干词泄漏（9-10 报告 P0）**复查是否修复**；`llms.txt` 条目名须中性化。
- 首页已有免责声明 ✅，但**战绩页一旦上线，所有准度表述必须带样本量与置信区间**，否则从"合规"变成"虚假宣传"。

---

## 七、分阶段路线图

### P0 — 通电（0–30 天）：让钱能收进来、让证据被看见、让自动化真正跑起来

| # | 动作 | 负责 | 验收标准 |
|---|---|---|---|
| 1 | 支付链路端到端自测（PayPal IPN + Creem + 权限开通） | 需你操作后台 | 真实下单 → 权限自动开通，可复现 |
| 2 | 上线 `/accuracy` 公开战绩页（54 事件 Brier/方向/分域 + 与基线对比） | 自动执行 | 页面 200，首页二级 CTA |
| 3 | 打破自举死锁：外部探针 + self-heal 进 cron | 自动执行 | `self-heal` loop 从 critical → healthy，连续 7 天 |
| 4 | 前端埋点（Vercel Analytics，零成本） | 自动执行 | 6 个关键事件有数据 |
| 5 | 首页叙事重构：战绩前置，"lab that publishes its score" | 自动执行 | 首屏出现 Brier 数字 |
| 6 | `/tuivan` 红线复查 + llms.txt 中性化 | 自动执行 | `audit-public-terms.mjs` 0 命中 |
| 7 | 付费墙时机：Deep $4.99 设为默认推荐 | 自动执行 | 结果页升级触发点上线 |

**P0 的意义：这 7 件事不做完，后面所有"提升"都是在给一个没通电的系统刷漆。**

### P1 — 长大（30–90 天）：让样本自己长大、让 API 开始收钱

| # | 动作 | 验收 |
|---|---|---|
| 8 | 事件语料 54 → 300+（Manifold/Metaculus/Kalshi/Polymarket 自动扩产） | n≥300，CI95 宽度 < 0.10 |
| 9 | 校准修正（ECE < 0.10，BSS > 0.10） | Scorecard 达标 |
| 10 | 前瞻性注册 + 概率 hash 封存 | 每条事件可验证不可篡改 |
| 11 | 事件产品化 `/events`：进行中事件板 + 追踪 | 用户事件预测 > 0 |
| 12 | API Key + 按次计费（MCP/OpenAPI/public field） | 首笔 API 收入 |
| 13 | 开发者门户 `/docs` | 第三方可自助接入 |
| 14 | 修 intel-adopt（0 insight → 有产出）+ 主引擎消费接线（useCount > 0） | 217 条经验被真实消费 |
| 15 | 每日一推 + streak 服务端化 | daily-forecast 表 > 0，DAU 提升 |
| 16 | 修 32 个失败测试 | CI 全绿且真实覆盖 |
| 17 | GEO 扩产 14 → 50 篇 | 长尾覆盖 |

### P2 — 加固（90–180 天）：壁垒、混合模式、规模化

| # | 动作 |
|---|---|
| 18 | 数据集版本化 + 公开发布（护城河） |
| 19 | 抗污染活体记分板（学术/媒体引用入口） |
| 20 | AG-UI 补齐协议栈 |
| 21 | 混合模式：Deep + 专家复核加价档 |
| 22 | 好友对比 + 可分享匹配卡（社交飞轮） |
| 23 | 移动端 PWA 安装引导 + 推送 |
| 24 | 中文流量收单方案落地（或流量重定向到中性面） |
| 25 | B 端：事件预测订阅（研究/媒体/投研） |

---

## 八、北极星指标与验收

**北极星：周活跃付费用户（WAU-paid）。** 在 0 付费之前，用下列先行指标替代：

| 阶段 | 先行指标 | 当前 | 30 天目标 | 90 天目标 |
|---|---|---|---|---|
| 信任 | 公开已验证事件数 | 54（仅后端） | 54（公开） | 300+ |
| 信任 | Brier / BSS / ECE | 0.136 / +0.034(n=9) / 0.250 | 0.15 / >0.05 / <0.15 | <0.15 / >0.10 / <0.10 |
| 活跃 | 周活跃用户 | ~0（24h 预测 0） | 有埋点后定基线 | +200% |
| 反馈 | 月回报数 | 0 | 50 | 300 |
| 转化 | 付费用户 | **0** | **≥1（真实端到端）** | ≥25 |
| 收入 | MRR | $0 | 首笔 | $300+ |
| 生态 | 第三方 API 调用方 | 0 | 1 | 10 |

---

## 九、风险提示（不粉饰）

1. **统计风险**：当前 n=9，Brier CI95 [0.076, 0.427] 跨过基线。**在样本扩到 100+ 之前，任何形式的对外准度宣称都不成立**，且可能反噬合规。这条必须写进红线。
2. **死锁风险**：自动化依赖自身流量，天然在低流量期失效。P0-3 是唯一解。
3. **竞争风险**：占星赛道 $56.9 亿但集中度高，Co-Star 已被 Midjourney 收编（资源量级碾压）。**在"AI 生活预测"这一格硬碰没有胜算**；唯一胜算在"可验证"这一格——目前无人占领。
4. **合规风险**：战绩页上线 = 从"娱乐声明"走向"性能声明"，须同步升级免责与表述规范；`/tuivan` 天干泄漏若未修，同时威胁支付通道与品牌。
5. **工程风险**：CI 显示绿但 32 个测试在红，自动化链无冒烟测试——存在"账本显示 success 实则静默失败"的已知模式。
6. **单点风险**：PayPal 为唯一已通收单通道（Creem 密钥已配但未验证）；建议同步保留第二通道。

---

## 十、结论（不附和）

1. **这个项目不是"缺功能"**。37 个引擎模块、54 事件回测 Brier 0.136、40+ 自动化 mode、MCP/A2A/OpenAPI 全齐——功能密度已经超过绝大多数同阶段产品。继续堆功能是负收益。

2. **它缺的是三件小事和一个大转向**：
   - 三件小事：支付通电、战绩页上线、心跳脱离流量依赖。
   - 一个大转向：**把旗舰从"个人生活预测"换到"可验证的事件预测"**。前者是 $56.9 亿红海且不可自证；后者是项目唯一跑进预测市场区间（Brier 0.136 vs 市场 0.14-0.16）的赛道，且无人占领。

3. **按项目自己的标准（Monetization as Validation），它目前不算验证过。** P0 的 7 件事做完，才算第一次真正通电。

4. **做完 P0+P1，项目的形态应该是**：一个公开记分板的概率场实验室——首页挂着 Brier 曲线和 300+ 已解决事件，用户来追踪事件、看自己的实验记录、买 $4.99 的深度解读，开发者的 Agent 通过 MCP 付费调用它的概率场。这与今天的"AI-Powered Life Forecasts"是两个物种，而前者才有护城河。

---

*本报告全部生产数字取自 2026-10-08 00:32 UTC 对 oraclemind.cc 的 live 实测与源码实地审计；市场与技术数据取自 2026 年公开报告与文献（已在正文标注来源）。*
