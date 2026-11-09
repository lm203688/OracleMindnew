# OracleMind 对标评估报告：CodaBench Neural Interfaces 2026 六项标准

> 评估任务：Chief 派单（请求 ID `oraclemind-benchmark-eval-1`，m00213）
> 评估时间：2026-11-06 ｜ 评估性质：**纯评估，不改代码**（Chief 明确）
> 评估对象：CodaBench Neural Interfaces 2026 六项标准 vs OracleMind 现状

---

## 评估结论总览

| # | 标准 | OracleMind 现状 | 评级 | 可操作提升项 |
|---|---|---|---|---|
| ① | 可复现性（±2σ 重跑 / 种子锁定） | 有 `reproduce/` 复现包（run-all.sh 一键复现校准飞轮+共形实验）+ package-lock.json 依赖锁定 + feature-significance/agent-tools 有确定性 RNG（种子参数化） | 🟢 基本达标 | 提升：种子/环境锁定显式化（补 .nvmrc 或 engines 字段 + 每次实验记录 node/npm 版本与 seed），重跑脚本加 ±2σ 置信区间断言 |
| ② | 数据合规（外部数据声明 / 密封测试集禁止） | 无独立外部数据集（语料为内联事件 + 人工标注 outcome，877 万命例为理论数据非结局真值）；有 `integrity-declaration.md` 诚信声明；无密封测试集 | 🟡 部分达标 | 提升：补一份"数据来源与许可声明"文档（语料来源、标注方法、无独立数据授权）；确认无密封测试集（当前无） |
| ③ | 评测标准化（60 分钟单 A100） | 项目为 Web 概率预测服务（Node/TS），**非 GPU 训练任务**；无单 A100 评测需求；推理为 API 调用（有 latency/diagnostics 监控） | ⚪ 不适用 | 无（非同类任务；若对标需定义 Web 推理时延预算而非 GPU 训练窗口） |
| ④ | 15GB/profile 存储约束 | 无 profile 存储概念（用户档案为生辰+偏好，数据量极小）；无超限风险 | ⚪ 不适用 | 无（非模型 profile 提交场景） |
| ⑤ | IP 归参与者 | 无对外 IP 声明文档；仓库为私有（lm203688/oraclemind），参与者=用户 | 🟡 部分达标 | 提升：补一份 IP/许可声明（产出归参与者、无第三方专有数据 IP 争议） |
| ⑥ | 能力基线（Constant=33.3%/EEGNet=32.6%/CTNet=35.0%/REVE=36.0%） | 项目已用**基准相对**框架：`scientific-metrics.ts` 多基准（climatology/random/persistence/superforecaster，skill = 1 - model/baseline）+ `north-star.ts` BSS vs 气候学/随机（决策 B 质量优先） | 🟢 已超越 | 提升：无（已具备更强基准相对体系）；可选：若参与神经接口分类赛道，需引入 EEG 数据集与对应基线（当前无 EEG 任务，属不同赛道） |

---

## 一、逐项对照详情

### ① 可复现性（±2σ 重跑，种子/环境/依赖锁定）—— 🟢 基本达标
- **依赖锁定**：`package-lock.json` 存在（npm ci 可复现）。
- **复现包**：`reproduce/run-all.sh`（一键复现校准飞轮 + 共形校准对比，dry-run/write 模式；Step 0 环境检查 node/npm 版本）。
- **确定性 RNG**：`feature-significance.ts` `makeRng(seed)`（L129-162，seed 参数化，默认 0x9E3779B9）；`agent-tools.ts` 有 seed 变量（L316）。
- **提升项**（可操作）：① 补 `.nvmrc` 或 `package.json engines` 锁定 Node 版本（当前无，见 grep engines 为空）；② 复现脚本记录 seed + node/npm 版本到输出；③ 加 ±2σ 置信区间断言（当前重跑无 CI 断言）。

### ② 数据合规（外部数据声明 / 密封测试集禁止）—— 🟡 部分达标
- **无外部数据集**：语料为内联 `event-corpus*.ts`（55+217+126 条）+ 人工标注 outcome；877 万命例为理论数据非结局真值（诚实边界已声明）。
- **无密封测试集**：当前无 held-out 密封测试集。
- **诚信声明**：`integrity-declaration.md` 完整（八字=启发式≤15%，不进入统计推断）。
- **提升项**：补一份"数据来源与许可声明"（语料来源、outcome 标注方法、无第三方专有数据、无密封测试集），归档 docs/。

