# OracleMind SCI 论文达标性核查与评价

> 核查日期：2026-10-19｜核查人：WorkBuddy AI
> 方法：直接读取 `vercel-deploy/` 生产代码、`schema.prisma`、`scripts/`、Git 历史与 `data/` 种子集，逐项对照 SCI 投稿硬门槛。
> 依据方案：`OracleMind-SCI就绪执行方案-2026-10-18.md`

---

## 一、核查结论（一句话）

**❌ 项目目前尚未达到 SCI 论文要求。**

- **内核设计已达 SCI 级**：经验贝叶斯收缩 + Split Conformal 有限样本修正 + 防篡改前瞻注册，三件事在文献与方法上站得住，是真实可发表的科研内核。
- **但"实验结果 + 可复现资产 + 学术诚信 hygiene"三项硬门槛全部空缺**。其中"数据"这一项不仅空缺，还存在一个**一票否决级诚信雷点**（见第三节）。

> 一句话定位：**论文的"骨架与思想"已具备，但"血肉（真实实验数据）"为零，且现有唯一数据生成器产于造假。** 不能直接投 SCI；必须先完成 2026-10-18 方案的 Sprint 0→1→5。

---

## 二、SCI 硬门槛对照表（逐项核查）

| # | SCI 硬门槛 | 状态 | 证据 |
|---|---|---|---|
| 1 | 真实、可核验的 (预测 p, 真值 y) 数据集 | 🔴 BLOCKED | 唯一数据机制 `scripts/cold-start-seed.mjs` 为**编造**（见第三节）；`data/backfill-events.seed.json` 的 14 条真实事件**未写入数据库**（无 `coldstart-backfill.mjs`，无 DB 文件） |
| 2 | 校准/不确定性方法的定量对比实验 | 🔴 BLOCKED | `vercel-deploy/experiments/` 目录**不存在**；无 Platt/Isotonic/本项目三者对比，无 ECE/Brier/LogLoss/Bootstrap CI 结果 |
| 3 | 统计正确性（覆盖率/校准误差）可复现 | 🟡 PARTIAL | `calibration.ts`（经验贝叶斯收缩，零数据→0.5）、`conformal-prediction.ts`（`ceil((n+1)q)` 有限样本修正、`1-1/n` 边际覆盖）、`forecast-guard.ts`（BSS）**代码真实且文献扎实**，但**无任何运行结果产出** |
| 4 | 前瞻注册 / 防篡改（系统论文卖点） | 🟡 PARTIAL | `commit-seal.ts` 引擎存在（`src/lib/engines/commit-seal.ts`），但**未部署公开验证页**（vercel-deploy 内无 `verify` 路由/页面），OpenTimestamps 锚定未接通 |
| 5 | 因果层方法学诚实 | 🔴 BLOCKED | `causal-reasoning.ts` 仍为 **LLM prompt 包装**，无 do-calculus / 后门调整 / d-分离；若写 "causal inference" 即学术不端 |
| 6 | 古典层诚实声明（八字=启发式先验） | 🔴 BLOCKED | `domain-prior.ts` 不存在；八字仍可能以"先验"名义进入统计推断 |
| 7 | 数据来源可复现 + 引用清单 | 🔴 BLOCKED | 真实种子集有 `collectionProtocol` 与 `source` 字段，但**未实际采集到 300+**，且未跑通回填 |
| 8 | CI 门禁（防回归 / 防投毒） | 🔴 BLOCKED | `vercel-deploy/.github/workflows/` **不存在**；`api/feedback/outcome` 仍无鉴权（查缺报告 Q 头号缺口仍在） |
| 9 | 论文草稿 + 复现包 | 🔴 BLOCKED | 无任何草稿、无复现 README、无实验 JSON |

**状态汇总**：🔴 BLOCKED 6 项 / 🟡 PARTIAL 3 项 / 🟢 DONE 0 项（注：PARTIAL 的 3 项均为"代码在但零产物"）。

---

## 三、🚨 红色警报：数据完整性危机（一票否决级）

`scripts/cold-start-seed.mjs` 是项目当前**唯一**向 `PredictionFeedback` 灌数据的脚本，但其本质是**编造数据**，若作为校准证据使用即构成学术不端：

```js
// cold-start-seed.mjs 关键逻辑（已读取原文）
const SEED_EVENTS = [ /* 硬编码的"猜测事件"，如 "Will NVIDIA release a new GPU..." */ ];
predictedDirection: event.outcome,   // 预测方向
actualOutcome: event.outcome,        // 实际结局 = 同一个 outcome  ← 自洽循环
reportedAt: new Date(),              // 决议日写成"现在"，而非真实过去日期
actualNote: 'Cold-start seed ... Not from real user feedback.'
```

