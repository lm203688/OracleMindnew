# OracleMind · AI 目录 / 平台提交材料

> 目标：把 OracleMind 通过线上平台嫁接出去，增加曝光与引流（用户打不开海外站点，由 AI 备料、用户确认后执行）。
> 公开资产已就绪：`/api/public/field`（免鉴权 CORS 端点）、`/api/openapi.json`（OpenAPI 文档）、`/embed.js` + `/widget`（可嵌入概率场卡）。

---

## 1. 一句话定位（对外，禁命理/占卜词）

**OracleMind** — 一个把古代哲学框架与现代数据科学融合的多维概率场引擎。输入一个事件或出生信息，得到可复现的「综合倾向指数」（确定性公式，非频率派概率），作为决策参照。

EN: *OracleMind — a multidimensional probability-field engine that fuses an ancient philosophical framework with modern data science. Input an event or birth profile; get a reproducible Composite Tendency Index as a decision reference.*

**新 GEO 方向（2026-08-14 定）**：面向**预测 / 决策情报社区**（Metaculus、Manifold、Kalshi、Polymarket、PredictIt、LessWrong、r/Forecasting、r/predictionmarkets、体育 analytics 社区），定位为「交叉验证事件判断的可复现概率场参照」——补充参考，不是下注秘籍，不碰彩票（彩票均匀随机、无信号，碰了违反 Precision Over Hype 且重引 PayPal AUP 冻结风险）。

---

## 2. 可嵌入 widget 代码片段（给第三方站点主）

```html
<script
  src="https://oraclemind.cc/embed.js"
  data-oraclemind-widget
  data-mode="event"
  data-question="Will the Fed cut rates before Jan 2025?"
  data-prior="0.7"
></script>
```

- `data-mode`: `event`（事件，需 `data-question` + `data-prior` 客观基础率）或 `person`（人生，需出生 + `data-target`）。
- 免鉴权、跨域、近零成本；iframe 高度 440px，圆角卡片。

---

## 3. 开发者接入（公开 API）

```
POST https://oraclemind.cc/api/public/field
Content-Type: application/json

{ "eventDescription": "Will X happen?", "eventPrior": 0.7 }   // 事件模式
{ "birthYear": 1990, "birthMonth": 6, "birthDay": 15, "target": "career" }  // 人生模式
```

文档：https://oraclemind.cc/api/openapi.json

---

## 4. 目录清单（状态：待执行）

### A. 预测 / 决策情报社区（新方向，优先，合规安全）

| 社区 | 入口 / 触达方式 | 操作要点 |
|---|---|---|
| **Metaculus** | https://www.metaculus.com / 其论坛 | 无付费提交；在相关赛事评论区以"可复现概率场参照"身份分享方法 + 链接，建权威；先贡献高质量评论再带链接 |
| **Manifold** | https://manifold.markets | 同上，参与问答市场讨论，主页简介挂 oraclemind.cc |
| **Kalshi** | https://kalshi.com | 合规预测市场；在相关主题社媒/X 以"交叉验证参照"引述，勿称下注建议 |
| **Polymarket** | https://polymarket.com | 同上；X/Discord 触达，强调"参照、非建议" |
| **PredictIt** | https://www.predictit.org | 同上 |
| **LessWrong** | https://www.lesswrong.com | 发文/评论谈校准与 Brier（已有 `forecast-accuracy-calibration.md` 作弹药），理性主义受众高度匹配 |
| **r/Forecasting** | https://www.reddit.com/r/Forecasting | 发交叉验证方法论帖 + 公开 API 链接 |
| **r/predictionmarkets** | https://www.reddit.com/r/predictionmarkets | 同上 |
| **体育 analytics 社区**（r/soccer、r/nba、r/MLS 的分析帖） | Reddit/子论坛 | 以"概率参照"参与，不碰 r/sportsbook 等下注贴士站 |

> 这些社区的核心价值主张（已在 `public/geo/cross-check-event-forecasts.md` 成文）：**作为预测者已有概率判断的交叉验证参照**，而非竞争者或下注秘籍。合规、且与我们"事件推演=客观可验证"闭环自洽。

### B. 通用 AI 工具目录（维持，待用户账号）

| 目录 | 提交入口 | 要求 | 状态 |
|---|---|---|---|
| Product Hunt | https://www.producthunt.com/submit | 需账号 + 预告 | 待用户账号 |
| Toolify | https://www.toolify.ai/submit | 表单/账号 | 待用户账号 |
| Futurepedia | https://www.futurepedia.io/submit-ai-tool | 表单 | 待用户账号 |
| There's An AI For That | https://theresanaiforthat.com/submit | 表单 | 待用户账号 |
| AI Directories (aidirectories.co) | 付费收录 | 付费 | 待用户决定 |
| SaaS Hub / AlternativeTo | https://alternativeto.net/ | 账号 | 待用户账号 |
| GEO/llms.txt 已铺（站内） | /api/openapi.json + public/geo/*.md（含 cross-check-event-forecasts.md） | 已上线 | ✅ |

> 只要有任一目录提供「开放提交 API + token」，我可代提交；其余需用户在对应站点登录后操作。把账号交给我或贴上提交 token 即可。

---

## 5. 提交文案（复制即用）

**Short (≤280 字符)**
OracleMind — a probability-field engine fusing ancient philosophy + modern data science. Get a reproducible Composite Tendency Index for any event or life dimension as a decision reference. Free embeddable widget & public API. https://oraclemind.cc

**Long (目录描述)**
OracleMind is a multidimensional probability-field engine that combines an ancient philosophical framework with Monte-Carlo simulation, multi-agent consensus and empirical-Bayes calibration. Every reading is deterministic and reproducible (same inputs → same index), and is delivered as a Composite Tendency Index on a [0,1] scale — a philosophical decision reference, not a prediction of fixed fate. It ships a free, no-auth public API and an embeddable probability-field widget so any site can surface a decision card. Event inference is anchored on publicly verifiable base rates and validated against a corpus of resolved events.

**Tags / Categories**: AI Decision Tool, Forecasting, Probability, Analytics, API, Widget, Productivity.

**Forecaster-facing (EN, for Metaculus/Manifold/LessWrong/Reddit)**
> OracleMind is a reproducible probability-field engine you can use to *cross-check* your event forecasts. Supply your own base rate as `eventPrior`; it layers live public-web intelligence (entities, sentiment, source diversity, risk/opportunity signals) onto a deterministic Monte-Carlo + multi-agent core, and returns a Composite Tendency Index plus the evidence behind it. Not a betting tip, not a market-beating claim — a transparent reference to challenge your own assumptions. Free public API + embeddable widget: https://oraclemind.cc/api/openapi.json

---

## 6. 自动化提交 helper（有开放 API 时用）

```bash
# 模板：若目录提供开放提交 API，替换 URL/KEY 后运行
curl -X POST "https://<directory>/api/submit" \
  -H "Authorization: Bearer $DIR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"OracleMind","url":"https://oraclemind.cc","description":"A multidimensional probability-field engine fusing ancient philosophy with modern data science.","tags":["AI","Forecasting","API","Widget"]}'
```

> 当前所有连接器均 disconnected，且无目录提供免登录开放提交 API，故本步暂挂起，待用户提供账号/token 后批量执行。