### ③ 评测标准化（60 分钟单 A100）—— ⚪ 不适用
- 项目是 Web 概率预测服务（Node/TS + Next.js + Prisma），**非 GPU 训练/评测任务**。无单 A100 窗口需求。
- 已有推理性能监控（diagnostics/deploy-probe/latency），但与"60 分钟单 A100 训练窗口"非同类。
- **提升项**：无（若未来接入神经接口赛道才需定义 GPU 预算；当前不适用）。

### ④ 15GB/profile 存储约束 —— ⚪ 不适用
- 无模型 profile 存储概念。用户档案（生辰+偏好）数据量极小（KB 级/用户）。
- **提升项**：无（不适用）。

### ⑤ IP 归参与者 —— 🟡 部分达标
- 仓库私有（lm203688/oraclemind），参与者=用户本人；无对外 IP 声明文档。
- **提升项**：补一份 IP/许可声明（产出归参与者；无第三方专有数据/模型 IP 争议；若未来用开源模型需附许可），归档 docs/。

### ⑥ 能力基线（Constant=33.3% / EEGNet=32.6% / CTNet=35.0% / REVE=36.0%）—— 🟢 已超越
- 项目**已采用更强**的基准相对体系（决策 B 落地）：`scientific-metrics.ts` 多基准对照（climatology/random/persistence/superforecaster，skill=1-model/baseline，Precision Over Hype 原则）+ `north-star.ts` BSS vs 气候学/随机（质量优先，仅已验证结局）。
- 基线 33.3% 对应项目 `launch-readiness/route.ts` `BASELINE_ACCURACY=33.3`（3 场景随机 = 33.3%），但这是分类准确率基准，项目主指标是 Brier/BSS（更严格）。
- **提升项**：无（已具备更强基准相对；EEGNet/CTNet/REVE 为 EEG 分类赛道基线，项目无 EEG 任务，不同赛道）。

---

## 二、可操作提升项清单（按优先级）

| # | 维度 | 现状 | 提升方向 | 价值 | 成本 | 优先级 |
|---|---|---|---|---|---|---|
| 1 | ①可复现性 | 复现包+lock 已有 | 补 `.nvmrc`/`engines` 锁 Node 版本；复现脚本记录 seed+版本；加 ±2σ 断言 | 高（对外可复现性硬门槛） | 低（改 2 文件+脚本） | **P1** |
| 2 | ②数据合规 | 无数据来源声明 | 新增 `docs/data-provenance-statement.md`（语料来源/标注法/无密封测试集/无第三方专有数据） | 高（合规硬门槛） | 低（1 文档） | **P1** |
| 3 | ⑤IP 归属 | 无 IP 声明 | 新增 `docs/ip-attribution.md`（产出归参与者/无第三方 IP 争议/开源依赖许可附录） | 中 | 低（1 文档） | P2 |
| 4 | ③评测标准化 | 不适用（Web 服务非 GPU） | 定义 Web 推理时延预算（若需对标） | 低 | 中 | P3 |
| 5 | ④存储约束 | 不适用（无 profile） | 无 | — | — | 无 |
| 6 | ⑥能力基线 | 已超越（多基准相对） | 无（已具备更强体系） | — | — | 无 |

---

## 三、诚实边界
- 本评估为**纯评估，未改任何代码**（Chief 明确）。
- ③④不适用是事实判定（项目为 Web 概率预测服务，非神经接口 GPU 训练赛道），非规避。
- ⑥"已超越"仅指**基准相对框架**这一维度；项目**未参与** EEG 分类任务，EEGNet/CTNet/REVE 基线不适用（不同赛道），已如实标注。
- 项目无任何独立事实源佐证已解决结局时一律 unresolved（现有事件均人工标注 outcome，为已解决历史事件，属事实记录非预测真值），此处仅就"可复现/合规/基准"维度评估。

## 四、归档
- 本报告：`docs/reports/oraclemind-codabench-benchmark-eval-2026-11-06.md`
- 未修改 docs/README 索引（纯评估，不改变文档结构）。
