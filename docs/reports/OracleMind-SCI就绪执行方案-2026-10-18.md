# OracleMind SCI 就绪执行方案（可直接落地版）

> 日期：2026-10-18｜依据：`OracleMind-科学性与SCI论文可行性评估-2026-10-18.md`
> 目标：把项目从"科学内核达标但零数据"推进到"具备 SCI 投稿所需的实验数据 + 方法完整性 + 可复现资产"。
> 用法：本文每个任务都是一张工单（文件级改动 + 验收标准 + 完成定义）。按 Sprint 顺序执行，Sprint 0 是硬前置。

---

## 0. 总路线（14 周，6 个 Sprint）

```
Sprint 0 (W1-2)  数据解锁：冷启动回填 → 真实 (p,y) 数据集      ← 一切前提
Sprint 1 (W3-5)  方法硬化：跑 P2 共形校准对比实验 + 测试加固
Sprint 2 (W5-6)  系统资产：commit-seal 归位部署 + OpenTimestamps 锚定
Sprint 3 (W6-8)  因果层治理：causal-reasoning 改名/升级（去假因果）
Sprint 4 (W8-10) 古典层重构：八字→结构化领域启发式先验（接口+声明）
Sprint 5 (W10-14) 论文撰写与投稿（P1 系统 + P2 方法，并行）
```

**铁律**：Sprint 0 未完成前，不启动任何论文撰写。没有真数据，P1/P2/P3/P5 全无结果。

---

## Sprint 0 — 数据解锁（硬前置，W1-2）

### T0-1 建立历史事件种子数据集（**无需人工数据输入——AI 代理自动采集**）
> 回答"我没数据输入怎么办"：数据由 AI 代理从**公开可核验真值源**自动采集，每条 outcome 带主源引用。这比人工编 50 条更严谨（外部可验证），且符合学术规范（用公开预测基准是标准做法）。起步集已采 14 条真实已决事件（`data/backfill-events.seed.json`，经 `scripts/validate-backfill.mjs` 实测通过）。

**执行要求**
- 采集协议（已写入 seed 文件 `collectionProtocol` 字段，校验脚本强制执行）：
  - **首选源**：Metaculus 已决二元问题（`metaculus.com`，含人群基线，可做 engine-vs-crowd 对比；2024 年有 2000+ 条已决，见 openforecaster.github.io 实证）
  - **补充源**：GDELT 历史事件、官方主源（federalreserve.gov / fec.gov / who.int / isro.gov.in / olympics.com / europarl.europa.eu / usgs.gov 等）
  - **硬性规则**：每条 `outcome` 必须可追溯到公开主源 URL；`resolutionDate` 必须早于采集日（回填=过去事件）；禁止无来源断言
- **采集动作**：代理用 WebSearch 逐条核实真值并写 `source`；校验脚本 `validate-backfill.mjs` 已升级——强制"决议日必须已过" + "source 须为可达 URL" + 非 Metaculus 源给提示。
- **扩量**：起步 14 条 → 用同一协议（优先 Metaculus 导出）扩到 **300+**，全部带引用。
- **学术诚信**：代理采集合成的是"公开可核验真值"，不是模型编造；论文方法章节声明数据来源与可复现性。

**验收**：`backfill-events.seed.json` 含 ≥300 条、全部 `resolutionDate` 早于采集日、每条有可达 `source`、通过 `validate-backfill.mjs`。
**完成定义**：`node scripts/validate-backfill.mjs` 零错误；数据集可复现（附 source 清单）。

**验收**：`backfill-events.seed.json` 含 ≥50 条、无 `outcome=neutral` 占比 >20%、每条有 `source`。
**完成定义**：数据通过 `scripts/validate-backfill.mjs` 校验（字段齐全 + source 可达）。

### T0-2 新增 PredictionFeedback 回填字段
**执行要求**：在 `schema.prisma` 的 `PredictionFeedback` 模型增加：
```
isBackfilled   Boolean  @default(false)   // true=历史回填，不进入前瞻注册账本
sourceEventId  String?                  // 关联 backfill-events.seed.json 的 id
resolvedAt     DateTime?                // 回填时填真实决议日
```
并执行 `prisma migrate dev`（**禁止再用手写 SQL / db push**，见查缺报告 H4）。

**验收**：`npx prisma migrate dev --name add_backfill_fields` 成功；`prisma generate` 后 `tsc --noEmit` 生产错误 = 0（CI 门禁已建）。
**完成定义**：`db.predictionFeedback` 可存回填标记。

