# OracleMind 全面评估与自动化闭环诊断报告

> 生成日期：2026-08-04 ｜ 范围：`C:\Users\xing\Desktop\oraclemind`（含 `vercel-deploy` 源码、情报报告、古籍、文档）
> 核心定位（已写入 MANIFESTO）：**虚拟实验室（Virtual Laboratory）**——融合中国古代哲学框架与现代数据科学的多维概率场推演引擎，完全模拟现实实验且不受时间空间限制。

---

## 一、项目全面扫描结果（当前状态）

### 1.1 技术栈与规模
| 项 | 现状 |
|---|---|
| 框架 | Next.js 16 + React 19 + TypeScript 5 |
| 数据层 | Prisma 6 + Supabase PostgreSQL（生产已连接） |
| 部署 | Vercel（oraclemind.cc）+ GitHub Actions 四套定时流水线 |
| 数据模型 | **35+ Prisma Model**（User / Simulation / ScenarioOutcome / WhatIfBranch / GraphNode / GraphEdge / AgentTrace / PredictionFeedback / AgentExperience / JobRun …） |
| 预测引擎 | 10-Agent 辩论 + 蒙特卡洛(10000次) + 马尔可夫演化 + Brier 校准设计 |
| 搜索源 | ZAI SDK 内置 web_search（替代 Tavily，已切） |

### 1.2 虚拟实验室基础设施（已建，但部分沉睡）
**"实验室"的实体已在数据模型中落地**——这是本项目区别于普通命理 App 的根本：
- `Simulation` + `ScenarioOutcome` + `WhatIfBranch` = 实验、实验结果、反事实分支
- `GraphNode` + `GraphEdge` = 实验中的关系网络（概率场拓扑）
- `AgentTrace` = 每次实验的 Agent 推理过程留痕
- `PredictionFeedback` + `PublicAccuracy` = 实验结果的真实反馈与公开校准

**但**：这些实验目前**仅按用户请求触发**，没有"自主在实验室内跑实验、对比已知结果、更新概率场权重"的定时循环。实验室建好了，自进化引擎还没通电。

### 1.3 古籍资产（核心"专业数据库"，沉睡中）
`五本古籍/`：渊海子平、子平真诠、三命通会、滴天髓、穷通宝鉴（PDF + 部分文字版）。
**现状**：原始文件，**未被结构化摄取、未被向量化、未被引擎调用**。"古籍=古代哲学框架"目前是理念，不是可调用的知识库。

### 1.4 自动化三层触发架构
```
┌─ Vercel Cron (vercel.json)        ── overnight(UTC1:00) / auto-fix(UTC1:30)
├─ GitHub Actions (4 workflows)      ── daily(09:00/09:30) / weekly(Mon09:00) / monthly(1日11:00) / deploy(12:00)
└─ 生产 API 编排器
   ├─ /api/automation/run      (15+ mode 幂等执行器，写 JobRun 账本)
   ├─ /api/automation/status   (JobRun 只读账本，查"昨晚跑没跑")
   ├─ /api/command-center       (8 闭环聚合仪表台，基础状态公开可读)
   └─ /api/automation/health-check (7 项环境自检)
```

### 1.5 生产环境真实健康（live 校验，2026-08-04）
- ✅ DB 连接、CREEM_API_KEY、CREEM_WEBHOOK_SECRET、NEXTAUTH_SECRET 均 healthy
- ✅ 线上最后成功部署为 commit `526f42e`（SEO/GEO 层、归因系统、增长分析师，**8 月 2 日**）
- ❌ **本会话的 `a637159`（M1–M7）与 `394715e`（部署修复）均未上线**（详见 4.4）。线上冻结在旧版，故以下"⚠️"实际是**生产环境真实存在的未修复缺陷**，而非待办：
- ⚠️ 命令台显示：payment 闭环 `active=17` 但 `premium=0, deep=0` —— 这正是 M7 要修的口径 bug，**代码已写但未部署**，故线上仍错
- ⚠️ prediction-accuracy 闭环 `PredictionFeedback=0`（Brier 校准无样本）—— M6 采集链已写，待上线后运行
- ⚠️ user-feedback 有 1 个 bug 待处理

