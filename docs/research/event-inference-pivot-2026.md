# 战略评估：从"人个体推演"转向"事件发展推演"作验证旗舰

> 日期：2026-08-13
> 背景：用户提出——验证应优选**事件**而非**人**（事件客观、好把控）；下一步开辟**事件发展推演**，用情报库优势；重点验证**现代推演方法在事件上是否更有优势**；人的推演受个性/情绪等不可知因素干扰，无法纯数理。
> 合规红线：对外禁用 八字/算命/fortune-telling/divination/horoscope；事件推演须 framing 为「决策支持 / 概率演化分析」，绝非占卜。

---

## 0. 一句话 verdict（不附和）

用户的三点判断**都成立且被文献支撑**：事件有有限时域内可客观解析的 ground truth，正好补上我们最大的窟窿（生产 11 预测 / 0 outcome）；现代数据+情报方法在事件上的确有优势（尤其系统数据类）。但补一条关键反证据：**裸新闻访问对 AI 预测无显著帮助**（ForecastBench），所以"情报补偿"必须是**结构化策展**，不是灌水。人的推演保留为**概率倾向场**（本就不是确定性），不拿它赌准确率。

---

## 1. 为什么事件推演是对的（证据）

| 证据 | 数值 | 含义 |
|---|---|---|
| 事件在有限时域解析、无需人工标注 (hivebook.wiki) | — | **直接解决 0 outcome 瓶颈**：世界自己出答案 |
| 超级预测员 Brier (Tetlock/GJP) | 0.18–0.22 | 可量化"准度"的基准 |
| 预测市场 (Polymarket/Kalshi) | 0.14–0.16 | 近实时、自动聚合 |
| AI/LLM 检索增强预测 (predscope 2025-26) | 0.16–0.18 | **现代方法已具竞争力** |
| — 其中经济/系统数据类 | AI 0.12 vs 市场 0.11 | **现代方法在系统化数据上几乎追平甚至占优** |
| 朴素基线率 (base rate) | 0.25（二元下限） | 任何正经模型都应显著低于此 |

结论：事件域是可被**客观度量准确率**的，且现代方法（集成+检索+校准）已证明有效——这正是验证"现代推演方法"的可行战场。

---

## 2. 对用户三个论点的逐条评估

### (a) 验证选事件不选人 — ✅ 完全同意
- 人个体结局模糊、长程、主观（"事业顺不顺"无解析日）；事件有 crisp resolution（"X 国 2027 前是否签 Y 条约" → 0/1）。
- 这把 engine-audit 从"只验工程正确性"升级为"验真实预测准度"（接 resolved outcome）。

### (b) 事件推演 + 情报库优势 — ✅ 同意，但补反证据
- ✅ PolySwarm（23 实时源+10 聚合）、AIA Macro Forecaster（agentic 检索补上下文, Brier 0.1076≈超级预测员）证明：事件有**公开信号可抓**，情报补偿在此真正生效；人推演无公开信号 → 现代方法无抓手 → substrate 主导 → 难验证。用户直觉正确。
- ⚠️ **反证据**（ForecastBench, Karger et al. 2024）：17 个顶级 LLM 接最新新闻后预测**未显著改善**，且仍落后超级预测员（AI 0.111 vs 超预 0.093）。启示：**情报须结构化/策展 + 聚合 + 校准**，裸 dump 新闻不是胜点。我们的 IntelligenceStore 必须做"精选特征"，不是"全文检索灌入"。

### (c) 人推演有不可知因素（个性/情绪）— ✅ 同意机制局限，但澄清边界
- 个性/情绪部分可建模（心理测量/行为模型）但高方差、不可由生辰 substrate 还原 → 用户说得对。
- 但澄清：OracleMind 人推演**本就是概率倾向场（propensity），非确定性预测**，从不声称"算出性格/命运"。差距在**验证**（无 ground truth），不在机制。→ 人推演保留为品牌叙事层（概率场/能量基调），**不拿它作为准确率 claim 的载体**。

---

## 3. 双轨定位（保住"古代框架+现代数据科学"品牌）