### T0-3 写冷启动回填脚本
**执行要求**：新建 `scripts/coldstart-backfill.mjs`
- 读 `data/backfill-events.seed.json`
- 对每条事件调用 `prediction-engine` 产出 `p`（走真实引擎，非随机）
- 写 `PredictionFeedback`：`actualOutcome` 取 seed 真值、`isBackfilled=true`、`resolvedAt=resolutionDate`
- 全部包在 `SEED_ACCOUNT_ID`  guard 下（避免污染真实用户账本）
- 幂等：已存在的 `sourceEventId` 跳过

**验收**：运行后 `forecastScorecard` 对回填数据返回非 null Brier，且 `n ≥ 50`。
**完成定义**：`npm run backfill` 一键产出数据集；新增测试 `scripts/__tests__/coldstart-backfill.test.ts` 断言 `n≥50` 且 Brier 落在合理区间。

### T0-4 竞技场自动结算接线
**执行要求**：在 `arena.ts` 的 `mirrorArenaPicksToFlywheel` 之外，新增定时任务：每日拉取已到期市场，回填 `actualOutcome`（来源=市场决议）。复用 `vercel.json` 已有 cron 机制。
**验收**：新预测在决议后 24h 内进 `PredictionFeedback`，`isBackfilled=false`。
**完成定义**：运行 7 天观察，≥10 条真实结算入库。

> **Sprint 0 出口标准**：`PredictionFeedback` 中 `isBackfilled=true` 的 (p,y) 对 ≥200，`isBackfilled=false` 的真实结算 ≥10。此时 P2/P3/P5 论文的实验数据齐备。

---

## Sprint 1 — 方法硬化（W3-5）

### T1-1 共形校准对比实验（P2 论文核心结果）
**执行要求**：新建 `scripts/experiments/conformal-coldstart.mjs`
- 在同一回填数据集上对比 4 种校准器：
  1. 不校准（LLM 原始 p）
  2. Platt scaling
  3. Isotonic（MCP 风格）
  4. **本项目：经验贝叶斯收缩 + Split Conformal（calibration.ts + conformal-prediction.ts）**
- 指标：ECE、Brier、LogLoss、Bootstrap CI 宽度、边际覆盖率（应 ≥ 1−1/(n+1)）
- 输出 `experiments/results/conformal-coldstart.json` + 图表数据

**验收**：本项目方法在小样本（n<50）段的 ECE / 覆盖达标率优于基线 ≥1 项，且结果可复现（固定 seed）。
**完成定义**：实验脚本入 CI（每次 push 重跑，防回归）。

### T1-2 测试加固（补查缺报告 H2 的 0% 覆盖）
**执行要求**：为 `prediction-feedback.ts`、`commit-seal.ts`、`causal-reasoning.ts`（改名后）、`scenario-synthesizer.ts` 补单测，目标引擎层覆盖率 ≥60%。
**验收**：`jest --coverage` 引擎层 ≥60%，CI 门禁拦截 <50%。
**完成定义**：覆盖率报告入 `coverage/` 并提交。

### T1-3 统计真值测试补强
**执行要求**：给 `calibration.ts` 加断言：零数据→0.5；`K=20,n=20` 时 shrink≈0.5；`recommendedConfidenceCap` 单调。给 `forecast-guard.ts` 加：climatologyBrier(0.8)=0.16；BSS 符号正确。
**验收**：新增用例全绿，且每条对应闭式真值。
**完成定义**：测试文件入 `src/__tests__/lib/`。

---

## Sprint 2 — 系统资产（W5-6，P1 系统论文底座）

### T2-1 修复 commit-seal 未部署（查缺 Q 头号）
**执行要求**：把根目录 `src/app/verify/[id]/page.tsx`、`src/app/api/opentimestamps/anchor/route.ts`、`src/app/api/verify/public/route.ts` **迁移到 `vercel-deploy/src/app/`**，删除根 `src/`。
**验收**：`next build` 后 `/verify/[id]` 可访问；OpenTimestamps 锚定 API 在 `vercel-deploy` 内被打包。
**完成定义**：根 `src/` 目录删除，构建产物含验证页。

### T2-2 OpenTimestamps 锚定接通
**执行要求**：在 `sealSimulation` 成功后调用 OpenTimestamps API（或本地 `ots` CLI）对 `commitHash` 做时间戳锚定，存 `sealedAt` + `otsProof`。
**验收**：公开验证页可展示"此预测在 X 时间前已封存，不可篡改"。
**完成定义**：端到端演示：注册→封存→锚定→验证页展示证明。

### T2-3 防投毒（查缺致命缺口）
**执行要求**：`api/feedback/outcome` 加鉴权（仅 `SEED_ACCOUNT` + 管理员 + 市场决议服务可写），普通用户写结局走 arena 结算通道。
**验收**：未授权 POST 返回 401/403；CI 加安全测试。
**完成定义**：`security/api-guard.test.ts` 覆盖该路由。

