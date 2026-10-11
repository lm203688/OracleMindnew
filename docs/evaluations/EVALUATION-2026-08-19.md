# OracleMind 全面扫描 · 四视角终评 · 自动化闭环逐任务审计（2026-08-19）

> 生成日期：2026-08-19 ｜ 范围：`C:\Users\xing\Desktop\oraclemind`（源码 vercel-deploy + 古籍 + 语料 + 情报 + 工作记忆）
> 方法：实地读码（automation/ops-chains/lab-chains/engine-audit/command-center/prediction-engine/vercel.json/workflows）+ 生产 live 校验（oraclemind.cc command-center）+ 账本比对。
> 定位红线（对齐 MEMORY.md）：多维概率场引擎 / 虚拟实验室；对外禁用命理占卜词；三大原则（Automation First / Precision Over Hype / Monetization as Validation）。

---

## 〇、执行摘要（Verdict）

**项目成熟度：自动化地基是全项目最成熟的资产，但"完全不需要你参与"仍差三件事——① 生产调度链真实在跑（现 30h 断链）；② 采纳结果真正被引擎消费（现假闭环）；③ 最后一公里部署/回滚 token 固化（现人工闸门）。**

生产实测（2026-08-19 09:45 UTC，live command-center）：

| 指标 | 数值 | 判读 |
|---|---|---|
| 系统总健康 | degraded（4 healthy / 2 warning / 0 critical） | 非故障，但自动化在停摆 |
| 用户 | 114 free，**0 paying** | 转化未验证（Monetization 原则未通电） |
| 推演 | 11 条预测 / **0 验证** | 校准闭环仍饥饿（不是算法差，是没样本） |
| 反馈 | 13 条（7 accuracy / 0 bug / 0 feature） | 用户在用，但无分拣样本 |
| Agent 经验 | 107 条（**0 insight** / 12 correction / 95 pattern） | **intel-adopt 生产死循环**（0 情报采纳成功） |
| 实验室 | `lab-experiment` **30h 未运行** | ⚠️ 生产调度链断链实锤 |
| 引擎审计 | 6 门全过 @ 08-18 09:48，30 事件 Brier=0.10，lastGood=cd5b404 | 方法验证 OK，但已 24h 未刷新 |
| 系统健康 | 7/7 全绿 | 底层 DB/密钥健康 |

**一句话结论：代码闭环已"设计完整"，生产调度已"实际断链"。你的自动化不是缺功能，是缺"确保定时任务真的在跑"的最后一层。**

---

## 一、项目全貌扫描

### 1.1 技术栈与资产清单

| 层 | 现状 |
|---|---|
| 框架 | Next.js 16 + React 19 + TS（vercel-deploy/，Vercel 生产） |
| 数据层 | Prisma + PostgreSQL（生产 connected，7/7 健康） |
| 古籍 substrate | `五本古籍/` 5 本：2 本已摄取 727 条（渊海子平/三命通会），3 本仅 PDF 待 OCR（M9 未做） |
| 事件语料 | `data/event-corpus.json` **30 条** crisp 0/1 已解决事件（审计权威集） |
| 真实情报锚点 | Manifold 预测市场共识（免 key，`prediction-market.ts`）+ web-scrape（≥2 来源才透出） |
| 引擎 | 倾向场（真实八字 10 神映射）70% + 统计蒙特卡洛 + 多 Agent 共识 30%；事件轨走 eventPrior 市场锚定 |
| 部署 | Vercel（oraclemind.cc）+ GitHub Actions 4 套 workflow + Vercel Cron 3 条 |
| 支付 | PayPal（_xclick+IPN，$4.99 真实测试款已走通；IPN 后台待用户开）；Creem 已拒审（占卜词，已清） |

### 1.2 调度层现状（三层触发）

```
Vercel Cron (vercel.json, 3 条)
  01:00 overnight（13+ 步批量）/ 01:30 auto-fix / 02:00 engine-audit(force)
GitHub Actions (4 workflows)
  daily 03:00/13:00 批量 ｜ weekly 周一 09:00 ｜ monthly 1 日 11:00 ｜ deploy 12:00
生产 API 编排器
  /api/automation/run（26 mode，幂等 JobRun 账本，失败告警）
  /api/command-center（9 loop 仪表台，公开可读）
```

