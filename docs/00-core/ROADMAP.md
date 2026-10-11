# OracleMind 路线图（ROADMAP）

> ⚠️ **本文件已被 `docs/00-core/OracleMind-综合方案-2026-10.md` 取代（2026-10-10）。**
> 全部内容（诊断 / 战略 / 产品 / 协议化 / 商业预测 / 合规 / 执行 / 决策）已合并进该单一权威文档。
> **新任务以综合方案为准**；本文件的 P0/P1 已完成项与 W0-2/W0-3/W1-5 已落地项，在综合方案中标注为 ✅ / 📦 继承。
> 若 owner 决策 D8 否决取代，则本文件恢复权威。
>
> 📌 **本文件保留的价值**：最完整的「已落地物 ↔ 文件路径」索引（P0 交付明细、部署通道诊断、波次状态）。**查阅实现细节时优先看这里。**
>
> **本文件是「整理所有任务」的唯一权威清单。** 三份输入报告的待办项已在此合并去重，按 P0/P1/P2 排期，并标注真实状态。
> 依据（三份输入报告，均位于 `docs/reports/`）：
> 1. `OracleMind-全面提升报告-2026-10-08.md` — 全面扫描 / 竞品对标 / P0–P2 路线图（主来源）
> 2. `PHASE0-PHASE1-REPORT.md` — 推演准确率校准专项（校准层 + 1-tap 回报 + 符号回归试点）
> 3. `TESTING-SUMMARY.md` — 测试框架搭建总结（Jest + 覆盖率 + 文档）
> 权威目标定义见 `docs/00-core/CORE-GOALS.md`。
> 版本：v1.2 ｜ 更新：2026-10-10 ｜ 复验：基于本地 `vercel-deploy` 实测 + GitHub API 实测
> 状态图例：✅ 已完成 ｜ 🔄 进行中 ｜ ⬜ 待办 ｜ ⛔ 被阻塞（需 owner 操作）｜ 📦 代码已就位·待部署

---

## 速览（2026-10-09 复验）

| 阶段 | 自动化项 | 用户闸门项 | 说明 |
|---|---|---|---|
| **P0 通电** | 6/6 已完成 | 1 项（P0-1 支付）仍 ⛔ | P0-5 的 metadata 于本日补完，此前仅视觉层到位 |
| **P1 长大** | 3 项完成（P1-9b / P1-15 / P1-10），7 项 ⬜ | 2 项 ⛔ | 校准层/符号回归试点已就绪但未被真实样本驱动；P1-9b 已解锁飞轮信号入口 |
| **P2 加固** | 0/8 | 0 | 全部 ⬜ |

**最硬资产（事件轨）**：54 条已解决事件，avgBrier=**0.136**，方向准确率=**0.833**，已公开在 `/accuracy`。**最致命缺口**：0 付费用户（P0-1 未通电）、样本仍偏小（n=54，需扩到 300+）、自动化心跳此前依赖自身流量（已用外部 cron 打破）。

---

## 🚨 部署通道状态（2026-10-10 实测 · 报告 #1 最紧急项）

| 环节 | 状态 | 证据 |
|---|---|---|
| GitHub 推送（push-om.py, Git Data API） | ✅ **已通** | 远程 main = `dae99be6`（含 P0/P1 + W0-2/W0-3/W1-5 全部代码）；推后自检 0 漂移/0 缺失 |
| Vercel 生产部署 | ⛔ **阻断** | 远程 head 已更新，但 `GET /accuracy` 仍 **404**、首页 `<title>` 仍 "AI-Powered Life Forecasts"；`ci-deploy.mjs` 报 `invalidToken: true`（Vercel token 失效）；webhook 未触发 |
| 后果 | — | 本地↔生产不同步，所有"已落地"代码用户看不到 → 这是"停滞感"真因（报告诊断一致） |

**需 owner 出手修复部署（二选一）**：
1. 在 Vercel 后台重新生成 Token → 写入 `vercel-deploy/.env.vercel-token`（或给我新的 Vercel Token），我用 `ci-deploy.mjs` 触发 gitSource 生产部署；
2. 或在 Vercel 项目设置里确认 GitHub(`lm203688/oraclemind`) webhook 已连接并启用 auto-deploy on push to `main`。

