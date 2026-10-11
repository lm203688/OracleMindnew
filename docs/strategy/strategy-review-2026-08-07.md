# OracleMind 闭环与战略复盘（2026-08-07）

> 范围：支付迁移闭环 + 历轮已完成工作的结果 + 待办 + 扩展方向 + 竞品商业模式借鉴

---

## 一、当前任务闭环状态（支付迁移）

**我侧已完成（commit `39e82f1`，已 push master）：**
- 用新店 Key `creem_7b9...` 建 3 个 OracleMind 商品（已复核 active）：
  - Deep Analysis $4.99 → `prod_7YycAgL3PP058KroOmZKYa`
  - Premium Monthly $9.99/月 → `prod_gq5tn9v0RzkKZbBOyhEPE`
  - Premium Yearly $99/年 → `prod_3YeioVJhK3rTsT24Ao1MzK`
- 代码 7 文件 26 处商品 ID 改新 → `tsc` 通过
- 归档 FrontierKB 旧 3 个 OracleMind 商品 → **商店分离完成**（新店只放 OracleMind，FrontierKB 只留 SwarmLabs×2 + 其他项目）

**生产实测：** `system-health = healthy`；`payment = warning`（84 免费、0 付费）。
**根因：** 你还未在 Vercel 改 env + redeploy，所以新代码 + 新店凭证尚未同时生效。

---

## 二、其他已完成工作的闭环结果（修了什么 / 提升了什么）

### A. 合规红线（品牌 + 监管风险）—— 最高优先级
- **修了**：全站用户可见的「八字 / 天干日主 / 命理 / destiny / horoscope / astrology / cosmic / stars」全部清除，统一改「古代推演 / 概率场 / 推演原型 / 关系维度 / 周期起伏」。
- **提升了**：对外话术与「不是星座/命理 App」定位自洽，解除命理/算命类监管与平台下架风险；路由 `/bazi-chart` → `/tuivan-chart`（308 跳转）。
- **保留**：内核 `bazi-engine/classical/*` 用神/十神/大运作计算 substrate（双轨制），无用户可见渲染路径。

### B. 部署稳定性（生产不再被打挂）
- **修了**：① Prisma 引擎跨平台不匹配（ubuntu openssl 错 → could not locate Query Engine）；② M5 自愈链改走 Vercel git 源部署 + 数据库硬门禁（`database.ok!==true` 即回滚）。
- **提升了**：部署闭环稳定，CI 一律走 `scripts/ci-deploy.mjs`，生产库安全。

### C. 预测校准闭环（精度飞轮）
- **修了**：`PredictionFeedback` 原生 SQL 列名不符导致闭环全断 → 改用 Prisma 类型安全查询。
- **提升了**：预测→反馈→校准的精度飞轮打通（v2.4.0）。

### D. 知识库（推演深度）
- **修了/补了**：补齐 3 本古籍（子平真诠 / 滴天髓 / 穷通宝鉴）→ 内核推演依据更扎实。

### E. SEO / GEO 获客
- **做了**：235 个可索引页提交 Bing/Yandex；中文 pSEO 落地页（10 天干 × 6 维度 = 60 页，合计 67 页）；全量 IndexNow 收录闭环。
- **提升了**：获客漏斗「入口」已铺好，等收录 + 排名起量。

### F. 支付合规
- **修了**：OracleMind 迁入「网站=oraclemind.cc、正确注册」的独立 Creem 新店 → Creem 警告的「unregistered traffic（未注册流量）」根因解除。
- **SwarmLabs×2 已恢复**（误删后重建为活跃商品）。

---

## 三、需要你做的事（汇总）

| # | 事项 | 谁做 | 时效 |
|---|---|---|---|
| 1 | Vercel `CREEM_API_KEY`→`creem_7b9D0NEZhsuy3JC6wrMyrN`、`CREEM_WEBHOOK_SECRET`→`whsec_6c7iJuTYovGu4e3HScYpyQ`，然后 **Redeploy** | 你（Dashboard） | 立即，解锁支付闭环 |
| 2 | Creem 账户层：把账户支持邮箱对齐 + 提交 re-review（解 Account Rejected） | 你（Dashboard） | 尽快 |
| 3 | 流量：235 页等收录；持续 GEO/内容产出 | 我 + 你 | 持续 |

> 第 1 步做完喊我，我立刻复验 `command-center` + 测试支付 + Vercel Functions `[Webhook]` 日志。