**⚠️ 关键工程隐患（生产断链的直接候选根因）**：

1. **`run/route.ts` 未设 `export const maxDuration`**（grep=0）。Vercel 函数默认超时 ~10s（Hobby 上限 60s）。而 `engine-audit` 一次要跑 15 夹具 × 4 维度 × 2 + 30 事件 × 2 ≈ **180 次引擎推演**，`overnight` 一次串联 13+ 步——**几乎必然超时被掐断**。这正是"报告停在 08-18、lab 停在 08-18"与"调度文件明明在"之间的最大嫌疑。
2. **vercel.json 定义了 3 条 cron**。Vercel Hobby 计划 cron 上限为 2 条（Pro 250 条）。若项目在 Hobby，第 3 条可能被拒/不调度（需在 Dashboard 确认计费档位）。
3. **GitHub Actions 依赖 `secrets.ADMIN_API_KEY`**（Vercel 已配、GitHub 仓库未必配）。未配则所有 curl → 401 → workflow 静默失败。
4. **`VERCEL_TOKEN` 未固化为生产环境变量**（记忆里 ci-deploy 用会话级 `vcp_` token，过期即断）→ 回滚闸门 `engine-audit-rollback` 与 GH deploy 链最后一环仍人工。
5. 鉴权 `authorized()` 依赖 `x-vercel-signature` 头——**需到 Vercel Dashboard 确认 Cron 实际发出的请求头是否含此签名**（若不含，cron 全 401）。

---

## 二、四视角深度评估

### 视角 A：用户（C 端体验 + 市场需求）

**判断：产品定位对（"概率场/决策辅助"去迷信化是差异化抓手），但用户感知到的仍是"工具"而非"可验证的实验室"，且没有可截图分享的社交飞轮——西方赛道（Co-Star/AURA）的增长引擎是"每日一句可截图 + 好友对比 + streak"，这三件当前全缺。**

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 价值感知 | 🟢 | 综合倾向指数 + 方法透明 + 古籍溯源，诚实表达成立 |
| 转化漏斗 | 🔴 | 114 free / 0 paid；`daily-forecast` 表 0 条（前端从未调用该 API）；无前端埋点，流失点未知 |
| 实验感 | 🔴 | "虚拟实验室"概念无用户可感知入口（无"我的第 N 次实验 / 我的准确率"仪表盘） |
| 社交飞轮 | 🔴 | 无 9:16 能量卡 / streak / 好友对比 / 每日一句可截图 |
| 事件轨 | 🟢 | `/api/public/field` 事件模式真实随 Manifold 共识移动（0.27/0.49/0.77 分布），是唯一可自证的"准" |

**用户视角意见**：
1. 把"我的实验准确率"做成留存 + 付费钩子（对标 Co-Star 成长记录）——但前提是接通真实反馈样本（现 0）。
2. 优先落地 9:16 可截图能量卡 + daily streak（P0，增长引擎，已列入上次评估未执行）。
3. 前端埋点（Vercel Analytics）必须补，否则"114→0 付费"的流失节点永远看不见。

### 视角 B：领域专家（预测科学 / AI 交叉验证）

**判断：事件轨的设计是专业的（Brier 硬量化 + Manifold 真共识 + 方向性排序），且严格区分"现代方法验证"与"古典 substrate 不验证"——这是诚实且正确的边界。但"交叉验证"在个人轨仍是装饰。**

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 事件校准 | 🟢 | 30 事件 avgBrier=0.10、方向性排序成立（resolved1 0.701 > resolved0 0.275）——现代管线真在跟踪现实 |
| 合成校准神谕 | 🟢 | 注入 p∈{0.2~0.8} 恢复误差 <0.06；零数据诚实收缩 0.5——校准层本身正确 |
| 个人轨验证 | 🔴 | 11 预测 / 0 outcome → 个人轨的 Brier 无法计算，只能靠用户手点回报（当前 0） |
| 情报采纳 | 🔴 | `intel-adopt` 用 3 个通用话题（"八字 科学 交叉验证"等），`gatherIntelligence` 生产返回 null（web-scrape 出口被拦）→ **0 条采纳**，且写入的 AgentExperience 主引擎根本不读（见 3.3） |
| 古典 substrate | 🟢 | 倾向场用标准子平 10 神映射、不拟合冻结标签——诚实护栏做对了 |

