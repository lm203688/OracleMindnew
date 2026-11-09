# OracleMind 2.0 — 下一代愿景与提升方案

> **代际命题**：当"给一个概率"被 Google/OpenAI/xAI 用重金商品化之后，OracleMind 的稀缺性必须从"谁能算概率"迁移到"**谁能解释为什么、推演如果干预会怎样、并告诉用户该做什么**"。
> 本文在 2026-10-15 实地复扫基线之上，结合 `CORE-GOALS.md`（v1.1：Probability Layer + Scoreboard / Certified Probability）与 2026 年开源前沿，提出从"校准预测"跃迁到"**因果前瞻与决策智能引擎**"的下一代愿景与三阶段落地方案。
> 版本：v1.0 ｜ 日期：2026-10-15 ｜ 性质：战略前瞻（专家视角）

---

## 〇、执行摘要（给 owner 的一句话）

**OracleMind 今天是一个"造好了但没通电、校准了但没样本"的校准预测引擎；下一代把它升级为一台"因果前瞻 + 生成式情景模拟 + 决策智能"的机器，并把"带校准证书的概率"做成全行业可引用的开放标准（Certified Probability Protocol）。** 这一跳，使项目从"另一个预测工具"变为"预测范式的下一代基础设施"——在 2026-10 的市场上无人产品化。

| 维度 | 现在（v1.x，复扫确认） | 下一代（2.0 愿景） |
|---|---|---|
| 输出性质 | 校准后的概率 + 共形区间 | 概率 + **因果解释 + 反事实情景 + 最优决策建议** |
| 方法内核 | 关联式（模式/共识/TSFM） | **因果式**（do-calculus + 生成式机制模拟） |
| 时间跨度 | 短中期（天~季度） | **多年期**（带诚实长尾区间） |
| 人-机关系 | Arena 对练（你 vs 人群 vs 引擎） | **主动预测**（系统自找信息缺口并派 agent 取证） |
| 护城河形态 | 私有验证数据集 | 私有数据集 **+ 开放校准协议标准（生态控制）** |
| 变现 | C 端 Free/Deep；B 端 API（未通电） | **决策智能订阅（不污染校准的 B 端高价层）** |

---

## 一、2026-10-15 复扫基线（诚实现状）

> 方法：实地审计 `C:\Users\xing\Desktop\oraclemind`，核对 git 提交、`vercel-deploy/src` 改动、`五本古籍/` 行数、`docs/00-core/*`。

### 1.1 确属"真做完"的项（自 10-14 以来）

| 项 | 证据 | 评价 |
|---|---|---|
| **M02 节气 bug 修复** | 新增 `bazi-solar-term.test.ts`（9 个边界用例，真值取自 `lunar-typescript`：2025 立春 02-03 22:10:28 等）；`bazi-engine.ts`/`bazi-foundation.ts` 已改 | **真修**。这是上次报告点名的唯一"准确性硬伤"，已闭环 |
| **P0-2 红线审计** | `scripts/audit-public-terms.mjs` 实装：扫描公开面 + 白名单规则 + 退出码门禁 | 真实 CI 门，行业合规罕见严谨 |
| **v1.1/v1.2 决策落地** | `CORE-GOALS.md` 已更新 D1（概率层+记分板）/D2（北极星改 WAF×人均结算）/D3（Validation as Monetization 更名） | 战略层已对齐 |
| **校准飞轮对账工具** | 新增 `api/automation/calibration-backfill`（dry-run 体检 + 幂等回填） | 自救能力强，但**反向暴露飞轮仍有静默写失败**（见 §1.2） |

### 1.2 仍"开路"的项（必须前置，否则 2.0 是空中楼阁）