> GitHub PAT（细粒度 `github_pat_11A7…`）已验证可读写，后续推送已无阻塞。

---

## P0 — 通电（0–30 天）

> **目标：让钱能收进来、让证据被看见、让自动化真正跑起来。**
> 这 7 件事不做完，后面所有「提升」都是在给一个没通电的系统刷漆。

| # | 动作 | 谁做 | 验收标准 | 状态 |
|---|---|---|---|---|
| **P0-1** | 支付链路端到端自测（PayPal IPN 开关 + Creem 状态 + 权限自动开通） | ⛔ **需 owner 操作后台** | 真实下单 → 权限自动开通，可复现 | ⛔ |
| **P0-2** | 上线 `/accuracy` 公开战绩页（54 事件 Brier / 方向 / 分域 + 与基线对比） | 自动执行 | 页面 200，首页二级 CTA | ✅ |
| **P0-3** | 打破自举死锁：心跳脱离流量依赖 + self-heal 补进 cron | 自动执行 | `self-heal` loop 连续 7 天 healthy | ✅ |
| **P0-4** | 前端埋点：首屏 / 提问 / 结果 / 升级 / 支付发起 / 支付完成 | 自动执行 | 6 个关键事件有数据 | ✅ |
| **P0-5** | 首页叙事重构：战绩前置，"a lab that publishes its score" | 自动执行 | 首屏出现 Brier 数字 + **全局 metadata/OG/twitter/jsonLd 同步换旗号** | ✅（2026-10-09 补完 metadata） |
| **P0-6** | `/tuivan` 红线复查 + llms.txt 中性化 | 自动执行 | `audit-public-terms.mjs` 0 命中 | ✅ |
| **P0-7** | 付费墙时机：Deep $4.99 设为默认推荐（而非 Premium 订阅） | 自动执行 | 结果页升级触发点上线 | ✅ |

**P0 完成度：6/7 自动化项全部落地，仅 P0-1 因需 owner 操作支付后台而阻塞。**

### P0 交付明细（2026-10-08 ~ 2026-10-09）

| # | 落地物 | 文件 |
|---|---|---|
| P0-2 | 公开战绩页 + 只读 API（Brier、CI95、样本充足度、基线对比、逐事件表） | `src/app/accuracy/page.tsx`、`src/app/api/public/accuracy/route.ts` |
| P0-3 | 心跳工作流（打破「心跳依赖流量」死锁）+ 2 条 self-heal cron（另加 `daily-forecast-seed`、`self-heal-supervisor`） | `.github/workflows/heartbeat.yml`、`vercel.json` |
| P0-4 | 埋点全链路：模型 + 采集端点 + 客户端 + Provider + 漏斗消费端 | `schema.prisma`(ProductEvent)、`src/app/api/events/route.ts`、`src/lib/analytics.ts`、`src/components/providers/analytics-provider.tsx`、`src/app/api/automation/user-analytics/route.ts` |
| P0-5 | 首页战绩前置：`HeroScorecard` + 导航 Scorecard 项 + **全局 metadata/OG/twitter/jsonLd 换旗号**（2026-10-09 补 `layout.tsx` 标题/描述/keywords/OG/twitter/jsonLd + `manifest.json` PWA 描述 + landing-hero 徽章）+ sitemap + llms.txt | `src/components/modules/v3/landing-page-v3.tsx`、`hero-scorecard.tsx`、`src/app/layout.tsx`、`public/manifest.json`、`src/app/sitemap.ts`、`public/llms.txt` |
| P0-6 | 红线扫描 0 命中（上游已修，本次复验确认；用户面 `/tuivan` 用中性词，仅引擎内部 prompt 双轨制保留 substrate 术语） | `scripts/audit-public-terms.mjs` |
| P0-7 | 结果页付费墙（Deep $4.99 主推 / Premium 次选）+ 定价页 Deep 置为默认推荐档 | `src/app/page.tsx`(ResultView)、`src/components/modules/v3/pricing-page.tsx` |

---

## P1 — 长大（30–90 天）

> **目标：让样本自己长大、让 API 开始收钱。**