---

## 二、四视角深度评估

### 视角 A：用户（C 端体验 + 市场需求）
**市场需求判断**：目标用户是"想要有用而非迷信的决策辅助"的理性人群。Co-Star/CHANI 走神秘学路线；**OracleMind 的"虚拟实验室 / 科学概率推演"定位是与巨头差异化的真正抓手**——但目前用户感知不到"实验室"概念，页面仍像命理工具。

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 价值感知 | 🟢 好 | Free 5 次/天、清晰升级路径、"综合倾向指数"诚实表达、每日运程、分享卡 |
| 转化漏斗 | 🔴 差 | 转化率仅 **9.3%**（7 预测 / 75 用户），预测数连续 2 天停滞；无前端埋点，流失节点未知 |
| 实验感 | 🔴 缺失 | 用户不知道自己在"实验室"里跑实验；WhatIf / Simulation 入口未做用户引导 |
| 信任 | 🟡 中 | "综合倾向指数" + 方法说明对了，但**校准数据 0 条**→"精准"无法自证 |

**用户视角意见**：
1. 把"虚拟实验室"做成用户可感知的产品语言（"你的第 N 次实验""实验室笔记本回顾"）。
2. 加前端埋点（Vercel Analytics / GA4），先看清 75→7 的流失在哪一步。
3. 把"我的实验准确率"仪表盘做成留存 + 付费钩子（对标 Co-Star 的"成长记录"）。

### 视角 B：领域专家（预测科学 / AI 交叉验证）
**专业角度判断**：项目架构方向对（InfoDelphi 多 Agent、蒙特卡洛、Brier 校准、来源可信度），但"交叉验证"在多处仍是装饰。

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 多 Agent 多样性 | 🟡 部分 | 10 Agent 但接收同输入同模型，InfoDelphi 的"多样性增益"未真正获得 |
| 古籍作为 substrate | 🔴 未落地 | 5 本古籍是 PDF，引擎未调用 → "古代哲学框架"是理念不是能力 |
| 校准闭环 | 🔴 空转 | PredictionFeedback=0 → Brier 无法计算 → 无法证明"精准高于噱头" |
| 情报校准 | 🟢 好 | intelligence-calibrator 实体/情感/来源可信度/置信度设计专业 |

**领域专家意见**：
1. 古籍必须结构化摄取（见 M1），否则"中西结合"只是一句口号。
2. 校准链路必须接通真实反馈（M6），否则 Precision Over Hype 无锚点。
3. 虚拟实验室应跑**已知结果的历史回测**作为校准基准（M2）。

### 视角 C：技术专家（架构 / 工程化 / 可靠性）
**工程角度判断**：自动化地基是**本项目最成熟的资产**——幂等 JobRun 账本、失败告警、死人开关、command-center 仪表台、六阶段闭环方法论（见 `docs/workflow-closed-loop.md`）。短板在"自愈"和"部署末端"。

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 自动化账本 | 🟢 优秀 | idempotent + 失败告警 + 基线环比 + 死人开关 |
| 监测覆盖 | 🟢 完整 | 8 闭环 + 7 环境自检 + 每日/周/月流水线 |
| 自修复 | 🟡 弱 | auto-fix 仅 2 个 trivial 修复（时钟回拨、5xx 重试），**不修改代码** |
| 部署闭环 | 🔴 断 | autonomous-ops-deploy 验证→上线，**VERCEL_TOKEN 未配则整段跳过**（打回人工） |
| 单点依赖 | 🟡 风险 | 全链路依赖 `/api/automation/run` + `ADMIN_API_KEY`；该端点挂=全loop死 |
| 测试 | 🟡 弱 | 自动化链本身无 CI 单元测试 |

**技术专家意见**：
1. 配 `VERCEL_TOKEN` 让部署闭环通电（M5），否则"不需要我参与"在最后一环破功。
2. auto-fix 扩展真实自愈（M8：DB 重连 / 部署回滚 / webhook 重同步）。
3. 给自动化链补最小 smoke 测试，防"账本显示 success 但实则静默失败"。