| 维度 | 人个体推演 | 事件发展推演（新旗舰） |
|---|---|---|
| 主驱动 | 古代 substrate 主导（四柱→子平倾向场） | **现代情报+集成主导**（可选"周期共振"作特征） |
| 输入 | 生辰（birth datetime） | 事件陈述 + 结构字段（域/区/时域/分辨率标准）+ 情报上下文 |
| 时间锚 | 生辰四柱 | 事件起点时间 → 干支/五行/周期相位（**中性 framing：时间相位共振，非算卦**） |
| 验证 | 饥饿（无 ground truth） | **饱满（resolved outcome → Brier）** |
| 合规风险 | 中（需严防算命话术） | 低（= 决策支持/概率演化分析） |

> 用户"现代方法在事件上更有优势"→ 对应上表：事件轨把权重从古代 substrate 移到现代方法，正好让现代方法唱主角、可被实测。

---

## 4. 诚实风险 / 必须回答的 blocker

1. **情报源瓶颈（最关键）**：connector 列表几乎全 disconnected，用户打不开海外站点 → 事件推演要的"活情报"从哪来？
   - 选项 A：策展静态语料（我们先建结构化事件知识库，可控但覆盖有限）
   - 选项 B：推理时独立"情报检索层"（需引入 LLM/检索，破坏现有引擎 deterministic/no-LLM 设计 → 须做成独立旁路，只产结构化特征喂入）
   - 选项 C：用户/访客补事件上下文（众包）
   - **须用户定夺**：优先哪条？这决定事件引擎能否真正"用上情报"。
2. **分辨率标准必须 crisp**（predscope 失败模式 4）：主观标准（"X 是否算成功"）校准最差 → 事件须定义可机器解析的 resolution criterion。
3. **不能先声称"现代方法更优"**：须先建事件引擎 + 收结局 → 实测 Brier 对比基线，才算数。这是 empirical test，不是预设结论。

---

## 5. 架构提案（事件推演模块，复用现有层）

```
事件输入(event, domain, horizon, resolution_criterion, [intel_context])
   ├─[复用] StatisticalLayer (蒙特卡洛集成/gauss)        ← 分布而非单点
   ├─[复用] MultiAgentLayer (事件角色 Agent: 地缘/经济/统计/怀疑者…)  ← 替换现人角色
   ├─[复用] calibration.ts (经验贝叶斯收缩 + recommendedConfidenceCap)
   └─[新增] IntelligenceStore.retrieve(event) → 结构化特征向量
            fusion: p = w1·ensemble + w2·intel   (w 仅在有 outcome 时学习)
                   │
   └─[护栏升级] engine-audit 加「真实准度关」:
            resolved outcome o∈{0,1} → Brier / calibration gap vs 基线 0.25
            → 只有改善的情报源/方法保留
   └─[新增] EventOutcomeLedger + resolution cron (到时自动解析→回写→校准)
```

**接线点**：`prediction-engine.ts` 增 `mode: 'event' | 'person'`；事件模式跳过 `tendency-field`（无生辰），改走 `intel + ensemble`；engine-audit 增真实 ground-truth 关。

---

## 6. 分阶段下一步（待用户拍板）

- **Phase 0（决策）**：定情报源路线（A/B/C）；定首批事件类型（建议：可解析的经济/政策/科技发布类，避开主观标准）。
- **Phase 1（建事件引擎）**：`mode:'event'` 分支 + 事件角色 MultiAgent + EventOutcomeLedger schema + resolution cron。
- **Phase 2（接情报）**：IntelligenceStore 策展首批中性源；结构性 retrieve（非裸新闻）。
- **Phase 3（实测闭环）**：跑 20–50 个可解析事件，收结局 → Brier vs 0.25 基线 → 回答"现代方法在事件上是否更优"。
- **同步**：engine-audit 状态接 `/api/command-center` 看板；人推演保留为概率场品牌层。

---

## 7. 来源
- 概率预测 Brier leaderboard / Tetlock: https://hivebook.wiki/wiki/probabilistic-forecasting-benchmarks-for-ai-agents-brier-scored-leaderboards-calibration-metrics-and-byok-submission-patterns
- 预测统计（超级预测/Brier）: https://gitnux.org/forecasting-statistics/
- ForecastBench (AI vs 超级预测员, 新闻无显著帮助): https://forum.effectivealtruism.org/posts/zwzgR8iuFEcJms3Hu/announcing-forecastbench-a-new-benchmark-for-ai-and-human
- 预测市场准确率 2025-26: https://predscope.com/guide/prediction-market-accuracy-data
- PolySwarm / AIA Macro Forecaster / PySR / DoWhy 见 `docs/research/inference-algorithms-math-2026.md`