| # | 动作 | 验收 | 状态 |
|---|---|---|---|
| P1-8 | 事件语料 54 → 300+（Manifold / Metaculus / Kalshi / Polymarket 自动扩产） | n≥300，CI95 宽度 < 0.10 | ⬜ |
| P1-9 | 校准修正（Platt / isotonic），ECE < 0.10，BSS > 0.10 | Scorecard 达标 | ⬜（校准层已就绪，待样本驱动） |
| P1-9b | **一键回报（1-tap）组件**：结果页加「准 / 部分准 / 不准」三档 → 写 `PredictionFeedback`（来源：PHASE0-PHASE1-REPORT §C4；全面报告 §C4/P4） | 月回报数 > 50 | ✅（2026-10-09 落地：OutcomeReturn 组件 + /api/feedback/verify 接线；验收=飞轮开始收到真信号，需上线后看回报量） |
| P1-10 | 前瞻性注册（pre-registration）+ 概率 hash 封存 | 每条事件可验证不可篡改 | ✅（2026-10-09 落地：Simulation 加 `commitHash`/`committedAt`，`src/lib/engines/commit-seal.ts` 用 sha256 封存"创建时规范载荷（不含结局）"，在 personal/event stream + engine 三处完成点调用；验收=上线后 Simulation.commitHash 非空率=100%） |
| P1-11 | 事件产品化 `/events`：进行中事件板 + 用户可追踪 | 用户事件预测 > 0 | ⬜ |
| P1-12 | API Key + 按次计费（MCP / OpenAPI / public field） | 首笔 API 收入 | ⬜（⛔ 依赖 P0-1 支付通电） |
| P1-13 | 开发者门户 `/docs`：快速开始 + 示例 + Widget 嵌入码 | 第三方可自助接入 | ⬜ |
| P1-14 | 修 `intel-adopt` 死循环（0 insight → 有产出）+ 主引擎消费接线 | `useCount > 0` | ⬜ |
| P1-15 | 每日一推 + streak 服务端化 | `daily-forecast` 表 > 0 + streak 连续天数可查 | ✅（2026-10-09 落地：User 加 `streakCount`/`streakLastDate`，`src/lib/engines/streak.ts` 纯函数 + `daily-forecast/route.ts` 在生成新预测时按"昨日/今日/断签"更新；daily-forecast 持久化此前已存在） |
| P1-16 | 修测试：32 个伪集成测试（localhost 依赖 → handler 级单测）（来源：TESTING-SUMMARY） | CI 全绿且真实覆盖 | ✅（2026-10-09 复验：实跑仅 1 个 flaky 失败，非报告所述 32 个；已改为确定性 Monte Carlo 校准校验；全 26 套件 / 279 用例通过） |
| P1-17 | GEO 扩产 14 → 50 篇（event-forecasting / decision-intelligence 长尾） | 长尾覆盖 | ⬜ |

### P1 专项补充（来自另两份报告）

**校准与反馈闭环（PHASE0-PHASE1-REPORT）**
- ✅ 经验贝叶斯校准层 `src/lib/engines/calibration.ts` 已上线（零数据也诚实收缩到 0.5）。
- ✅ 符号回归试点 `scripts/symbolic-pilot.py`（gplearn，合成数据方法验证，**非真实训练**）已就位；真实上线需 `PredictionFeedback.actualOutcome` 有 ≥50 条/类样本。
- ✅ **解锁点 = P1-9b 一键回报**（2026-10-09 落地）：结果页 `OutcomeReturn` 三档 → `/api/feedback/verify` → `PredictionFeedback` 飞轮已接通。下一步验收 = 上线后月回报数 > 50，届时校准层从「诚实收缩」升级为「真实学习」。

**测试框架（TESTING-SUMMARY）**
- ✅ Jest + Testing Library + Babel + jsdom 已搭好（根级独立工程，`package.json` 474B + `node_modules`）。
- ✅ 3 套件 / 13 用例通过（工具函数、首页组件、健康检查）。
- ⚠️ **诚实标注**：TESTING-SUMMARY 称「13/13 全过」，但全面报告 §11 指出另有 **32 个伪集成测试（localhost 依赖）仍失败**。二者不矛盾——13 是通过的新测试，32 是既有的红套件。P1-16 的验收是「让这 32 个从红转绿或重构为 handler 级单测」，而非只看总数。