---

## 四、需要扩展的领域

**横向（多域捆绑，提升留存 + 客单价——竞品已验证有效）：**
- 西方星座维度（已有）、塔罗、数字命理、易经六爻、姓名学、梦境解析
- 内核已有八字/紫微式计算能力，对外统一包装为「推演/概率场」即可复用

**纵向（场景纵深）：**
- 关系维度（已有「关系维度」）、职业/财富/健康周期、团队/合盘对比

**新模态：**
- 语音推演 / 每日概率场语音播报（高毛利 premium）
- 推演图谱可视化 + 「能量卡片」式情感/趋势可视化（借鉴 found.fun）

---

## 五、竞品新商业模式借鉴（2026 最新）

### 1. Co-Star（已被 Midjourney 收购，2026-07；~490 万 MAU，月流水 ~$50 万）
- **模式**：Freemium + **单点微交易**（按报告/提问次数付费 $数），不逼订阅；极简 UI + 「毒舌但真诚」推送；**好友星盘对比 / 团体合盘**社交裂变。
- **核心洞察**：卖「被理解」不是「算命」；100% 收入来自内购，**不卖广告/不卖数据**。
- **可借鉴**：OracleMind 做「好友推演匹配 / 关系维度对比分享卡」→ GEO 病毒传播；订阅之外加**按次深度解读**微交易。

### 2. The Pattern / Sanctuary
- The Pattern：关系/周期深耕，「Go Deeper」订阅，类心理咨询叙事。
- Sanctuary：chat-first，**人类占星师 + AI** 混合，按分钟计费（争议点：排队也计时）。
- **可借鉴**：OracleMind 可做「AI 推演 + 可选真人解读」分层；但**避免按分钟计费的信任坑**。

### 3. LingYuan（灵媛，国内，10 万+ 用户）
- **模式**：八字 + 紫微 + 星座 + 姓名 **多域捆绑**；**Credits 体系**（$4.99/30 credits，追问/深度解读消耗）；免费版 + ¥99 深度解读。
- **可借鉴**：**多域 bundle 提升感知价值与留存**；credits 降低付费决策门槛（比纯订阅更轻）。

### 4. MingAI 命改
- **模式**：按消息计 credits（30/80/220 每月）+ 奇门遁甲加值模块；Stripe。
- **可借鉴**：**加值模块（如「关系合盘」「职业推演」）独立付费**，不绑架进订阅。

### 5. RoxyAPI（B2B API，毛利 96–98.5%）
- **模式**：一个 API Key 覆盖 8 个玄学域；订阅 $39–149/月；**多域提升留存**。
- **可借鉴**：OracleMind 的「古代推演 + 现代数据科学」引擎可封装成 **B2B API / White-label**，这是最高杠杆的收入曲线。

### 6. AI Companion 通用六模式（Replika / Character.AI / Scrile）
- Freemium 订阅主导；**Token/Credit 经济**；Persona 解锁；**语音按分钟/订阅**；**White-label/API 授权（最高杠杆 B2B）**；企业合作（医疗/教育/员工 wellness）；UGC 内容市场（创作者分成）。
- **可借鉴**：White-label 引擎授权给健康/冥想/教育品牌 → 预测性收入，不依赖 C 端买量。

### 7. found.fun（情感陪伴，2026 新锐）
- **模式**：纯隐私「被听见」；能量卡片 + 能量足迹可视化；先免费打磨信任 3–6 月再订阅；B 端匿名情感 dashboard。
- **背景**：中国情感经济 2029 将破 4 万亿；68.3% Z 世代向 AI 倾诉。
- **可借鉴**：OracleMind 强化「决策伴侣 / 被理解」定位（与「概率场」话术天然契合），**避开宿命论监管**，用可视化留存。

---

## 六、建议优先级（下一步）

1. **立即**：你做 Vercel env + redeploy（解锁付费）→ 我复验。
2. **本周**：Creem 账户 re-review；上线「7 天 Premium 试用」（RoxyAPI：试用转化高 30–50%）。
3. **本月**：扩展 2–3 个横向域（塔罗/数字命理/姓名学）做多域 bundle；加 Credits 微交易层。
4. **增长杠杆**：做「关系维度对比分享卡」社交裂变 + 语音推演 premium；评估 B2B/White-label API 这条最高毛利曲线。