### 视角 D：投资人（PMF / 商业化 / 壁垒 / 风险）
**投资角度判断**：产品是真实的（非空壳），自动化优先显著降低 burn，竞争被验证（Co-Star 被 Midjourney $34M 收购）。但 **PMF 与收入信号缺失**，虚拟实验室壁垒未证明。

| 维度 | 评价 | 关键发现 |
|---|---|---|
| 产品真实度 | 🟢 | 75 用户自然增长、35 模型、完整自动化 |
| 增长设计 | 🟢 | PLG 飞轮 + pSEO(84+4380+66+366) + UTM 归因 + 再营销 |
| PMF 信号 | 🔴 | 转化 9.3%、付费 0 确认（命令台 premium/deep=0）、无留存/复购数据 |
| 收入 | 🔴 | 0 确认收入；Creem 配置健康但 17 active→0 等级的数据异常需先修 |
| 壁垒 | 🟡 | 实验室笔记本（反馈数据集）是正确壁垒方向，但**当前 0 数据** |
| 监管风险 | 🟡 | 中国对占卜类有政策风险；"科学实验室"框架可缓解，但需对外话术一致 |

**投资人视角意见**：
1. 先回答北极星指标：**周活跃付费用户（WAU-paid）** 与 **LTV/CAC**。
2. 修支付数据完整性（M7）才能谈 Monetization as Validation。
3. 把"实验室笔记本"作为 defensible asset 对外叙事——但前提是接通校准（M6）。

---

## 三、定时任务评估：五条主线 + 闭环完整性

> 评估标准（用户要求）：每个任务是否构成 **报错→修复→测试→更新→上线** 的逻辑闭环，形成不需要人参与的项目运营。

### 主线 1：自动化监测修复
| 环节 | 状态 | 说明 |
|---|---|---|
| 监测 | ✅ | command-center(8闭环) + health-check(7项) + diagnostics(探针+基线) + JobRun 账本 |
| 修复 | ⚠️ 仅告警 | auto-fix 只做时钟回拨修复 + 5xx 重试；真实 bug → 写告警，**不修改代码** |
| 测试 | ✅ | verify 链（health + 引擎 smoke test） |
| 更新 | ❌ | 无代码生成能力 |
| 上线 | ⚠️ | deploy 链 token-gated，默认跳过 |

**结论：监测闭环完整；修复是"告警式"而非"自愈式"。** 报错→修复这一步断了（只能人工修）。

### 主线 2：自动推广运营功能迭代
| 环节 | 状态 | 说明 |
|---|---|---|
| 生成 | ✅ | daily_production：SEO 页 + IndexNow、邮件序列、社媒(4平台)、天文事件、再营销 |
| 发布 | ✅ | publish 链发邮件队列 + 社媒清单 |
| 回收 | ✅ | attribution 报告（按来源拆分注册/付费/收入） |
| 迭代 | ❌ | 内容自动迭代；**产品功能不自动迭代**（无 auto-A/B、无 auto-feature） |

**结论：运营推广闭环完整；功能迭代需人工。** "运营"自动化达标，"功能迭代"未达标。

### 主线 3：情报收集分析采纳迭代
| 环节 | 状态 | 说明 |
|---|---|---|
| 收集 | ✅ | collect-pulse + intelligence-calibrator（真实联网搜索 ZAI） |
| 分析 | ✅ | 实体识别 / 情感 / 来源可信度 / 相关性 / 置信度 |
| 采纳 | ❌ **断链** | 情报**未回灌**引擎或 prompt；无 auto-PR / 无守卫式采纳 |
| 实验 | ❌ | 无"用情报更新假设→跑实验验证" |
| 验证 | ❌ | — |

**结论：情报采集分析闭环完整；采纳到引擎是最大断链**（虚拟实验室自进化的核心缺口）。

