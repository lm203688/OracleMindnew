# OracleMind 推演算法与数学理论调研 + 情报补偿架构提案

> 调研日期：2026-08-13
> 目的：回应用户两点诉求——① 找开源推演新算法与世界顶级数学难题/理论；② 评估"更强数据库 + 情报补偿用户输入不足"的可行性。
> 合规红线：对外禁用 八字/四柱/算命/fortune-telling/divination/horoscope；统一用 概率场/古代推演/推演原型/能量基调。

---

## 0. TL;DR（诚实结论）

- 用户命题"只要能演算到一定准确率的模型，这套理论才是可行的"= **方向正确（经验主义唯一诚实标准），但前提是准确率必须拿真实结果量**。现状：生产 11 预测 / 0 outcome 回报 → 准确率目前不可计算。engine-audit 五道关只验证"现代演算方法工程正确"，不验证"预测准不准"。
- "更强数据库 + 情报补偿"= **有产业先例的真需求**（AIA Macro Forecaster、PolySwarm 均用检索补上下文）。但无 outcome 反馈时，加外部特征=高伪相关风险，必须做成"可审计、逐源 Brier 打分"。
- 混沌理论给定物理边界：长程人生轨迹的"确定性准确率"在数学上不存在 → 产品必须维持**概率场**定位（亦契合公开红线）。

---

## 1. 开源推演/预测算法与平台（实地检索）

| 项目 | 核心方法 | 与 OracleMind 映射 | 可借鉴点 |
|---|---|---|---|
| **PolySwarm** (github.com/defidaddydavid/polyswarm, MIT) | 12 Agent 多角色辩论 + 10 种聚合（贝叶斯更新、IARPA 极值化、Prelec "Surprisingly Popular"、对数意见池、Cooke 经典模型）+ Brier 逐 Agent 校准追踪 | 已有 MultiAgentLayer(10 Agent 共识)，但**仅均值聚合、缺校准追踪** | 加 per-agent Brier；引入 extremized / Surprisingly Popular 聚合 |
| **WeatherNext** (Google DeepMind, 2026-08 Nature + 开源) | 1000 成员概率集成(FGN)，<1min 出分布，+24h 预警提前量 | StatisticalLayer 仅单层 gauss，缺**分布集成** | 输出概率分布而非单点；tail-risk 情景 |
| **AIA Macro Forecaster** (Bridgewater AIA Labs, arXiv 2511.07678) | 四阶段：agentic 检索上下文 → 跨模型集成 → 监督者调和 → 统计校准；Brier 0.1076 ≈ 人类超级预测员 | **"情报补偿"范本**：先检索补上下文再推演 | `retrieveContext(input)` 直接对标其 stage-1 |
| **PySR / Symbolic Regression** (Miles Cranmer, 已有 scripts/symbolic-pilot.py) | 进化算法从数据发现闭式方程（island model + Pareto 前端） | 用于"演算逻辑发现" | outcome 数据到位后自动发现维度公式 |
| **DoWhy / PyWhy / EconML / causal-learn** (Microsoft) | 因果推断四步：建模→识别→估计→反驳(refute)；图形因果模型(GCM)根因/分布变化归因 | 维度间因果结构、伪相关排查 | 用 GCM 反驳"情报源→维度"虚假链路 |

来源：
- PolySwarm: https://dev.to/defidaddydavid/i-built-a-12-agent-ai-swarm-that-debates-crypto-predictions-open-source-1k98
- WeatherNext: https://www.unite.ai/googles-weathernext-2-gains-a-full-day-of-cyclone-warning-goes-open-source
- AIA Macro Forecaster: https://github.com/NikhilSKashyap/aia-macro-forecaster ; arXiv:2511.07678
- PySR: https://www.emergentmind.com/topics/pysr-method
- DoWhy/PyWhy: https://py-why.github.io/ ; https://petergtz.github.io/dowhy/v0.8/index.html

---

## 2. 顶级数学难题与理论（按与推演相关性排序）