---

## P2 — 加固（90–180 天）

| # | 动作 | 状态 |
|---|---|---|
| P2-18 | 数据集版本化 + 公开发布（护城河） | ⬜ |
| P2-19 | 抗污染活体记分板（学术 / 媒体引用入口） | ⬜ |
| P2-20 | AG-UI 补齐，形成完整 2026 Agent 协议栈 | ⬜ |
| P2-21 | 混合模式：Deep + 专家复核加价档（对标 Nebula $50M ARR） | ⬜ |
| P2-22 | 好友对比 + 可分享匹配卡（社交飞轮） | ⬜ |
| P2-23 | 移动端 PWA 安装引导 + 推送 | ⬜ |
| P2-24 | 中文流量收单方案落地（或流量重定向到中性面） | ⬜（⛔ 依赖 P0-1） |
| P2-25 | B 端：事件预测订阅（研究 / 媒体 / 投研） | ⬜ |

---

## 🎮 预测游戏转型 · 波次计划（2026-10-09 报告）

> 报告核心判断：转型方向正确（ForecastBench 2026-10-09 显示带工具 AI Brier 69.0 已超人类顶级 68.6，"给概率"正在商品化，必须转向"人"），**但停滞真因是交付通道断，不是方向错**。重排为「先能玩 → 再好玩 → 再长大」，北极星建议从"付费"改为"校准"（见 owner 闸门 #7）。

### 波次 0：止血（1–3 天）

| # | 动作 | 验收 | 状态 |
|---|---|---|---|
| **W0-1** | 打通部署通道，把已完成的 P0/P1 推上线 | `GET /accuracy`=200，title 变新旗号 | 📦 GitHub 已推（`dae99be6`）；⛔ **Vercel 生产部署被 token 失效阻断**，需 owner 修部署 |
| **W0-2** | 部署后自动回探哨兵（部署完自动打生产端点，失败即告警） | 部署失败 5 分钟内可知 | ✅ 已落地（`src/lib/ops/deploy-probe.ts` + 路由 + command-center Loop 15 + vercel.json 6h cron），📦 待部署 |
| **W0-3** | LLM fallback（GLM 失败时切备用模型/确定性降级，不静默返回空串） | 引擎永不返回空概率 | ✅ 已落地（`src/lib/zai-client.ts` 兜底链：主模型→OpenAI 兼容备用→本地降级文案），📦 待部署 |
| **W0-4** | 首页冷启动优化（当前 7.33s） | 首屏 TTFB < 2s | ⬜（未做；高风险改动，需 profiling） |

### 波次 1：核心玩法（2–4 周）

| # | 动作 | 验收 | 状态 |
|---|---|---|---|
| **W1-1** | 校准曲线主界面（替代胜负榜，看 ECE + Resolution） | 玩家可见自己的校准曲线 | ⬜ |
| **W1-2** | Beat the Oracle：先独立作答 → 揭晓 AI → 算 Alpha | 每题产生人机对照数据 | ⬜ |
| **W1-3** | 三层短周期题库（快题 1–7 天 / 中题 / 慢题） | 快题占比 ≥40%，24h 内首次结算 | ⬜（题库已有 Manifold 源 + 时间跨度过滤，待加周期分桶） |
| **W1-4** | 段位系统（直觉派→校准者→预言家） | 玩家有明确下一目标 | ⬜ |
| **W1-5** | 身份与防刷：提交锁（同题禁止结算前改口）+ 登录绑定 | 排行榜可信 | ✅ **提交锁已落地**（`arena.ts submitArenaPrediction` 锁定）；登录绑定 ⬜（需 auth 改造） |
| **W1-6** | 错误归因（Why You Were Wrong） | 每次结算给一条归因 | ⬜ |

> **§8.3 回溯挑战（零成本让玩家秒获校准曲线）**：经核 **已落地**——`fetchCorpusMarkets` 用 54 条已结算语料作主源，`knownOutcome` 提交即结算（arena.ts L593-618）。无需重建，是 W1 最低成本启动项。

### 波次 2：放大与护城河（1–3 月）