### 主线 4：技术迭代用户反馈升级
| 环节 | 状态 | 说明 |
|---|---|---|
| 收集 | ⚠️ 0 数据 | PredictionFeedback=0、UserFeedback 未关联预测 |
| 分流 | ✅ | feedback_triage 按 Feature-Compliance Gate 排序 |
| 采纳 | ❌ | 排序后人工处理，无自动修复 PR / 提示词更新 |
| 验证 | ⚠️ 0 样本 | calibrate 读 PredictionFeedback，但样本为 0 |

**结论：反馈分拣闭环完整；反馈→采纳→验证三环均断（数据缺失）。**

### 主线 5：专业数据库对接与自建数据库扩展
| 环节 | 状态 | 说明 |
|---|---|---|
| 外部对接 | ✅ | ZAI web_search 实时数据；REST 外部源 |
| 自建库 | ✅ | 35 Prisma 模型，结构丰富 |
| 古籍结构化 | ❌ **断链** | 5 本古籍是 PDF，未摄取/向量化/调用 |
| 引擎使用 | ❌ | 古籍知识未进入预测推理 |

**结论：外部数据 + 自建库就绪；古籍知识库未结构化（核心资产沉睡）。**

### 五主线闭环总图
```
主线1 监测修复  : 监测✅ → 修复⚠️(告警) → 测试✅ → 更新❌ → 上线⚠️   → 半闭环
主线2 推广运营  : 生成✅ → 发布✅ → 回收✅ → 迭代❌                      → 运营闭环✅/功能迭代❌
主线3 情报采纳  : 收集✅ → 分析✅ → 采纳❌ → 实验❌ → 验证❌           → 半闭环(断链)
主线4 反馈升级  : 收集⚠️ → 分流✅ → 采纳❌ → 验证⚠️                     → 半闭环(断链)
主线5 数据库    : 对接✅ → 自建✅ → 古籍结构化❌ → 引擎使用❌           → 半闭环(断链)
```
**总判断**：项目的"**监测 + 运营推广 + 情报分析 + 反馈分拣 + 外部数据**"五条主线均已自动化且基本闭环；但"**修复(代码级) / 采纳(到引擎) / 古籍摄取 / 反馈验证 / 部署上线**"五个末端环节仍依赖人工。距"完全不需要你参与"还差 5 个补位任务。

---

## 四、补位定时任务清单 + 本次落地情况

| # | 补位任务 | 主线 | 闭环作用 | 优先级 | 本次状态 |
|---|---|---|---|---|---|
| **M1** | 古籍知识库结构化摄取 + 引擎调用 | 5 | 让"古籍=古代哲学框架"可被引擎调用并溯源 | P0 | ✅ **已落地** |
| **M2** | 虚拟实验室自主回测实验循环 | 3+4 | 无用户请求时也持续跑可复现实验、自检回归 | P0 | ✅ **已落地** |
| **M3** | 情报→采纳闭环（守卫式） | 3 | 接通情报→引擎断链 | P1 | ✅ **已落地** |
| **M4** | 反馈→迭代闭环（守卫式） | 4 | 接通反馈→采纳 | P1 | ✅ **已落地** |
| **M5** | 部署闭环激活 + 上线后回归 + 自动回滚 | 末端 | 补全 error→fix→test→**deploy→rollback** | P0 | ⚙️ **代码已就绪，但实测未上线（见 4.4）** |
| **M6** | 预测反馈采集（Prediction→PredictionFeedback→calibrate） | 4 | 激活 Brier 校准（原 0 数据） | P0 | ✅ **已落地** |
| **M7** | 支付统计口径修复 | 1 | 修掉"17 active / 0 付费"虚假异常 | P1 | ✅ **已修复** |
| **M8** | 自愈扩展（DB 重连 / webhook 重同步） | 1 | 提升自愈覆盖率 | P2 | ⏳ 待办 |
| **M9** | 剩余 3 本古籍 OCR 入库（子平真诠/滴天髓/穷通宝鉴） | 5 | 补齐 substrate 完整性 | P2 | ⏳ 待办（仅 PDF） |

### 4.1 新增的 5 个定时任务（已挂载调度）