**领域专家意见**：
1. **事件轨是对的，把它做大**：30 条语料太少，Brier 的统计功效不足。应自动扩充语料（见 N2）让 eventAccuracy 有 100+ 样本。
2. **情报采纳链路是假的**：gatherIntelligence 在生产的 null 问题 + 主引擎不消费 AgentExperience，两条都必须接线，否则 M3/M4 是"写库自嗨"。
3. 个人轨不要再追求"算得准"（本性不可纯数理），把叙事放到"周期性/能量基调"的情感价值 + 事件轨的硬准度上——双轨分工是对的。

### 视角 C：技术专家（架构 / 工程化 / 可靠性）

**判断：架构设计是优秀级的（幂等账本、守卫式采纳、回滚闸门、诚实护栏），但"工程末端"四处断裂：生产调度不触发、函数超时、采纳不被消费、部署 token 缺失。自动化链自身没有任何"监控它自己的心跳"。**

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 幂等账本 | 🟢 | `runOnce` + anchorForSlot/mondayAnchor 半日锚点，设计正确 |
| 守卫式采纳 | 🟢 | 只写提案不自动改码 + 回滚人工闸门——Precision Over Hype 的执行典范 |
| 监测覆盖 | 🟢 | 9 loop + 7 项健康 + lab 新鲜度哨兵（`labStaleHours>24` 已能报警） |
| **调度自愈** | 🔴 | **lab 30h / engine-audit 24h stale，报警存在但无人处理、无自动重放**——"监控者没被监控" |
| 函数超时 | 🔴 | 重型 mode 无 `maxDuration`，默认 10s 下 engine-audit/overnight 必超时 |
| 采纳消费 | 🔴 | `agent-experience-memory.ts` 仅被 `/api/simulate/personal/stream` 引用；**主 `PredictionEngine`（public/field、predict-engine、daily 链路）从不读 AgentExperience** |
| 部署回滚 | ⚠️ | 代码完整，但 `VERCEL_TOKEN` 未固化 + GH secret 未必配 |
| 自动化测试 | 🔴 | 自动化链自身无 CI 冒烟测试；verify 只查 health+1 次引擎调用，覆盖极薄 |

**技术专家意见**：
1. **先修调度**：给 run/route 加 `export const maxDuration`（Hobby 60s 上限内拆分重型任务，或上 Pro 300s）；确认 cron 计费档位与签名头；把 GitHub Actions 的 `ADMIN_API_KEY` secret 配上。这一件不做，其余全是空转。
2. **加"调度心跳哨兵"（N1）**：读 JobRun/lab_fixture/engine-audit 时间戳，>36h 未跑自动重放 + 告警——监控者也要被监控。
3. **接线采纳消费（N4）**：让主引擎在推理前注入最近的高置信 AgentExperience（insight/correction），并打 `useCount`，否则 M3/M4 是死库。
4. **自动化链补最小 smoke test**：一次脚本断言"账本有记录 + 报告新鲜 + 引擎非 NaN"，防"显示 success 实则静默失败"。

### 视角 D：投资人（PMF / 商业化 / 壁垒 / 风险）

**判断：产品真实（非空壳）、自动化显著降低 burn、事件轨有 B 端变现想象力（研究/媒体/投研对"可验证的预测"付费意愿远高于个人命盘）。但 PMF 仍未证明：0 收入、0 验证样本、114 免费用户不活跃。壁垒方向（实验室数据集）数据为零。**

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 产品真实度 | 🟢 | 114 自然注册、30 事件语料、完整自动化栈、PayPal 真实测试款走通 |
| 增长设计 | 🟢 | pSEO + GEO 集群（76.5）+ 嫁接（公开 API/Widget/OpenAPI/MCP）+ IndexNow |
| 变现验证 | 🔴 | **0 付费**；premium/deep 定价存在但无人转化；PayPal IPN 后台尚未开 |
| 事件 B 端 | 🟡 | Brier 可证准度 = 潜在 B 端卖点，但当前无订阅/API 计费产品（`/api/public/field` 免鉴权） |
| 壁垒 | 🟡 | 实验笔记本 + 校准数据集是正确壁垒方向，但 0 数据 → 无护城河 |
| 监管 | 🟢 | 占卜/塔罗/数秘付费域已退役，PayPal 冻结风险已消除；话术红线执行到位 |