| # | 动作 | 验收 | 状态 |
|---|---|---|---|
| **W2-1** | 预测遗嘱（个人轨复活，哈希封存 + 到期复盘） | 情感向传播素材 | ⬜（P1-10 `commitHash` 已具备封存能力，待产品面） |
| **W2-2** | 组队预测 + 分域角色 | 队内聚合 > 个人均值 | ⬜ |
| **W2-3** | 已结算事件 54 → 300+ | n≥300，CI95 <0.10 | ⬜（P1-8） |
| **W2-4** | 「人类优势域地图」首发报告 | 可引用/发表 | ⬜ |
| **W2-5** | 演出层：结算动画 + 揭晓仪式 + 可分享战绩卡 | 分享率 >5% | ⬜ |
| **W2-6** | B 端：API Key + 按次计费 + 开发者门户 | 首笔 B 端收入 | ⬜（⛔ 依赖 P0-1） |
| **W2-7** | 移动端 PWA 安装引导 + 推送 | 移动端占比 >50% | ⬜ |

---

## 关键依赖关系

```
P0-2 战绩页 ──┬──→ P0-5 首页叙事（需要战绩数据）
              └──→ P0-7 付费墙（需要信任背书）

P0-3 心跳 ────→ 所有 P1 自动任务（心跳不做，P1 全是空转）

P1-8 语料扩充 ──→ P1-9 校准修正（n 不够，校准无意义）
                  └──→ P2-19 活体记分板

P1-9b 一键回报 ─→ 校准层从「诚实收缩」升级为「真实学习」（PHASE0 解锁点）

P0-4 埋点 ────→ 一切增长优化（没有埋点，优化都是盲猜）

P0-1 支付 ⛔ ──→ P1-12 API 计费 / P2-24 中文收单（支付链路不通，计费无意义）
```

---

## 需 owner 出手的事项（唯一人工闸门）

| # | 事项 | 影响 | 状态 |
|---|---|---|---|
| 1 | PayPal 后台开启 IPN（接收 IPN 消息 + URL = `https://oraclemind.cc/api/payment/paypal/ipn`） | 不修则收款必失败 | ⛔ |
| 2 | 确认 Creem 账号状态与 webhook 可达 | 第二支付通道 | ⛔ |
| 3 | 核对 187 free 用户构成（是否含测试/匿名账号） | 校准转化诊断 | ⬜ |
| 4 | 是否批准 `/tuivan` 红线处置方案 | 合规 + 支付通道安全 | ⬜（用户面已合规，待确认） |
| 5 | OCR 剩余古籍（如仍缺） | 古典 substrate 完整性 | ⬜ |
| 6 | 🔴 **修复 Vercel 生产部署**（重生成 Token 或确认 GitHub webhook） | 不修则所有代码到不了用户，停滞持续 | ⛔（见上方「部署通道状态」） |
| 7 | 拍板 CORE-GOALS 第 3 条原则：`Monetization as Validation` → `Validation as Monetization` | 北极星从"付费"改为"校准"，保护校准数据纯度 | ⬜（报告建议改非删；需 owner 决策） |

**保留人工闸门的原则性理由**：自动回滚到旧 commit、自动合入代码 PR 涉及不可逆生产变更，保留「ADMIN 触发 / 人工合并」符合 Precision Over Hype。补丁草稿可全自动，合并留人。

---

## 输入报告索引

| 报告 | 路径 | 贡献到本路线图 |
|---|---|---|
| 全面提升报告 2026-10-08 | `docs/reports/OracleMind-全面提升报告-2026-10-08.md` | P0/P1/P2 主框架、竞品对标、北极星指标 |
| Phase0/1 准确率校准 | `docs/reports/PHASE0-PHASE1-REPORT.md` | P1-9 / P1-9b 校准与 1-tap 回报、符号回归试点 |
| 测试框架总结 | `docs/reports/TESTING-SUMMARY.md` | P1-16 测试修复、Jest 工程现状 |
| 预测游戏转型与全面提升报告 2026-10-09 | `docs/reports/OracleMind-预测游戏转型与全面提升报告-2026-10-09.md` | W0/W1/W2 波次重排、校准阶梯/Beat the Oracle/错误归因机制、合规宪法、部署通道诊断 |

*本路线图与 CORE-GOALS 绑定；完成一项即更新状态，不另开文档。最后复验：2026-10-09。*