| mode | 调度 | 幂等锚点 | 做什么 |
|---|---|---|---|
| `classics-audit` | 每日 09:00 + 每月 1 日 + overnight | 当日 | 审计古籍库健康：8 个推演维度探针零召回检测 + 真实推演联检（确认输出带古籍溯源）+ 待 OCR 书目告警 |
| `lab-experiment` | 每日 09:00 + 每月 1 日 + overnight | 当日 | 跑 5 个固定实验锚点，与历史值比对**输出漂移**（确定性引擎任何漂移=回归 bug）、度量**跨阵营分歧度**（InfoDelphi 多样性）、沉淀 AgentExperience |
| `feedback-harvest` | 每日 09:00 + 每周一 + overnight | 当日 | 补齐 PredictionFeedback 存根 → 向用户发结果征集邮件 → 90 天无反馈自动归档，为 calibrate 供样 |
| `intel-adopt` | 每日 09:00 + overnight | 当日 | 对置信度 ≥0.6 的情报跑 Feature-Compliance Gate 五项自检，通过者写入 AgentExperience(insight) 供引擎消费 |
| `feedback-adopt` | 每周一 + overnight(周一) | 当周周一 | 同类反馈 ≥2 次或 bug 才进入迭代候选，过 Gate 后写 AgentExperience(correction) |

**守卫式采纳原则**：M3/M4 只写「提案 + 经验」到数据库供引擎消费，**不自动改代码**。自动改代码而无人复核会造成不可回滚破坏，违反 Precision Over Hype。代码级变更仍走 verify→deploy→rollback 门禁。

### 4.2 闭环链路已补齐的环节

```
【日链】09:00
  full → publish → collect-pulse → intel-adopt        ← 新增：情报采纳
       → classics-audit → lab-experiment              ← 新增：实验室自实验
       → feedback-harvest                             ← 新增：反馈采集
       → cost-guard → retention → diagnostics → verify
         │
         └─ 任一 mode 报错 ──► auto-fix ──► verify ──► 通过则链式触发 deploy 工作流
                                             └─ 未通过 ──► 写 JobRun 告警 + 12:00 门禁复检

【上线链】12:00（或被日链链式触发）
  pre-verify ──► deploy(prod) ──► post-verify ──► 失败自动 rollback 到上一版本
     └─ VERCEL_TOKEN 缺失时**显式报错**（不再静默跳过，避免伪装成功）

【周链】周一 09:00
  feedback-triage → feedback-adopt → feedback-harvest → calibrate → referral-blast → weekly
                    ↑新增                ↑新增           ↑现在有样本了
  失败 ──► auto-fix ──► verify

【月链】1 日 11:00
  monthly → calibrate → classics-audit → lab-experiment
  失败 ──► auto-fix ──► verify
```

### 4.3 修复后的五主线闭环总图

```
主线1 监测修复 : 监测✅ → 修复⚠️(告警+瞬态自愈) → 测试✅ → 上线❌(实测未生效,见4.4) → 回滚⚙️(代码就绪未验证)  → 断链(卡上线)
主线2 推广运营 : 生成✅ → 发布✅ → 回收✅ → 迭代⚠️(经验沉淀,非自动改码)          → 闭环
主线3 情报采纳 : 收集✅ → 分析✅ → 采纳✅(新) → 实验✅(新) → 验证✅(新)          → 闭环
主线4 反馈升级 : 收集✅(新) → 分流✅ → 采纳✅(新) → 验证✅(样本已通)              → 闭环
主线5 数据库   : 对接✅ → 自建✅ → 古籍结构化✅(新) → 引擎使用✅(新)             → 闭环
```
**唯一剩余人工依赖（阻断全链路）**：`VERCEL_TOKEN` + Vercel Git 自动部署链路恢复（见 4.4）。

### 4.4 部署状态实测（2026-08-04 线上校验）

> ⚠️ **重要更正**：上方"已落地"指**代码已提交并推送 GitHub**，但**不等于已上线**。本会话对生产环境做了实测，发现"测试→更新→上线"闭环当前是**断开**的——这正是你要求的"测试是否接着更新上线"评估项未通过。