**投资人视角意见**：
1. 北极星指标定为 **周活跃付费用户（WAU-paid）**；在 0 付费之前，先给"免费→试用→付费"漏斗通电（现连免费用户都不活跃：68 次模拟 / 114 用户）。
2. 事件预测做成**按次/订阅的 API 计费**（嫁接已在，差变现），这是最可能的第一个付费场景。
3. 对外叙事升级为"**可验证的事件预测 API + 个人概率场**"，用 30→100 事件 Brier 曲线做信任背书（数据要靠 N2 自动扩）。
4. 风险提示：PayPal 单点收款仍是集中风险（虽已合规化），建议同时布局 Dodo Payments 等备选。

---

## 三、核心内核评估（古代推演 × 现代演算）

### 3.1 机制评估：能否"推测个人/事件概率、分析、预判趋势"？

**事件轨：YES，已真实工作。** 数据流 = 用户问事件 → 匹配 Manifold 市场共识（0.30~0.55 权重按 matchScore 缩放）→ eventPrior 锚定 → 综合倾向指数 → 可对照已解决语料打 Brier。生产实测指数随真共识移动且不再雷同。这是全项目唯一"Precision Over Hype"的自证证据。

**个人轨：机制成立，验证缺失。** 倾向场把八字十神映射到事业/财富/关系/健康维度（确定性、输入敏感、std=0.148 非退化），古典溯源 727 条真实回检——"古代推演"不再是口号。但"对真实人生的预测效度"没有任何无偏信号（0 条 PredictionFeedback outcome），所以个人轨只能作为**品牌叙事 + 留存钩子**，不能 claim 准确率。

### 3.2 关键生态位与服务体系构建（自动化 / 生态化 / 盈利化）

**生态位定位（建议）：决策智能层——在"占卜（无验证）"与"预测市场（只覆盖公共事件）"之间的空白，即 `个人决策 × 可验证概率场`。** 个人轨吸流留存，事件轨提供可验证价值并变现。

**服务体系分层（建议落地形态）**：

```
┌─ 免费层（获客 + 生态位占位）
│   Quick Insight / 每日概率场简报 / 9:16 能量卡 / Visual Resonance 预览卡（带水印）
│   /api/public/field 公开 CORS + Widget + OpenAPI + MCP（第三方嫁接，零发帖引流）
├─ 付费层（盈利化验证）
│   Deep Analysis（PDF + 时机 + 转折点 + 行动计划）/ 事件预测按次 / API 订阅 key
│   PayPal IPN 已通（$4.99 测试款走通）
└─ 数据层（生态化飞轮 = 壁垒）
    Manifold 共识自动归档 → 事件语料自动扩充（30→100+）→ engine-audit Brier 曲线
    → 用户回报（1-tap 三档）→ PredictionFeedback → calibrate → 置信度上限修正
```

**生态化现状**：嫁接部分已部署（公开 API / embed.js / OpenAPI / MCP），但缺两件事：① 事件语料不自动扩（生态不会自己长大）；② 用户回报漏斗无人点（生态缺燃料）。两者都靠"数据自进化的定时任务"解决（见第六节 N2/N3）。

### 3.3 关键架构断链（必须点名的三处）

1. **采纳→消费假闭环**：`intel-adopt`/`feedback-adopt`/`lab-experiment` 写 `agentExperience`，但主 `PredictionEngine` 推理路径**不读它**（grep 证实仅 streaming 模拟路由引用）。"情报采纳迭代""技术迭代"两条主线实际上是"写库自嗨"。
2. **情报→采纳死循环**：`intel-adopt` 用 3 个泛话题跑 `gatherIntelligence`，生产 web-scrape 被拦/无果返回 null → **agent-experience.insight = 0**。采纳管道没活过。
3. **反馈→校准饥饿**：PredictionFeedback=0 outcome → Brier 校准永远空转；唯一解锁是用户点回报，但流量 114 free 且无埋点。