---

## Sprint 3 — 因果层治理（W6-8，去假因果红线）

### T3-1 二选一（必须选，否则不得投稿）
- **方案 A（推荐，论文级）**：在 `causal-reasoning.ts` 增加真因果计算——给定 LLM 建议的 DAG，实现 **后门调整（backdoor adjustment）** 与 **可识别性检查**（d-分离），输出调整集与偏差界。无需新依赖，纯 TS 可实现。
- **方案 B（务实）**：模块重命名为 `structured-reasoning.ts`，文档与所有引用改称"structured causal-style reasoning"，**绝不在论文写 causal inference**。

**验收**：若选 A，新增 `backdoorAdjustment(dag, pairs)` 单测（用教科书 3 节点链验证偏差消除）；若选 B，全文无 "causal inference" 字样。
**完成定义**：通过方法学自查，可安全写进论文方法章节。

---

## Sprint 4 — 古典层重构（W8-10，诚实先验）

### T4-1 八字作为"结构化领域启发式先验"
**执行要求**：新增 `lib/engines/domain-prior.ts`，把古典框架输出定义为 **structured domain heuristic prior**（一个带置信区间的先验分布），明确声明"非科学、仅供人类参考"。它**只作为经验贝叶斯收缩的 `baseRate` 补充项**，永不覆盖数据。
**验收**：古典层输出在 UI 与论文中均标注"heuristic, non-scientific"；不参与统计显著性计算。
**完成定义**：`domain-prior.ts` 单测 + UI 标注 + 论文声明段。

### T4-2 论文诚信声明段
**执行要求**：在代码仓库 `docs/` 与论文方法章节放固定声明："八字/命理为结构化人类启发式，不具备科学预测效力，本系统仅将其作为可审计的领域先验，不进入统计推断。"
**验收**：声明出现在公开页 footer + 论文。
**完成定义**：声明文案定稿。

---

## Sprint 5 — 论文撰写与投稿（W10-14）

### T5-1 P2 方法论文（首选，最稳）
- 标题方向：**"Conformal Calibration under Cold Start: Empirical-Bayes Shrinkage with Distribution-Free Coverage Guarantees for Hybrid Forecasting"**
- 投：ICML/NeurIPS Conformal Prediction workshop 或 IJF
- 用 Sprint 1 实验结果 + Sprint 0 数据

### T5-2 P1 系统论文（最强差异化）
- 标题方向：**"Tamper-Evident Forecasting: Cryptographic Prospective Registration for Human-AI Hybrid Prediction"**
- 投：AIES / FAccT / Scientific Data（数据集版）
- 用 Sprint 2 的 commit-seal + OpenTimestamps + 验证页

### T5-3 复现包
- 开源代码 + `backfill-events.seed.json` + 实验脚本 + OpenTimestamps 证明
- 附 `README` 复现步骤

**验收**：两篇草稿完成，含真实实验结果（非示例数字）、诚信声明、复现包。
**完成定义**：投稿（或 preprint）。

---

## 执行纪律（红线，来自 SCI 评估）

1. 所有准确率数字必须来自 Sprint 0 真实验证集；**docstring 里的 0.136/0.159/83.3% 示例不得进论文**。
2. 古典层在论文中只能称 "structured domain heuristic prior"，**禁称科学先验**。
3. 因果层按 T3-1 处理前，论文不得出现 "causal inference"。
4. 诚实降级（零数据回 0.5、n<3 拒保证）**写进论文当卖点**，不藏。
5. 迁移一律 `prisma migrate`，**禁用手写 SQL / db push**（查缺 H4）。

---

## 工作量估算（1 人 + AI 协作）

| Sprint | 关键任务 | 人天 |
|---|---|---|
| 0 | 种子数据+迁移+回填脚本+竞技场结算 | 8–10 |
| 1 | 对比实验+测试加固+真值测试 | 8–10 |
| 2 | commit-seal 归位+OTS+防投毒 | 5–6 |
| 3 | 因果层治理 | 3–5 |
| 4 | 古典层重构+声明 | 4–5 |
| 5 | 论文撰写+复现包 | 12–15 |
| **合计** | | **40–51 人天（≈10–13 周）** |

**最关键路径**：Sprint 0 → Sprint 1 → Sprint 5(P2)。只要这三步跑通，第一篇方法论文即可投；P1 系统论文与 Sprint 2 并行，几乎零额外前置。

---

*本方案每条任务均可在 `vercel-deploy/src` 与 `data/` 内直接落地；所有文件引用对应既有模块。验收标准可被 CI / 单测自动判定。*