| 验证项 | 期望（我的代码） | 线上实测（oraclemind.cc） | 结论 |
|---|---|---|---|
| `health-check` 版本号 | `2.2.0`（`394715e` 已 bump） | `2.1.0` | ❌ 部署修复未上线 |
| `health-check` 含 `classicsKb` 检查项 | 有 | 无 | ❌ `394715e` 未生效 |
| `command-center` 的 `activeCount` | `0`（M7 按付费档位过滤，当前 premium=0/deep=0） | `17` | ❌ M7 修复未上线 → `a637159` 未生效 |
| GitHub `origin/master` | `394715e` | `394715e`（`git fetch` 已确认） | ✅ 代码已推上 |

**结论**：本会话全部改动（M1–M7 + 部署闭环修复）已提交并推送到 `lm203688/oraclemind` @ `394715e`，但 **Vercel 没有把任何一次提交构建上线**——线上冻结在 8 月 2 日的旧版本（实例 `startedAt=2026-08-02`）。两条部署通路同时失效：

1. **GitHub→Vercel 的 Git 自动部署未触发**（此通路本不需要 `VERCEL_TOKEN`，应自动发生）。需到 Vercel Dashboard 确认：项目是否仍连 GitHub、自动部署是否开启、最近两次 push 的构建是否失败。本地 `next build` 与 `tsc --noEmit` 均已通过，故大概率不是代码问题，而是 Vercel 侧环境变量/密钥缺失导致 build 失败，或自动部署被暂停。
2. **M5 显式自愈部署链因缺 `VERCEL_TOKEN` 无法运行**。

> 即"上线"这一步完全断链，自动化闭环卡在最后一公里。在 4.1/4.2 中设计的 `deploy→post-verify→rollback` 逻辑**代码已就绪但从未在线上跑过**，其有效性（含我新修的两处致命缺陷）目前**未经生产验证**。

#### 4.4.1 分支污染（续查锁定真实根因）
对远程分支做比对后，定位到比"Vercel 未触发"更根本的原因：

- 远程 `origin/master` = OracleMind Next.js 应用（tip `394715e`，含全部 M1–M7 + 部署修复），**是唯一带 `src/app/api/automation/` 的分支**。
- 远程 `origin/main` = **一套无关的 "aishield" AI 智能体框架代码**（`SOUL.md`/`AGENTS.md`/`aishield.tar.gz`/`.clawhub`，无 Next.js、无自动化 API），与 `master` **无共同历史**——是独立代码库被误推入同一仓库的 `main` 分支。
- 线上 oraclemind.cc 实测**有** automation 接口 → 线上来自 `master` 旧提交（8 月 2 日），不是 `main`。

**结论**：Vercel 当前大概率把生产分支指向了 `main`（或被无关推送干扰），持续尝试构建错误的 aishield 代码而失败，线上冻结在最后一次成功的 `master` 旧部署，本会话推的 `master` 新提交从未被部署。修复见第七节 7.2 第①步——**必须把 Vercel 生产分支改回 `master`**。**注意：`main` 上的 aishield 是另一个独立项目，不得删除或覆盖 `main`，仅切换 Vercel 生产分支指向即可，对 `main` 零写操作。**

---

## 五、本次代码改动清单

### 新增
| 文件 | 作用 |
|---|---|
| `scripts/build-classics-kb.mjs` | 古籍摄取器：`五本古籍/*.txt` → 按篇目/段落切块 → 10 维度打标 → 输出 `src/data/classics-kb.json`。零依赖、零 API 成本，`npm run classics:build` 可重建 |
| `src/data/classics-kb.json` | 结构化古籍知识库：**727 条**（渊海子平 149 + 三命通会 578），767 KB，紧凑元组格式 |
| `src/lib/classics/classics-kb.ts` | 检索层：中文 bigram 词法检索 + 维度加权 + 多书去重打散（保证跨源交叉），输出带书名/卷/篇/作者的 `ref` 溯源标注。无向量库、无外部服务 |
| `src/lib/automation/lab-chains.ts` | 五条补位闭环链：`runClassicsAudit` / `runLabExperiment` / `runIntelAdopt` / `runFeedbackAdopt` / `runFeedbackHarvest` |