---

## 四、五大主线定时任务闭环审计（逐任务）

### 主线 1：自动化监测修复

| 环节 | 状态 | 说明 |
|---|---|---|
| 监测 | ✅ | command-center 9 loop + health-check 7 项 + JobRun 账本 + lab 新鲜度哨兵 |
| 修复 | ⚠️ | auto-fix 仅 2 个瞬态修复（时钟回拨/5xx 重试）；真 bug → 写告警；引擎回归 → 人工闸门回滚 |
| 测试 | ✅ | verify（health + 1 次引擎烟测）+ engine-audit 6 门 |
| 更新 | ❌ | 无自动打补丁/改码能力 |
| 上线 | ⚠️ | deploy 链依赖 `VERCEL_TOKEN`（未固化）+ GH secret |

**闭环判定：半闭环。** `报错→告警→(人工/回滚闸门)→verify→deploy`。设计上有，**但生产调度断链（30h stale）+ token 缺失使"报错→处理"根本不会发生**。

### 主线 2：自动推广运营功能迭代

| 环节 | 状态 | 说明 |
|---|---|---|
| 生成 | ✅ | SEO 页 + IndexNow + 邮件序列 + 社媒清单 + GEO 集群（76.5 分，表格/FAQ 自动补强） |
| 发布 | ✅ | publish 链（邮件队列 + 社媒 manifest） |
| 回收 | ✅ | attribution 报告（按来源注册/付费/收入拆分） |
| 迭代 | ❌ | 内容层有 GEO 自迭代；**产品功能层无自动迭代**（无 auto-A/B、无功能决策消费 weekly 账本） |

**闭环判定：运营闭环 / 功能迭代未闭环。** GEO 内容已在自动进化（67.2→76.5），这是真成果。

### 主线 3：情报收集分析采纳迭代

| 环节 | 状态 | 说明 |
|---|---|---|
| 收集 | ✅ | collect-pulse + intelligence-calibrator + Manifold 共识（真实锚点） |
| 分析 | ✅ | 实体/情感/来源可信度/置信度 |
| 采纳 | ❌ **死循环** | intel-adopt 生产 0 insight（话题泛 + 采集 null）；写入的主引擎不消费 |
| 实验 | ⚠️ | lab-experiment 有（30h 未跑）；引擎回归漂移护栏在 engine-audit |
| 验证 | ✅ | engine-audit 6 门（含事件 Brier） |

**闭环判定：名义闭环、实际断链。** 收集→分析通了，采纳→消费两端都断。

### 主线 4：技术迭代用户反馈升级

| 环节 | 状态 | 说明 |
|---|---|---|
| 收集 | ⚠️ | 13 条反馈、11 预测 / 0 outcome；无前端埋点 |
| 分流 | ✅ | feedback-triage 按 Gate 排序 |
| 采纳 | ⚠️ | feedback-adopt 写 correction（12 条），主引擎不消费 |
| 验证 | ❌ | calibrate 0 样本 → Brier 空转 |

**闭环判定：半闭环（数据饥饿）。** 唯一解锁 = 用户回报 + 主引擎消费接线 + 事件结局自动回写（N3）。

### 主线 5：专业数据库对接与自建库扩展

| 环节 | 状态 | 说明 |
|---|---|---|
| 外部对接 | ✅ | Manifold 预测市场（免 key）+ web-scrape（≥2 源） |
| 自建库 | ✅ | Prisma 35+ model + 事件语料 + ServiceMeta 账本 |
| 古籍结构化 | ⚠️ | 2/5 本摄取（727 条），3 本仅 PDF（M9 未做） |
| 引擎使用 | ✅ | classicalBasis 回检溯源（classics-audit 联检过） |

**闭环判定：基本闭环，M9（OCR 3 本）是最后一个待补资产。**

### 五主线总图（生产实测口径）