| 问题/理论 | 领域 | 对推演的启示 |
|---|---|---|
| **混沌理论 / 蝴蝶效应 / 李雅普诺夫时间** | 动力系统 | **最相关 + 最诚实边界**：初始微小误差指数放大→长期预测数学上不可能。推演必须输出**概率分布 + 诚实置信上限**（calibration.ts 的 recommendedConfidenceCap 已朝此走），禁假装确定性长程预测 |
| **Kolmogorov 复杂度 / Solomonoff 归纳 / MDL** | 算法信息论 | **情报补偿理论根基**：最优预测器按 2^(-程序长度) 给先验（奥卡姆剃刀严谨化）。情报库=**压缩"仅由用户输入推断"的残差描述长度**；MDL 是工程可用近似 |
| **P vs NP** | 计算复杂度 | 某些"最优推演"若属 NP 只能近似/启发式（本就是启发式融合） |
| **Navier-Stokes 存在性与光滑性** | 流体/湍流 | 高维人生轨迹≈湍流，奇点/突变不可解析预测→用集成而非闭式 |
| **黎曼假设** | 数论/分布 | 分布零点结构 → 概率分布的"签名/漂移护栏"（engine-audit E 关） |
| **杨-米尔斯/质量缺口、Hodge、BSD** | 数学物理/代数几何 | 与本项目直接相关性低，列为理论储备 |

来源：千禧年大奖难题 https://baike.sogou.com/v10004854106.htm ；混沌理论 https://infogalactic.com/info/The_order_of_choas ；AIT https://www.envisioning.com/vocab/ait-algorithmic-information-theory

---

## 3. "情报补偿"架构提案

**问题定义**：用户输入极稀疏（出生年 + 目标维度）= 初始条件测量精度极低。混沌理论：输入越粗，残差不确定性越大。情报库目标不是"算更准"，而是**用外部上下文把残差不确定性压缩到可管理带宽**——AIT/MDL 语言。

**架构（现有引擎插一层，不动古典 substrate）**：

```
用户输入(input: birthYear, target)
   ├─[现有] tendency-field.ts (子平映射 → 维度倾向场)  ← 主驱动
   ├─[现有] StatisticalLayer / MultiAgentLayer (确定性, 无 LLM)
   └─[新增] IntelligenceStore + retrieveContext(input)
            ├─ 世代/经济周期代理统计 (按 birthYear band)
            ├─ 周期性/季节代理 (中性 framing, 非占卜)
            ├─ 文献领域先验 (RAG over 策展语料)
            └─ 匿名化真实回报聚合 (金矿, 来自 PredictionFeedback)
                   │
            fusion: final = w1·tendency + w2·ensemble + w3·intel
            (w 仅在 outcome 数据存在时才学习; 否则冻结为先验)
                   │
            └─[护栏] engine-audit 逐源 Brier 贡献追踪
                  → 仅改善(或不恶化)留出校准的源保留
```

**接线点**：`prediction-engine.ts` 融合公式 `0.7*tendency + 0.3*(L2/L3)` 改为含 `intel` 三项；`intel` 缺数据时权重 0（退化回现状，零风险）。

---

## 4. 诚实评估（机制真实 vs 对你概率高低）

- **机制层**：多 Agent 聚合、集成、因果反驳、MDL 压缩均为**真实可工程化**方法，非噱头。接入提升"演算工程质量"。
- **准确率层**：**当前无法证明任何准确率**（0 outcome），是事实缺口非算法问题。
- **物理边界**：混沌理论给定不可突破上限——长程人生轨迹"确定性准确率"数学上不存在 → 对外须维持**概率场**定位（契合公开红线）。
- **情报补偿风险**：无反馈时加外部特征=高伪相关风险，须"先建审计、再放量"，逐源 Brier 验证。

---

## 5. 分阶段落地建议（下一步）

- **Phase A（无需 outcome）**：建 `IntelligenceStore` schema + 接入 2–3 个中性高信噪比源（世代统计、周期代理、文献先验）；`intel` 默认权重 0，不影响现有输出。
- **Phase B（需少量 outcome）**：`retrieveContext` 接 fusion；engine-audit 加"逐源 Brier 贡献"关。
- **Phase C（反馈闭环通电后）**：真实回报数据学习 w 权重 + PySR 发现维度闭式 + 因果反驳伪链路。

---

## 6. 待用户决策/执行项

- [ ] 是否批准 Phase A（建 IntelligenceStore + 接入中性源）？
- [ ] engine-audit 状态是否接 `/api/command-center` 公开看板（上次已提议）？
- [ ] PayPal $4.99 真实测试款仍须用户出手（助理无法代付）确认收款到账。
- [ ] 真实用户回报闭环（ProductionFeedback）仍饥饿，需真实点击解锁校准。