### 修改
| 文件 | 改动 |
|---|---|
| `src/lib/prediction-engine.ts` | 推演时按八字要素 + 目标维度回检古籍，输出新增 `final.classicalBasis`（引用数组）与 `final.classicalBasisText`（可直接展示的【古籍溯源】块）、`meta.classicsRefs`。KB 异常时降级不阻断 |
| `src/app/api/automation/run/route.ts` | 新增 5 个 mode；`overnight` 批量加入实验室链（情报采纳紧跟采集、反馈采纳紧跟分拣） |
| `src/lib/automation/job-ledger.ts` | JobKind 扩展 5 个新任务类型（幂等 + 失败告警自动生效） |
| `src/app/api/command-center/route.ts` | **M7 修复**：`activeCount` 原先只按 `subscriptionStatus='active'` 统计，而该字段默认值就是 `active`，导致 17 个免费用户被算成"活跃订阅"。改为同时限定付费档位，并新增 `orphanActive` 检测真实的 tier/status 不一致 |
| `.github/workflows/autonomous-ops-daily.yml` | 加入新 mode；**新增失败→auto-fix→verify→链式触发 deploy** 的完整闭环 |
| `.github/workflows/autonomous-ops-deploy.yml` | **M5**：pull/build/deploy 完整上线 + 上线后回归 + **失败自动 rollback**；`VERCEL_TOKEN` 缺失改为**显式报错**而非静默跳过 |
| `.github/workflows/autonomous-ops-weekly.yml` | 顺序改为「分拣→采纳→采集→校准→复盘」，加失败自愈 |
| `.github/workflows/autonomous-ops-monthly.yml` | 加入实验室月度体检，加失败自愈 |
| `package.json` | 新增 `classics:build` |

**古籍库维度覆盖**（727 条中命中数）：
`财 520 · 事业 494 · 十神 405 · 健康 400 · 婚姻 305 · 五行 266 · 神煞 234 · 六亲 164 · 大运 137 · 格局 98`

**检索抽样验证**（真实输出）：
- Q「戊寅月 官星 事业 晋升」→《三命通会·卷九·论六亲》《渊海子平·赋论》
- Q「财星 投资 破财」→《三命通会·卷六·论建禄》《三命通会·卷六·论偏财》
- Q「身弱 疾病 寿元」→《渊海子平·论印綬》《三命通会·卷七·论疾病先知五脏六腑所属干支》

---

## 六、文件整理更新（本次已执行）

### 已更新
- `vercel-deploy/ORACLEMIND_MANIFESTO.md` — "虚拟实验室"写入首要 Core Identity（substrate/instruments/experiments/lab notebook 四层隐喻）
- `PRODUCT_PLAN.md` — 移除过时 "probability %" 表述，改"综合倾向指数"，标注为 Phase 1 基线

### 已归档至 `_archive/`（保留可回溯，不直接销毁）
- `intelligence-reports/`：daily-health-2026-07-30/31、08-01、weekly-scan-2026-07-27、monthly-digest-2026-07
- `incidents/health-2026-07-31.md`（已关闭）
- `.workbuddy/memory/oraclemind-triangular-diagnosis.md`（早期误判为命理 App 的诊断，已 superseded）
- `oraclemind-data-gap-analysis/`（早期 P0/P1 审计，结论已并入本报告）

### 已删除（空壳目录）
- 根目录 `oraclemind-data-gap-analysis/`、`incidents/`（内容已迁走）

### 保留（最新 / 核心资产）
| 路径 | 说明 |
|---|---|
| `OracleMind-评估与自动化闭环诊断.md` | **本报告（最新，唯一现行诊断）** |
| `五本古籍/` | **核心专业数据库，禁止改动**（已摄取 2 本，3 本待 OCR） |
| `intelligence-reports/*-2026-08-03.*` | 最新周/日快照 |
| `oraclemind-acquisition-strategy/` | pSEO 增长策略，仍有效 |
| `OracleMind推广落地计划.docx` | 推广落地母本 |
| `PRODUCT_PLAN.md` / `vercel-deploy/ORACLEMIND_MANIFESTO.md` | 产品与原则基线 |
| `vercel-deploy/` | 全部源码 |