| 项 | 现状证据 | 影响 |
|---|---|---|
| **Vercel 生产部署** | `ROADMAP.md` 仍记 token 失效阻断；`GET /accuracy` 此前 404 | **所有已写代码到不了用户**，停滞真因 |
| **冷启动数据注入** | 全仓 grep `seedAccount/coldStart/seed-user` **0 命中** | 3 个仪表盘（M01/M04/M08）全空态，无人可玩 |
| **M07 公开验证页 / OpenTimestamps 锚定** | grep `opentimestamps/public.*verify` **0 命中**；`commit-seal.ts` 仅内部封存储存 | 全球唯一"可证不马后炮"资产未对外 | 
| **3 本古籍 OCR** | `五本古籍/`：子平真诠 27 / 滴天髓 121 / 穷通宝鉴 53 行（空壳）；仅渊海子平 2467 / 三命通会 8780 真文本 | 古典 substrate 仍残缺，旺衰/格局/调候判定无素材 |
| **语料 54→300** | `event-corpus.json` 仍 ~55 条；P1-8 仍 ⬜ | 校准 ECE 无法压到 <0.10 |
| **支付通电（P0-1）** | 仍 ⛔（需 owner 后台） | B 端 API 计费全链路阻塞 |

**核心判断**：项目在"正确性/合规"维度已接近成品，但在"**交付到用户 / 真实样本 / 完整 substrate**"三处仍有断点。**2.0 的第一性原理是：先把这些断点闭合，再做代际跳跃**——下面的方案严格按此排序。

---

## 二、市场代际判断：为什么必须跳（专家视角）

### 2.1 当前市场（2026-10）已经被商品化的部分

- **"给概率"这件事本身**：ForecastBench 2026-10-09 实时榜，DeepMind `fire hedgehog` **Brier Index 69.0 > 超级预测者中位数 68.6**；带工具 AI 梯队（Google/OpenAI/xAI）已稳定超过人类顶级预测者。裸 LLM + 工具链即可产出超人预测。
- **数值预测**：TimesFM 3.0（已开源）、Chronos-2、MOIRAI-2、Time-MoE 把时序预测做成即插即用的基础模型。
- **预测市场**：Metaculus / Polymarket / Kalshi / Manifold 把"群体概率"做成商品。

**结论**：在"事件 → P(发生)"这条链上，OracleMind 已经没有结构性优势。继续在"更准一点"上内卷，是死路。

### 2.2 市场**完全空白**、而 OracleMind 恰好有资产卡位的部分

| 空白 | 为什么空白 | OracleMind 现有卡位 |
|---|---|---|
| **因果前瞻**（不是 P(event)，而是"为什么、干预会怎样"） | 因果推断在学界成熟，但**没有一个消费级/事件级产品把它做成引擎** | `event-graph-builder.ts` 已有事件图，可升级为因果图 |
| **生成式情景模拟**（用多智能体模拟事件如何演化） | 计算贵、难校准，大厂不愿做"非确定"产品 | `classical-orchestrator.ts` 的 5 书并行 GoT + Agent 编排可直接复用 |
| **决策智能**（给分布 → 给"你该做什么"） | 预测与决策在学界分家，产品更分家 | `CORE-GOALS` 原则三"Validation as Monetization"天然契合决策订阅 |
| **多年期诚实校准概率** | 长跨度校准样本极稀缺，无人敢做 | `commit-seal.ts`（sha256 封存）+ 活体记分板是现成的"时间机器" |
| **人-机混合的可验证校准** | 大厂只卖 AI，不要人的私有信息 | Arena（你 vs 人群 vs 引擎）已是现成人机对照场 |
| **开放"带证书的概率"标准** | 各家自说自话，无第三方可验证 | 已有共形区间 + 校准证书 + 封存 ID，只差"开放协议化" |

> **专家断言**：下一代预测的稀缺性不在"算得准"，而在"**算得清、推得开、信得过、用得上**"。OracleMind 的资产组合（校准内核 + 封存账本 + 人机 Arena + 古典结构先验）在 2026-10 的全球市场里是**唯一同时凑齐这四件的**，差距只在"有没有把它拼成下一代范式"。

