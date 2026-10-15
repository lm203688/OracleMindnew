# 板块 4 · 竞技场 Arena（你 vs 人群 vs 引擎）

> 边界：`automation/arena.ts`（1075 行）+ `api/arena/*`（submit/markets/leaderboard）+ `/arena` 页面 + `mirrorArenaPicksToFlywheel()` + `automation/run` cron + 4 套单测。

## 一、流程合理性 / 走通性 / 人类使用习惯

**流程链路**：提交预测 → 对练场结算（你 vs 人群 vs 引擎三方可比 Brier）→ `mirrorArenaPicksToFlywheel()` 把真实结算 Brier 镜像进 `db.predictionFeedback` → 校准飞轮吃到真实样本 → command-center 仪表读取 → `automation/run` 定时对账。

**走通性 / 风险（已实质完成）**：
- **断链 #5（prior 报告点名）已被主动修复**：`mirrorArenaPicksToFlywheel` 真实写回 PredictionFeedback，`getHistoricalAccuracyContext` 读同一张表——飞轮一旦转即生效。
- 有 submit/markets/leaderboard 三 API + 页面 + 4 单测，**架构与测试都齐备**。
- **未走通点**：① 仍 **0 真实用户**，arena 是"空场"；② 市场源来自何处未明——`markets` API 需接真实市场（Manifold/Metaculus）才有"人群 vs 引擎"对照；③ 排行榜无公开化与邀请机制，gamification 价值未释放。

**人类使用习惯**：**"你 vs 人群 vs 引擎"是强留存设计**（类似游戏排位），叠加 `/api/...use-streak` 每日连续——但需实时市场和可见排行榜才好玩；当前空场态对首批用户劝退。

**结论**：架构 9/10，实测走通 2/10（0 用户），gamification 设计 8/10，对照数据源 3/10。

## 二、市场竞品与需求比较

| 竞品 | 模式 | 关系 |
|---|---|---|
| Metaculus 锦标赛 | 社区锦标赛、无金钱 | 方法论标杆，OracleMind arena 更像"个人练习场" |
| PredictIt / Kalshi | 真金（美国合规） | 合规冲突，不可照搬 |
| Manifold | 玩金（免 key API） | **OracleMind 已接入其共识情报**，可直接喂 arena 市场 |
| Good Judgment Open | 超预训练 | 可借鉴其 Brier 文化 |

**需求**：用户要"我和大众/AI 谁更准"的即时反馈与排位；OracleMind 已有骨架，差的是"接真市场 + 公开榜 + 首批冷启动用户"。

## 三、最新开源技术融合机会

- **Manifold API（已用共识）** 可扩展为 arena 的实时市场源（免 key、play-money）。
- **TrueSkill / ELO**：为 arena 排位做技能评分（比单纯 Brier 平均更适合跨人比较）。
- **ForecastBench 评测框架**：把 arena 产出直接对接 ForecastBench 风格的评测，对外宣称"你的水平 vs SOTA AI"。
- **开源排行榜组件**（如 leaderboard 库）：快速上线公开榜。

## 四、单板块提升方案

- **P0-①**：arena `markets` 接 Manifold/Metaculus 真实未结算市场，让"人群 vs 引擎"有真对照。
- **P0-②**：冷启动——用内部/种子账号先跑出可见排行榜，避免空场劝退首批用户。
- **P1-①**：引入 TrueSkill 排位，替代纯 Brier 均值。
- **P1-②**：公开排行榜 + 分享卡 + 邀请机制，释放 gamification 留存。
- **P2**：arena 成绩与"个人战绩/校准证书"打通，形成"练习→证书→排行"闭环。

**板块健康度评分（0–5）**：架构 5 · 实测走通 1 · gamification 设计 4 · 对照数据源 2 · 开源可融合 4 → **综合 3.2**

---

*下一份：M05-智能体编排与提示层*