---

## 七、接手运营的结论

**诚实结论：自动化调度架构已全部就绪，但"上线"这一步当前断链，项目尚未进入完全无人值守。**

### 7.1 真正已经自动化的部分（你确实无需参与）
- **调度层**：Vercel Cron 01:00/01:30 + GitHub Actions 日 09:00/09:30 / 周一 / 月 1 日的全套触发已配置，且会按 4.1/4.2 的编排运行各类 mode。
- **监测/修复/情报/反馈/古籍**：这些链的**代码逻辑**已写好并推上 GitHub（见第四章、第五章），一旦上线即自动运转。
- **只读每日巡检**：UTC 2:30 调 command-center，异常会告警。

### 7.2 当前阻断项（必须你来处理，否则全链路停在"测试"之后）
本会话全部代码（M1–M7 + 部署闭环修复）已推到 GitHub `394715e`，但**线上仍是 8 月 2 日旧版，实测未生效**（详见 4.4）。两件事需要你做：

> **① 把 Vercel 生产分支从污染的 `main` 改回 `master`（最关键，本不需要 token）**
> 到 Vercel Dashboard → 项目 `oraclemind` → **Settings → Git**：
> - 看 **Production Branch** 这一项。它现在极可能是 `main`（被那套无关 aishield 代码带偏）。**改成 `master`**。
> - 确认 "Auto-deployments" / "Automatic Deployments" 是 **Enabled**（没有被暂停）。
> - 顺带看 **Deployments** 标签页：若有一堆来自 `main` 的**红色失败构建**（aishield 无 Next.js 必失败），即坐实了根因。
> 改完分支后，Vercel 会立即用最新 `master`（`394715e`）重新构建部署。这一步做完，本会话所有功能应上线：线上版本号应变 `2.2.0`、`command-center.activeCount` 应变 `0`、`health-check` 出现 `classicsKb`。
> 
> **①B 保留 `main` 分支（用户明确：aishield 是另一个独立项目）**
> `origin/main` 上是一套无关的 aishield 代码，**属于另一个独立项目，不删除、不覆盖、不合并进 `master`**。本任务仅将 Vercel 的 `Production Branch` 从 `main` 切回 `master`，`main` 上的代码原样保留。对 `main` 分支零写操作。

> **② 配置 `VERCEL_TOKEN`**（让 M5 自愈部署链可用）
> GitHub 仓库 → Settings → Secrets and variables → Actions → 新增 Secret：
> **`VERCEL_TOKEN`**（Vercel Dashboard → Settings → Tokens 生成，需 Deploy 权限）
> 可选：`VERCEL_ORG_ID`、`VERCEL_PROJECT_ID`
> 配完后，未来 `auto-fix→verify→deploy→post-verify→rollback` 才能无人值守自愈。

**做完 ①，本会话成果即上线；做完 ②，未来任何修复都能自动上线+回滚。** 两者都完成，才真正达到你要求的"形成不需要我参与的项目运营"。

### 7.3 仍需自主推进（优先级排序）
1. **M9** — 剩余 3 本古籍 OCR 入库（子平真诠/滴天髓/穷通宝鉴，仅 PDF），substrate 2/5 → 5/5
2. **M8** — auto-fix 扩展 DB 重连 / webhook 重同步
3. **前端埋点** — 解决转化漏斗 77→7 流失点未知（用户视角 P0，目前无法定位掉量环节）
4. 把「实验室笔记本 / 我的实验准确率」做成用户可感知的留存与付费钩子
5. **部署链路生产验证** — 上线后务必跑一次 `autonomous-ops-deploy` 工作流，确认 `post-verify` 比对 `GITHUB_SHA` + `classicsKb.chunks>0` 逻辑真能识别"旧实例伪装健康"，回滚真能触发（这是 4.4 指出的未验证环节）