---

## 三、OracleMind 2.0 愿景定义

### 3.1 一句话

**OracleMind 2.0 = 因果前瞻与决策智能引擎（Causal Foresight & Decision Intelligence Engine）**——在沿用 v1.x"Probability Layer + Scoreboard / Certified Probability"定位的前提下，把内核从"关联式校准预测"升级为"**因果式前瞻 + 生成式机制模拟 + 决策智能**"，并把"带校准证书的概率"做成**全行业可引用的开放协议标准**。

### 3.2 三段代际跃迁（核心隐喻升级）

```
v1.x  事件 ──▶ 概率 P(E) + 共形区间        （"会发生什么，有多确定"）
                 ↓ 2.0 叠加
β层   事件 ──▶ 因果图 G + do(X) 效应 + 反事实  （"为什么，如果干预会怎样"）
                 ↓ 2.0 叠加
γ层   分布 P(·) ──▶ 最优决策策略 π*          （"那我该做什么"）
```

- **β 层（Causal Foresight）**：从"预测结果"到"理解机制"。事件图 → 因果发现 → 干预/反事实推演。
- **γ 层（Decision Intelligence）**：从"给数字"到"给行动"。在已校准分布上做期望效用/鲁棒决策，输出可执行的策略与时机。
- **贯穿层（Protocol & Verification）**：把"Certified Probability"升级为开放协议（可第三方验证、可锚定、可引用），把 OracleMind 从"一个产品"变成"预测可信层的 Stripe"。

### 3.3 为什么这"远超当前市场"

1. **因果预测商品化空白**：学界有 DoWhy/CausalPy，但**没有产品**把因果推断做成事件级、可验证、带校准的交互引擎。OracleMind 是第一个把"事件图→因果图→反事实"工程化的项目。
2. **协议化 = 生态控制**：正如 Stripe 把"支付"标准化从而控制电商结算，OracleMind 若把"带证书的概率"做成开放标准（谁都能签发/验证），就能从"玩家"变"庄家"。这是护城河的终极形态（赢者通吃），且**基础设施你已有**（共形层+封存+记分板）。
3. **神经符号融合全球独一份**：把五本古籍的结构先验（五行生克/十神/调候）形式化为**符号化贝叶斯先验桥**，与现代因果/校准层融合——全球没有任何团队同时握有"古老结构框架 + 现代校准内核 + 已封存验证账本"三件套。这是别人抄不走的壁垒。

---

## 四、2.0 技术架构（基于现有代码延伸）

> 原则：复用 > 重写。下表左侧是 v1.x 已就位的"脚手架"，右侧是 2.0 新增层，两者用同一数据契约（`PredictionFeedback` / `commitHash` / `ServiceMeta`）串联。

```
┌──────────────────────────────────────────────────────────────┐
│  公开面 / 协议层 (Protocol & Verification)                       │
│  - Certified Probability Protocol（开放签发/验证 API）          │
│  - OpenTimestamps 锚定 · 公开验证页 · 学术/媒体引用入口          │
│  - （复用）commit-seal.ts · public/accuracy · arena 记分板       │
├──────────────────────────────────────────────────────────────┤
│  γ 决策智能层 (Decision Intelligence)  【新增】                  │
│  - Expected-Utility / Robust / Info-Gap 决策求解器             │
│  - 时机策略（何时动、何时等）· 决策后验追踪                      │
├──────────────────────────────────────────────────────────────┤
│  β 因果前瞻层 (Causal Foresight)  【新增】                       │
│  - Causal Discovery（LLM辅助+统计）· Do-Calculus 引擎          │
│  - Counterfactual / What-if-under-intervention 推演            │
│  - Generative Scenario Simulator（多智能体机制模拟）            │
├──────────────────────────────────────────────────────────────┤
│  α 主动预测层 (Active Forecasting)  【新增】                     │
│  - Uncertainty-Gap 检测器 · 证据采集 Agent 调度（最优实验设计）  │
│  - 长跨度校准（多年期共形区间）· 在线自适应共形(ACI)            │
├──────────────────────────────────────────────────────────────┤
│  v1.x 基座（已就位，复用）                                      │
│  - calibration.ts（经验贝叶斯）· conformal-prediction.ts        │
│  - event-graph-builder.ts · arena.ts · science-layer.ts        │
│  - classical-orchestrator.ts（5书并行GoT）· intelligence/*      │
│  - commit-seal.ts（sha256）· prediction-feedback.ts（飞轮）     │
└──────────────────────────────────────────────────────────────┘
```