三重问题：
1. **自洽循环**：`actualOutcome` 与 `predictedDirection` 取同一值 → Brier 是人为构造的低值，不是模型在真实世界上的表现。
2. **非真实决议**：事件是"未来式猜测"（如 2025 年发新 GPU），`reportedAt` 却填当前时间，没有真实决议真值。
3. **零外部可核验**：没有任何 `source` URL，不可被审计，不属于任何公开预测基准。

**结论**：此脚本的数据**绝不能**进入任何论文的实验表。2026-10-18 方案 T0-1/T0-3 已设计好正确路径（从 Metaculus/GDELT/官方主源自动采集真实已决事件），但该正确路径**尚未编码执行**。

---

## 四、真实已达 SCI 级的优势（公允记录）

这些是项目值得肯定的硬资产，也是未来论文能站住的根：

1. **经验贝叶斯收缩校准**（`calibration.ts`）：`shrink = n/(n+K)`，零数据→诚实回 0.5，有闭式真值，符合"诚实降级"学术卖点。
2. **Split Conformal 有限样本修正**（`conformal-prediction.ts`）：采用 `ceil((n+1)·q)` 而非 `ceil(n·q)`，给出 `1-1/n` 精确边际覆盖保证；引用 Lei 2018 / Vovk 1999，文献正确。这是冷启动不确定性的**分布无关保证**，是方法论文的核心创新点。
3. **Brier Skill Score / climatology 基线**（`forecast-guard.ts`）：提供相对气候态的技能评分，指标选择专业。
4. **防篡改前瞻注册思想**（`commit-seal.ts`）：把"预测先封存、后揭晓"做成可审计资产，是系统论文（AIES/FAccT/Scientific Data）的强差异化卖点——只差部署与 OpenTimestamps 接通。
5. **地基已加固**：commit `0dbc7d5b` 修复了 `prediction-feedback.ts` 的 4 个生产 tsc 错误（flywheel 曾静默失败），并加了乐观锁。

> 一句话：**"做什么、为什么科学"已经想清楚并写进代码；"证明它有效"的实验还没做。**

---

## 五、距离达标的最短路径（回指 10-18 方案）

按投入产出比，达标关键路径只有三步，其余可并行：

| 步骤 | 任务 | 当前卡点 | 产出 |
|---|---|---|---|
| **S0（必须）** | T0-2 改 schema 加 `isBackfilled/sourceEventId/resolvedAt` + `prisma migrate`；T0-3 写 `coldstart-backfill.mjs` 从 `backfill-events.seed.json` 真实回填 | schema 未改、回填脚本未写、编造脚本未停用 | ≥200 条真实 (p,y) |
| **S1** | 跑 `experiments/conformal-coldstart.mjs` 对比 4 种校准器 | `experiments/` 不存在 | ECE/Brier/LogLoss/CI 结果 JSON |
| **S5** | 写 P2 方法论文（共形冷启动）+ P1 系统论文（防篡改注册） | 无草稿 | 两篇 preprint |
| 并行 | T2 部署 verify 页 + OTS；T3 因果层改名/升级；T4 八字改"启发式先验"声明；T8 加 CI 鉴权 | 均未做 | 系统论文底座 + 诚信合规 |

**死线纪律（来自 10-18 红线）**：
- `cold-start-seed.mjs` 的编造数据**永不进论文**；论文数字必须来自 S0 真实验证集。
- 因果层治理（T3-1）完成前，论文不得出现 "causal inference"。
- 八字在论文中只能称 "structured domain heuristic prior"，禁称科学先验。

---

## 六、综合评分与建议

| 维度 | 评分（/10） | 说明 |
|---|---|---|
| 科学思想新颖性 | 8 | 共形冷启动 + 防篡改注册，方向新颖且可发表 |
| 方法正确性（代码层） | 8 | 校准/共形/BSS 实现扎实、文献正确 |
| 实验证据 | 0 | 零真实结果；唯一数据生成器造假 |
| 可复现性 | 1 | 无实验脚本产物、无复现包、无 CI |
| 学术诚信 hygiene | 2 | 编造种子脚本未清理；因果/古典层声明缺失 |
| 工程完成度 | 4 | 内核可用，部署/验证页/鉴权缺失 |

**总评：当前处于"SCI 级设计 + 0 实验证据"状态，距离达标约需 40–51 人天（≈10–13 周）完成 10-18 方案。** 不可直接投稿；但内核质量高，属于"差最后一公里实验"的可救项目，不是推倒重来。

**最优先动作（今天就做）**：停用 `cold-start-seed.mjs`，落实 T0-2 + T0-3，先把 14 条（扩到 300+）真实事件灌进 `PredictionFeedback`。这是解锁全部后续论文的唯一前置。

---

*核查基于仓库实际文件与 Git 历史，非依据方案文档自我声明。凡标注 BLOCKED/PARTIAL 均已在代码中确认缺失。*
