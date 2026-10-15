# OracleMind 逐板块提升评估总报告

> 方法：对 `C:\Users\xing\Desktop\oraclemind` 全仓做独立扫描，把项目拆成 **9 个产品板块**，每个板块单独评估 ① 流程合理性/走通性/人类使用习惯 ② 市场竞品与需求 ③ 最新开源技术融合 ④ 单板块提升方案，并打 5 维健康度分（0–5）。
> 配套 9 份独立报告见 `docs/reports/per-module/M01–M09-*.md`。
> 外部标尺截至 2026-10-14（ForecastBench / 玄学 App 市场 / 各开源库）。

---

## 0. 板块拆分依据（来自真实代码边界）

| 编号 | 板块 | 核心代码边界 | 关键 API / 页面 |
|---|---|---|---|
| M01 | 核心校准预测引擎 | prediction-engine + calibration + conformal + forecast-guard + scientific-metrics | /api/predict, /api/forecast |
| M02 | 古典命理融合层 | bazi-engine + classical/(12) + ancient-frame-features + tendency-field | /api/divine, /api/tuivan |
| M03 | 事件语料与知识库 | event-corpus + event-graph-builder + graph/(2) + personal-graph-builder | /api/events, /api/graph |
| M04 | 竞技场 Arena | automation/arena(1075) + api/arena/* + /arena | /api/arena/submit |
| M05 | 智能体编排与提示层 | science-layer + agent-factory + react-reasoner + agent-mesh + modern-deep-analysis(2766) | /api/oracle-core, /api/agent-trace |
| M06 | 情报雷达层 | intelligence/(2) + expansion/marketing/tech-radar chains + weekly-scan | /api/intelligence-gather |
| M07 | 前瞻注册与反作弊 | commit-seal + event-outcome-ledger + job-ledger + calibration-backfill | /api/oracle-core/mirror |
| M08 | 概率演化与个人战绩 | streak + prediction-feedback + quality-evolution + journal | /quality-evolution, /accuracy |
| M09 | 商业/市场/交付自动化 | payment/(4) + billing/credits/referral + scheduler/self-heal/seo | /pricing, /api/payment |

---

## 1. 九板块健康度对比矩阵（0–5）

| 板块 | 架构完整 | 数据走通 | 人类主路径 | 竞品差异化 | 开源可融合 | **综合** |
|---|---|---|---|---|---|---|
| M01 校准引擎 | 5 | 2 | 3 | 4 | 4 | **3.6** |
| M02 古典融合 | 4 | 2 | 3 | 4 | 4 | **3.0** |
| M03 事件语料 | 5 | 2 | 4 | 4 | 4 | **3.4** |
| M04 竞技场 | 5 | 1 | 4 | 2 | 4 | **3.2** |
| M05 智能体层 | 4 | 3 | 4 | 4 | 4 | **3.4** |
| M06 情报雷达 | 5 | 2 | 2 | 4 | 4 | **3.4** |
| M07 前瞻注册 | 5 | 2 | 1 | 5 | 4 | **3.4** |
| M08 概率演化 | 4 | 1 | 2 | 5 | 4 | **3.2** |
| M09 商业交付 | 5 | 1 | 2 | 4 | 4 | **3.2** |
| **均值** | **4.7** | **1.8** | **3.0** | **4.0** | **4.0** | **≈3.3** |

**读图结论**：
- **架构完整度极高（4.7）**——9 板块都"造好了"，无空白模块。
- **数据走通度极低（1.8）**——全局被"0 真实验证样本"卡死：M01/M04/M08 的仪表盘全是空态，M07 自动回写仅覆盖 55 条语料。
- **竞品差异化（4.0）与开源可融合（4.0）都高**——说明"做什么"对了、"怎么借力"也清楚，卡在"跑起来"。

---

## 2. 跨板块三大共性断裂（必须连根拔）

1. **冷启动死锁（M01∩M04∩M08）**：校准证书、arena 飞轮、个人战绩都依赖 `PredictionFeedback` 真样本，而全仓 0 verified。→ 任何单板块优化都救不了，必须**统一注入首批真实样本**（arena 种子账号 + `event-outcome-ledger` 接 GDELT 回填）。
2. **古典 substrate 残缺（M02）**：5 书仅 2 本有真文本、节气为近似值 → 准确性硬伤 + "5 书并行"名不副实。→ 这是**唯一会直接砸用户信任的准确性 bug**，优先级高于所有"锦上添花"。
3. **用户可见度塌陷（M06∩M07∩M08）**：情报锚点、事前封存、个人校准曲线都是强信任资产，但**没有进主 UI / 无公开页 / 空态未设计** → 差异化无法被用户感知，等于没有。

---

## 3. 跨板块优先级路线图

### P0 · 本周（拔断裂 #1/#2，让已有架构产生可感知价值）
- **M02-① 节气 bug**：用 `lunar-typescript` 替换近似边界，加立春边界单测（准确性阻断）。
- **M02-② OCR 补 3 本空壳书**（子平真诠/滴天髓/穷通宝鉴）→ "5 书并行"从表演变真。
- **M03-① 语料 55→150+**：GDELT 历史已解决事件回填，让自动回写高频触发。
- **M01/M04/M08 冷启动注入**：arena 种子账号先跑出排行榜 + 把语料 55 条 + 既有 11 条灌进 `PredictionFeedback`，72h 内校准证书/曲线/战绩有形。

### P1 · 本月（把差异化资产变成用户可感知产品）
- **M07 前瞻注册对外化**：commitHash 锚定 **OpenTimestamps** + 公开验证页 + "已事前封存"徽章（全球唯一"可证明不马后炮"）。
- **M08 校准曲线设 Hero**：一句话"你比大众准 X%" + 强空态引导。
- **M04 TrueSkill 排位** + 公开榜 + 分享卡。
- **M05 LangGraph 重写 pipeline** + token 成本护栏。
- **M06 GDELT/EventRegistry 多源** + 共识"依据卡片"进预测 UI。
- **M09 定价价值叙事** + 增长内容质量门。
- **M01 ACI 在线校准** 替换固定 K 先验。

### P2 · 加固（赢者通吃壁垒）
- **M01 MAPIE** 对照实验验证自研共形层。
- **M03 GraphRAG** 统一古典+现代+图谱检索。
- **M02 命理师人工咨询桥**（对齐灵机/玄易变现）。
- **M08/M04 社交裂变**（战绩分享 + arena 邀请）。

---

## 4. 如果只能做三件事（跨板块最高杠杆）

1. **修 M02 节气 bug + OCR 补 3 书**——准确性是命门，且成本最低（库替换 + OCR）。
2. **打通冷启动数据 injection**（M01/M04/M08 共用一根水管）→ 一次注入，三个仪表盘同时活。
3. **M07 公开验证页 + OpenTimestamps**——把唯一"全球无竞品"的资产变成可对外讲的信任标准。

> 注：2026-10-13 报告点名的"断链 #6（校准证书读错静态表）"**已于本次复扫确认修复**（science-layer 现优先读 `db.predictionFeedback`），故不再列入行动项；arena 断链 #5 亦已修。

---

## 5. 各板块报告索引

- [M01-核心校准预测引擎](per-module/M01-核心校准预测引擎.md)
- [M02-古典命理融合层](per-module/M02-古典命理融合层.md)
- [M03-事件语料与知识库](per-module/M03-事件语料与知识库.md)
- [M04-竞技场Arena](per-module/M04-竞技场Arena.md)
- [M05-智能体编排与提示层](per-module/M05-智能体编排与提示层.md)
- [M06-情报雷达层](per-module/M06-情报雷达层.md)
- [M07-前瞻注册与反作弊](per-module/M07-前瞻注册与反作弊.md)
- [M08-概率演化与个人战绩](per-module/M08-概率演化与个人战绩.md)
- [M09-商业市场交付自动化](per-module/M09-商业市场交付自动化.md)

*本总报告与 9 份分报告构成完整的"逐板块评估 + 提升方案"交付物。*