### 4.1 新增层与开源技术锚点（2026 真实可用）

| 2.0 新层 | 关键能力 | 开源/学术锚点（2026） | 复用现有 |
|---|---|---|---|
| **Causal Discovery + Do-Calculus** | 从事件图自动推断因果结构；回答"如果 X 发生，E 的概率变多少" | `DoWhy`(微软)、`CausalPy`、`gCastle`(华为)、`causal-learn`、`EconML`；**Causal Summit 2026**；arXiv 2609.11897《Benchmarking Causal Discovery in the Foundation Model Era》(2026-09) | `event-graph-builder.ts`（升级为有向因果边 + 工具变量识别） |
| **Generative Scenario Simulator** | 多智能体模拟事件演化，产出"机制驱动"的结果分布 | `LangGraph`/`AutoGen`（编排）；`AgentSociety`(Piao 2025)、`GenerativeAgents`(Park 2023) 框架 | `classical-orchestrator.ts` 的 GoT 学派共识 + Agent 池直接复用为"模拟角色" |
| **Decision Intelligence** | 在分布上求期望效用/鲁棒/信息间隙最优策略 | `Pyro`(概率编程)、鲁棒优化库、`smooth ambiguity` 模型(Caltech, Pomatto) | `calibration.ts` 输出直接喂入决策层 |
| **Active Forecasting** | 系统自测信息缺口→派 agent/爬虫取证（最优实验设计） | Active Learning（ICML 2026 `ActiveUltraFeedback`, Krause 组）、信息获取 RL | `intelligence/*`（已有 Manifold 抓取）→ 升级为"按需取证" |
| **Long-horizon Calibration** | 多年期诚实区间 + 在线自适应共形 | `MAPIE`（已引入可交换性检验、LLM-as-Judge 用例）、**ACI 自适应共形**(Gibbs & Candès)、加权共形(分布偏移) | `conformal-prediction.ts`（加 ACI 在线校正） |
| **Certified Probability Protocol** | 开放签发/验证"带证书的概率"；可锚定、可引用 | OpenTimestamps（去中心化时间戳）、W3C Verifiable Credentials 思路 | `commit-seal.ts` + `public/accuracy` |
| **Automated Outcome Verification** | 多模态（新闻/CV/卫星）自动判定事件结局，降低人工成本 | CV/NLP 事件抽取（2026 多模态 LLM）、卫星图像变化检测 | `prediction-feedback.ts`（结局判定入口） |
| **Federated / Personalized Calibration** | 跨用户隐私保护地聚合校准，个性化先验 | 差分隐私(DP)、联邦学习 | `calibration.ts`（加 DP 噪声聚合） |
| **Meta-Forecaster (RL from Verification)** | 用记分板真实样本训练"元预测器"，自我进化 | RLVR for calibrated forecasting（awesome-agentic 2026-06 收录）、proper scoring rule 梯度 | `arena.ts` 飞轮 + `PredictionFeedback` |

---

## 五、分三阶段落地方案（具体、可验收）

> 排序铁律：**先关地基（α 前置）→ 再做 β 因果 MVP → 最后 γ 决策与协议化**。任何跳过 α 前置的 2.0 都是空中楼阁。

### 阶段 α — 地基闭环（0–30 天，必须先做）