```
主线1 监测修复 : 监测✅ → 修复⚠️(告警式) → 测试✅ → 更新❌ → 上线⚠️(无token)  → 半闭环 + 调度断链
主线2 推广运营 : 生成✅ → 发布✅ → 回收✅ → 迭代⚠️(仅内容)                    → 运营闭环/功能未闭环
主线3 情报采纳 : 收集✅ → 分析✅ → 采纳❌(死循环) → 消费❌(主引擎不读)          → 名义闭环实际断链
主线4 反馈升级 : 收集⚠️(0样本) → 分流✅ → 采纳⚠️(未消费) → 验证❌(饥饿)        → 半闭环
主线5 数据库   : 对接✅ → 自建✅ → 古籍⚠️(2/5) → 引擎使用✅                    → 基本闭环(欠OCR)
```
**总判断：离"不需要你参与"还差 ①调度心跳 ②采纳消费接线 ③结局自动回写 ④token 固化 ⑤古籍 OCR——5 个补位项，前 4 个是代码+配置，第 5 个是素材。**

---

## 五、补位定时任务清单（10 项，含闭环评估）

> 补位原则：先修"确保现有任务在跑"，再接"让采纳真正进引擎"，再上"让数据自己长大"。每项标注 **报错→修复→测试→更新→上线** 闭环判定。

### N1 · 调度心跳哨兵（Scheduler Heartbeat Watchdog）— P0
- **目的**：监控"定时任务本身"。读 JobRun 账本 + `lab_fixture:*` updatedAt + `engine-audit:latest` ranAt，任一 >36h 未跑 → 自动重放该 mode + 告警 + 写 incident 账本。
- **调度**：每 6h（UTC 04:00/10:00/16:00/22:00，Vercel Cron + GH Actions 双保险）。
- **闭环**：监测✅（时间戳比对）→ 修复✅（自动重放）→ 测试✅（verify）→ 更新✅（重放成功落账）→ 上线✅（无需部署）。**这是唯一"自动化监控自动化"的闭环，直接补 30h 断链。**

### N2 · 事件语料自动扩充器（Event Corpus Curator）— P0
- **目的**：从 Manifold API 拉"最近已结算市场"（结局 0/1 + 市场中点 + 来源 URL），经校验写入 `event-corpus.json`/DB，30→100+ 条。让 engine-audit 的 Brier 关样本量有统计功效，也让"生态数据自己长大"。
- **调度**：每周一 09:30（随 weekly 链）。
- **闭环**：收集✅（Manifold）→ 分析✅（结局核验/去重/质量过滤）→ 采纳✅（写语料）→ 验证✅（engine-audit eventAccuracy 自动重跑）→ 更新✅（语料版本进账本）。**闭环。**

### N3 · 事件结局自动回写结算（Event Outcome Auto-Settlement）— P0
- **目的**：扫所有 `status=pending` 的用户事件预测，凡 `closeDate` 已过 → 用 Manifold 市场结局 / 权威源自动判定 outcome → 写 PredictionFeedback → 进 calibrate。**让"反馈→校准"闭环不再依赖用户手点（现 0 条）。**
- **调度**：每日 03:00（GH daily 链）。
- **闭环**：报错✅（结算失败告警）→ 修复✅（重试/降级人工判定）→ 测试✅（方向性+Brier sanity）→ 更新✅（confidence cap 自动修正）→ 上线✅（无需部署，数据级闭环）。**这是"技术迭代用户反馈升级"的自动化核心。**

### N4 · AgentExperience 采纳消费接线（Experience Consumption Wire）— P0
- **目的**：主 `PredictionEngine.predict()` 推理前注入最近 7 天高置信（qualityScore≥0.6）的 `insight`/`correction` 经验进 prompt/上下文，并 `useCount+1`（已存在该字段，未接线）。把 M3/M4 从"写库自嗨"变成真采纳。
- **调度**：随代码部署一次性接线；此后由 N1 心跳哨兵每日验证 `useCount` 增长（>0 即证明消费在发生）。
- **闭环**：报错✅（useCount 停滞告警）→ 修复✅（接线回归）→ 测试✅（engine-audit determinism 不破）→ 更新✅（prompt 注入生效）→ 上线✅（verify+deploy 链）。**闭环。**