**目标**：让已写好的代码真正到用户、产生真实样本、补齐 substrate。

| # | 任务 | 关键动作 / 开源依赖 | 验收标准 |
|---|---|---|---|
| α-1 | **部署上线** | owner 重生成 Vercel Token 或确认 GitHub webhook；`ci-deploy.mjs` 触发生产部署 | `GET /accuracy`=200，首页旗号已换，部署探针 5 分钟内告警 |
| α-2 | **冷启动样本注入** | 写 `seed-corpus-backfill`（用 Manifold/Metaculus 已结算市场回填 `PredictionFeedback`，**重放真实已发生结局，非编造**）；加 seed 账号跑通 Arena | `PredictionFeedback.verified > 100`，三个仪表盘非空态 |
| α-3 | **OCR 补 3 本空壳书** | 接入 OCR（PaddleOCR / 微信 OCR / Tesseract 中文）补全《子平真诠》《滴天髓》《穷通宝鉴》 | 3 本实体文本 ≥ 1000 行，旺衰/格局/调候 Agent 有素材 |
| α-4 | **校准飞轮对账跑通** | 跑 `calibration-backfill` 修复 DDL 大小写静默失败；接监控 | dry-run 显示 pending=0，飞轮 N_verified/N_total 真实增长 |
| α-5 | **公开验证页 + 时间戳锚定** | 新增 `/verify/[commitHash]` 公开页；`commit-seal.ts` 输出接 OpenTimestamps | 任意封存 ID 可公开验真、不可篡改，第三方可读 |

**α 阶段不新增任何科学能力，只把已有能力"通电"。这是 2.0 的绝对前提。**

### 阶段 β — 2.0 因果前瞻 MVP（30–90 天）

**目标**：上线"为什么 + 如果干预会怎样"的最小可用因果层，与现有引擎并联。

| # | 任务 | 关键动作 / 开源依赖 | 验收标准 |
|---|---|---|---|
| β-1 | **事件图→因果图升级** | `event-graph-builder.ts` 增加有向因果边 + LLM 辅助因果发现（DoWhy/gCastle 兜底统计检验）；输出结构因果模型(SCM) | 每个事件产出可读因果图（节点/边/置信），人工抽检合理 |
| β-2 | **反事实/干预推演 API** | 实现 `do(X)` 效应估计（后门/前门调整，DoWhy）；`WhatIfUnderIntervention` 接口 | 用户问"若 X 发生，P(E) 变多少"返回带区间的效应量 |
| β-3 | **主动预测（信息缺口取证）** | 加 Uncertainty-Gap 检测：当某事件置信区间过宽→派情报 Agent 定向取证（复用 `intelligence/*`）；接 Active Learning 调度 | 系统自动发起≥1 次证据采集/事件，区间宽度收敛 |
| β-4 | **多年期校准区间** | `conformal-prediction.ts` 加 ACI 在线自适应 + 长跨度分桶校准（MAPIE 加权共形应对分布偏移） | 长跨度（>1 年）预测仍报告诚实宽区间，不谎称精确 |
| β-5 | **古典先验桥（神经符号）** | 形式化：五行生克/十神作为**符号化贝叶斯先验**，与校准后验做 principled 融合（不是加权平均）；权重全透明 | 古典分量在输出中可单独剥离查看，不污染事件轨宣称 |

**β 阶段使 OracleMind 成为"第一个能解释为什么的预测引擎"——市场空白。**

### 阶段 γ — 决策智能与协议化（90–180 天）

**目标**：把概率变成行动，并把"带证书的概率"变成行业标准。

| # | 任务 | 关键动作 / 开源依赖 | 验收标准 |
|---|---|---|---|
| γ-1 | **决策智能层** | 在已校准分布上求期望效用/鲁棒/信息间隙最优策略（Pyro + 鲁棒优化）；输出"做什么 + 何时做 + 置信" | 决策建议可回溯到分布与效用假设，B 端可用 |
| γ-2 | **生成式情景模拟** | 多智能体模拟事件演化（LangGraph 编排 + AgentSociety 思路），产出机制驱动的结果分布，与统计预测交叉验证 | 模拟分布与统计预测在已结算事件上一致率可查 |
| γ-3 | **Certified Probability Protocol** | 开放"签发/验证带证书概率"的 API + 文档；证书含共形区间+校准样本量+封存 ID；接 OpenTimestamps；发布规范 | 第三方可在自己系统签发/验证 OracleMind 格式证书 |
| γ-4 | **自动化结局验证** | 多模态（新闻/CV/卫星）自动判定事件结局，降低人工回填成本，放大账本 | 自动验证占比 ≥ 50%，人工复核仅兜底 |
| γ-5 | **联邦个性化校准 + 元预测器** | DP 聚合跨用户校准；用 `PredictionFeedback` 真实样本 RL 训练元预测器（RLVR for calibration） | 个性化先验提升冷启动用户校准；元预测器 Brier 优于静态基线 |
| γ-6 | **学术/媒体引用入口（活体记分板）** | 公开发布数据集版本 + 可引用报告（"人类优势域地图"） | 至少 1 篇外部引用/报道 |

**γ 阶段使护城河从"私有数据"升级为"行业标准 + 自进化元预测器"——赢者通吃。**

---

## 六、风险与红线（保持 Precision Over Hype）

1. **因果断言不可越界**：反事实/干预效应只在**事件轨**对外宣称，且必须附样本量与区间；个人轨永不出现"准确率/因果"。
2. **古典先验权重透明**：β-5 的符号桥必须可剥离、可审计，避免"玄学黑箱"反噬可信度（这恰是 v1.x 已建立的优势，2.0 不能丢）。
3. **α 前置不可跳过**：没有部署/样本/substrate，β/γ 全部是 demo，不是产品。
4. **协议化需真去中心化**：Certified Probability Protocol 若要成为标准，锚定必须接 OpenTimestamps 等去中心化方案，不能只存自家数据库（否则"可验证"是伪命题）。
5. **决策层不污染校准**：γ-1 决策订阅是 B 端高价层，但**核心玩法（事件追踪/校准/概率演化）永久免费**——这是 `CORE-GOALS` 原则三的硬约束，也是护城河地基。

---

## 七、北极星指标建议（2.0 版）

沿用 v1.1 北极星 **WAF × 人均已结算预测数**（校准数据是唯一护城河）。2.0 新增两个先行指标：

- **因果覆盖率**：已结算事件中带可读因果图的比例（β 层健康度）。
- **决策采纳率**：B 端决策建议被引用/采纳的次数（γ 层健康度，且因是 B 端不污染 C 端校准）。

> 拒绝任何"付费数"作为先行指标——金钱会让玩家保守、刷分、回避难题，自毁校准纯度。

---

## 八、专家结语

OracleMind 今天最珍贵的不只是 85,562 行工程，而是它**无意中凑齐了下一代预测范式所需的全部稀缺零件**：校准内核（诚实）、封存账本（时间不可压缩）、人机 Arena（人的私有信息）、古典结构先验（符号框架）。大厂有算力没这些零件，创业公司有零件没这套工程。

**真正的竞争不在"谁算得更准"，而在"谁先把'概率'升级为'因果前瞻 + 决策智能'，并把它标准化成行业可信层"。** 按 α→β→γ 三阶段执行，OracleMind 有机会从"一个造好了的预测工具"跃迁为"预测的下一代基础设施"——这在 2026-10 的全球市场，是无人占据的高地。

---

*本报告基线取自 2026-10-15 对 `C:\Users\xing\Desktop\oraclemind` 的实地审计；外部技术锚点取自 2026 年公开文献与开源项目（已在正文标注）。所有 2.0 新增能力均以复用 v1.x 现有模块为前提。*