### N5 · 古籍知识库增量构建（Classics KB Rebuild Watch）— P1
- **目的**：检测 `五本古籍/*.txt` 是否有新增/变更 → 自动 `classics:build` 重建 `classics-kb.json` → 跑 classics-audit 回归（维度探针零召回检测）。OCR 完成 1 本即可自动入库，不需人工构建。
- **调度**：每日 09:00 + 每月 1 日。
- **闭环**：检测✅（文件指纹）→ 摄取✅（build 脚本）→ 测试✅（classics-audit 探针）→ 更新✅（KB 版本进账本）→ 上线✅（打包进 bundle）。**闭环。**

### N6 · 自动修复补丁草稿 + 测试（Auto-Patch Draft with Review Gate）— P1
- **目的**：对 `feedback-adopt`/`engine-audit` 产生的高置信 correction 提案，由 agent 自动生成 diff 草稿 → 本地跑 `tsc`/`next build`/smoke → 推 `auto-patches` 分支 → 通过则发 PR 待合并（**人工合并闸门，绝不自动合入 master**）。
- **调度**：每周一 10:00（weekly 链后）。
- **闭环**：报错✅（提案）→ 修复✅（自动生成补丁草稿）→ 测试✅（tsc+build+verify）→ 更新⚠️（PR 待合并，留人工闸门）→ 上线⚠️（合并后走 deploy 链）。**半闭环（安全闸门是 Precision Over Hype 的诚实边界，推荐保留人工合并）。**

### N7 · 增长分析 → 实验决策循环（Growth Analytics Loop）— P1
- **目的**：聚合 attribution + retention + prediction + feedback + 埋点数据 → 产"本周增长实验提案"（定价/漏斗/内容/pSEO 补强清单）→ 自动触发 GEO/pSEO 内容生成器补弱项 → 写入 weekly 账本供决策层消费。**把"回收"升级为"迭代"。**
- **调度**：每周一 09:00（weekly 链前置）。
- **闭环**：收集✅ → 分析✅ → 决策✅（提案写账本）→ 执行✅（内容自动生成+IndexNow）→ 上线✅。**闭环（内容层）；产品层决策仍留人工确认（闸门）。**

### N8 · 支付/订阅健康巡检（Payments Watchdog）— P1
- **目的**：PayPal IPN 到达率（应有订单 vs 实际 IPN 落库）、trial→paid 转化率、订阅到期/续费、churn 预警 → 自动触发 retention/挽回邮件序列。
- **调度**：每日 06:00 + 每周一。
- **闭环**：监测✅ → 预警✅ → 修复✅（自动发挽回/续费邮件）→ 测试✅（IPN 自检）→ 更新✅。**闭环。**（注：IPN 后台首次开关仍须用户一次。）

### N9 · 成本护栏升级（Cost Guard v2）— P2
- **目的**：现有 cost-guard 只算邮件/社媒，升级覆盖 LLM 调用量 + Manifold/web API + DB 体积；超预算自动降级（降频率/关重型审计/限流）。
- **调度**：每日 06:30。
- **闭环**：监测✅ → 告警✅ → 修复✅（自动降级）→ 测试✅ → 更新✅。**闭环。**

### N10 · 自动化链自身冒烟测试（Ops Smoke Test）— P2
- **目的**：CI 里一条脚本断言：JobRun 账本有今日记录 + engine-audit 报告新鲜（<36h）+ 引擎无 NaN + verify ok。**防"账本显示 success 实则静默失败"。**
- **调度**：每日 13:00（PM 槽）。
- **闭环**：检测✅ → 修复✅（失败触发 auto-fix+重放）→ 测试✅ → 更新✅ → 上线✅。**闭环。**

### 现有任务闭环判定速查表

| 任务 | 报错→修复→测试→更新→上线 | 判定 |
|---|---|---|
| overnight 批量 | 告警→auto-fix(瞬态)→verify→❌→deploy 链(无token) | 半闭环 |
| auto-fix | 触发→2 个瞬态修复→verify→❌→❌ | 半闭环 |
| engine-audit | 6 门→pending-rollback→重跑→人工回滚→依赖token | 半闭环(留人工闸门) |
| engine-audit-rollback | —→ADMIN 触发→post-verify→回滚→Vercel API | 半闭环(需token+人工) |
| lab-experiment | 漂移告警→❌只沉淀→❌→❌→❌ | 断链(只报不改) |
| classics-audit | gaps 告警→❌(OCR人工)→探针→❌→❌ | 断链 |
| intel-adopt | 生产 0 insight | **死循环** |
| feedback-harvest | 邮件失败回退→❌→❌→❌→❌ | 半闭环(数据流) |
| feedback-triage/adopt | —→写 correction→❌→引擎不读→❌ | 断链 |
| publish | 失败回退 manifest→❌→verify→❌→❌ | 半闭环 |
| seo-push | IndexNow 失败→❌→verify-indexnow→❌→❌ | 半闭环 |
| referral-blast | 静默失败→❌→❌→❌→❌ | 断链(无转化跟踪) |
| retention / cost-guard | 告警→❌→❌→❌→❌ | 只读 |
| trial-reclaim | —→自动回收→command-center→✅ | **自愈闭环** |
| weekly / monthly / calibrate | 告警→❌→❌→❌→❌ | 报告型 |

---

## 六、达成"不需要你参与"的最小行动清单

### 需要你做的一次性动作（4 件，做完即通电）

1. **Vercel Dashboard 确认三件事**：① 项目计费档位（Hobby 则合并 cron 为 1~2 条，或升 Pro）；② Cron 调度是否真实执行、请求是否带 `x-vercel-signature`；③ 生产环境变量补 `VERCEL_TOKEN`（Deploy 权限，让回滚/部署链通电）。
2. **GitHub 仓库 Settings → Secrets 补 `ADMIN_API_KEY`**（与 Vercel 同值）——否则 4 条 Actions workflow 全部 401 空转。
3. **PayPal 后台开启 IPN**（notify_url=`https://oraclemind.cc/api/payment/paypal/ipn`）——支付闭环最后开关。
4. **OCR 剩余 3 本古籍**（子平真诠/滴天髓/穷通宝鉴）→ 产出 txt 放入 `五本古籍/`，N5 将自动摄取入库。

### 我（自动化层）可自主推进的（按优先级）

1. **P0 N1 调度心跳哨兵** + run/route 加 `maxDuration`/拆分重型任务 + 修 intel-adopt 话题与采集（改从 Manifold 已结算市场 + 近期 resolved 事件取信号，而非 web-scrape 泛话题）。
2. **P0 N3 事件结局自动回写** + **N4 采纳消费接线**（主引擎注入 AgentExperience）。
3. **P0 N2 事件语料自动扩充**（30→100+）。
4. **P1 N5 古籍增量构建 / N6 自动补丁草稿 / N7 增长分析循环 / N8 支付巡检**。
5. **P1 前端埋点 + 9:16 能量分享卡 + daily streak**（增长飞轮，属功能开发）。

### 诚实边界（保留人工闸门的理由）

- **自动回滚到旧 commit / 自动合入代码 PR**：涉及不可逆生产变更，保留"ADMIN 触发 / 人工合并"闸门符合 Precision Over Hype。N6 的补丁草稿全自动、合并留人，是自动化与安全的折中点。
- **古典 substrate 不验证、不自动调参**：现有 engine-audit 边界正确，保持。

---

## 七、结论

1. **自动化地基 9 分，生产执行 4 分**：调度文件齐全但 30h 断链，根因候选为函数超时（无 maxDuration）/Hobby cron 上限/GH secret 缺失——**先修调度，其它才谈得上闭环**。
2. **采纳闭环是假闭环**：`intel-adopt` 生产 0 产出 + 主引擎不读 AgentExperience，情报/反馈两条主线的"采纳"是写库自嗨，需 N4 接线 + N1 验证。
3. **校准饥饿的解锁在事件轨，不在个人轨**：N3 事件结局自动回写 + N2 语料扩充，能让 Brier/准确率"自己长大"，不依赖用户手点。
4. **离"不需要你参与"还差：4 件一次性配置 + 5 个代码补位（N1~N5）+ 3 个增长功能（分享卡/streak/埋点）。** 前两者完成后，项目进入"自动化自监控 + 数据自进化"状态，你的参与频率从"每周"降为"每月看一眼 command-center"。

*本报告全部"生产断链"证据取自 2026-08-19 09:45 UTC 对 oraclemind.cc 的 live 校验与源码审计，非推断。*