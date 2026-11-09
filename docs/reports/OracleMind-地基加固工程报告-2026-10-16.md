# OracleMind 地基加固工程报告——啃硬骨头，不打滑

> **本报告的立场**：项目已经建到相当高度（85,562 行代码、9 大板块、3.0 愿景已规划），但本报告**不讨论往上盖什么**，只回答一个问题——**你现在站的地基，承重能力够不够支撑 3.0 那栋楼？**
> 方法：全部为 2026-10-16 本地**实测**（跑 tsc / 跑 jest 覆盖率 / 跑 eslint / 读 schema / 读 CI / 读部署配置），不是静态阅读，不是猜。
> 一句话结论：**楼的设计是 4.7 分，地基工程是 3 分。现在每一层往上盖，都在把已经存在的裂缝压得更深。**

---

## 〇、体检方法（先声明：全部实测）

| 体检项 | 命令 / 手段 | 结果 |
|---|---|---|
| 类型检查 | `tsc --noEmit`（27 秒跑完） | **34 个错误**（生产 4 + 测试 30） |
| 单元测试 | `jest --ci`（38 秒跑完） | **27 套件 / 289 用例全绿** |
| 真实覆盖率 | `jest --coverage`（实测，非报告里的数字） | **engines 层 17.86%**，飞轮/封存/因果核心 **0%** |
| Lint | `eslint src/lib src/app/api --quiet` | **23 errors** |
| 生产构建 | `next build`（11.5 分钟首次 / 43 秒复跑，**通过**） | **构建通过但门禁形同虚设**：见 H3——`next.config.ts` 显式 `ignoreBuildErrors: true`，带着 4 个生产类型错误照常构建成功 |
| CI 门禁 | 读 `.github/workflows/*.yml` | **不跑 tsc / jest / lint**——只有 API 探活 + 部署 |
| 数据层 | 读 `schema.prisma` + 生成 client + `db.ts` | 见 §二，**发现生产代码真实类型错误** |
| 安全层 | grep zod / 鉴权 / rate limit | 见 §四 |

---

## 一、地基健康度评分（10 分制）

| 维度 | 评分 | 关键证据 |
|---|---|---|
| 架构设计（楼的设计） | **7/10** | 分层清晰、引擎边界明确、vercel.json 安全配置到位、57 个数据库索引 |
| 数据契约一致性 | **2/10** | schema ↔ 生成 client ↔ 写入代码三方漂移；`brierScore` 字段缺失导致飞轮写入静默失败 |
| 类型安全 | **4/10** | 34 个 tsc 错误（含 4 个生产代码）；`noImplicitAny: false` 削弱 strict |
| 测试保护网 | **2/10** | 289 用例全绿但只覆盖 17.86%；飞轮核心模块 0%；CI 不跑测试 |
| 数据层演进能力 | **2/10** | 无 prisma 迁移历史（只有 2 个手工 SQL）；`db` 无数据库时静默假成功 |
| API 安全基线 | **4/10** | 86 路由仅 5 个 zod 校验；~56 路由无明确鉴权；rate limit 无统一中间件 |
| 可观测性 | **2/10** | 错误路径靠 `console.warn` 吞掉，无人知晓 |
| **综合地基健康度** | **≈3/10** | **楼的设计 7 分，地基工程 3 分——裂缝正在被新楼层压实** |

---

## 二、P0 硬骨头：这四个坑，每一个都"会死人"

### H1 数据契约裂缝——飞轮核心写入在真实数据库上会失败（且无人知道）

**证据（实测，非推测）**：

1. `schema.prisma` 的 `Prediction` 模型**有** `probability / outcome / resolvedAt`，**没有** `brierScore`；
2. 但生成的 Prisma Client（`node_modules/.prisma/client/index.d.ts`）里 `PredictionCreateInput` **连 `probability` 都没有**——client 是旧版，schema 更新后**没有重新 `prisma generate`**；
3. `src/lib/engines/prediction-feedback.ts` 的写入代码（417/443/472 行）同时往 `Prediction` 写 `probability` **和** `brierScore`——后者在 schema 里根本不存在；
4. 这些写入路径的 `catch` 块全部是 `console.warn('写入失败（非致命）')` 后吞掉。

**这意味着什么**：飞轮是项目最核心的资产（校准数据是唯一护城河）。这段写入代码在生产环境跑起来时，Prisma 会抛字段校验错误 → 被 catch 吞掉 → **数据静默丢失，系统看起来一切正常**。289 个测试全绿，因为测试里 db 是 mock 的——**测试绿 ≠ 生产对**。你的 arena 镜像飞轮、校准曲线、概率演化，全部依赖这条路径。

**还有第二层静默**：`src/lib/db.ts` 的 no-op proxy——`DATABASE_URL` 缺失或格式不对时，所有 `create/update` 返回 `{id: 'mock-...'}`、`findMany` 返回 `[]`。生产环境如果数据库配置出错，**系统不崩，只是数据全丢**。

**动作**：
1. `prisma generate` 同步 client（5 分钟）；
2. schema 决策：`Prediction` 表补 `brierScore Float? @default(0.25)` 字段（与 `PredictionFeedback` 对齐），或删代码里的写入——**建议补字段**，Brier 是校准飞轮的度量核心；
3. 修 417/443/470/472 行类型错误，跑 tsc 验证归零；
4. **消除静默**：所有数据写入 catch 不得 `console.warn` 吞掉，必须写入 `JobRun` 账本（项目已有账本机制）+ 生产环境告警；
5. `db.ts` 的 no-op proxy：生产环境（`NODE_ENV=production`）缺数据库时**必须快速失败**（抛异常让部署挂掉），而不是静默降级——开发环境保留降级。

**验收**：`tsc --noEmit` 生产代码 0 错误；飞轮写入路径有集成测试（真 Prisma + 真 SQLite/测试库，不 mock）；数据库缺失时生产部署直接失败且告警。
**工作量**：0.5–1 天。

---

### H2 测试幻觉——289 个绿灯照不到 82% 的代码

**证据（实测覆盖率）**：

| 模块 | 覆盖率 | 性质 |
|---|---|---|
| `conformal-prediction.ts` | 96.1% | 好（护城河数学内核有保护） |
| `scientific-metrics.ts` | 98% | 好 |
| `calibration.ts` | 65% | 半 |
| **`prediction-feedback.ts`（飞轮）** | **0%** | **护城河本身没有测试保护** |
| **`commit-seal.ts`（前瞻封存）** | **0%** | **全球唯一信任资产没有测试** |
| **`causal-reasoning.ts`** | **0%** | 2.0 β 层的核心 |
| **`scenario-synthesizer.ts`** | **0%** | 3.0 Φ 层要复用的 |
| **`event-graph-builder.ts`** | **0%** | 因果图的入口 |
| **`modern-deep-analysis.ts`（2766 行）** | **0%** | 最大的文件，零覆盖 |
| `web-search.ts` | 1.16% | 情报轨的取数层 |
| `arena.ts`（1087 行） | 仅镜像/快照/裁决 4 个测试 | 核心对练逻辑覆盖薄 |

**这意味着什么**：每次改飞轮/封存/因果代码，**没有任何自动网能接住回归**。3.0 要在这些 0% 模块上叠世界模型层——**等于在没有任何承重测试的钢梁上焊新结构**。CI 更不跑测试（`autonomous-ops-deploy.yml` 只有 API 探活 + 部署 + 上线后回归），`package.json` 连 `test` 脚本都没有。

**动作**（按护城河优先级排序补测试）：
1. **第一优先**：`prediction-feedback.ts`（飞轮写入/结算/统计，目标 80%+）——这是护城河数据，必须真库测试（Prisma + SQLite 测试实例）；
2. **第二优先**：`commit-seal.ts`（封存/验证/篡改检测，目标 90%+，纯函数好测）；
3. **第三优先**：`calibration.ts`（已有 65%，补齐经验贝叶斯路径到 90%）、`conformal-prediction.ts`（96% 守住）；
4. **第四优先**：`causal-reasoning.ts` / `event-graph-builder.ts` / `scenario-synthesizer.ts`（2.0/3.0 依赖，先补公共接口契约测试）；
5. `arena.ts` 补对练结算路径测试（镜像已有，补评分/裁决/边界）；
6. `package.json` 加 `test` / `test:coverage` 脚本；CI 加 `jest` 步骤 + 覆盖率门禁（低于阈值直接 fail 部署）。

**验收**：核心引擎（飞轮/封存/校准/共形）覆盖率 ≥80% 且 CI 有覆盖率门禁；`npm test` 一键可跑。
**工作量**：2–4 周（这是全报告最大的一块硬骨头，但是唯一一项"不做就一定出事"的）。

---

### H3 类型安全网有洞——strict 被局部关闭，34 个错误长期潜伏

**证据**：
- `tsc --noEmit` 34 错误（4 生产 + 30 测试，测试错误多为 jest-dom 类型缺失/路由导出签名过时）；
- **`next.config.ts` 第 8 行显式 `typescript: { ignoreBuildErrors: true }`——构建期主动跳过类型检查**（实测：带 4 个生产类型错误 `next build` 依然通过）；
- `tsconfig.json` 明确写着 `"noImplicitAny": false`——strict 模式被自己削弱；
- 26 处 `as any`（在 8 万行里不算多，但集中在引擎边界）；
- babel-jest 转译不做类型检查 → 类型错误永远不会被测试发现 → 只会在生产运行时炸。

**动作**：
1. 修 4 个生产类型错误（随 H1 一并完成）；
2. 修测试类型错误（补 `@types/testing-library__jest-dom`、对齐路由导出签名）；
3. 删除 `noImplicitAny: false`，全开 strict；`as any` 逐项审计（数据边界处允许，其余改类型）；
4. **CI 加 `tsc --noEmit` 门禁**——类型错误不得进 main。

**验收**：`tsc --noEmit` 0 错误；`noImplicitAny` 删除；CI 类型门禁上线。
**工作量**：3–5 天。

---

### H4 数据层没有"时间机器"——无迁移历史、无回滚、配置错了假装正常

**证据**：
- `prisma/migrations/` **不存在**；只有 `prisma/` 根目录下 2 个手工 SQL 文件（`add_credits_and_ledger.sql`、`add_prediction_feedback_table.sql`）；
- `package.json` 的 schema 同步方式是 `db:push`（直接推库，无版本、无回滚）；
- 双 git 仓库（详见 H7）导致 schema 变更的审计线索分裂。

**这意味着什么**：schema 每改一次，生产库和开发库的差异就只能靠人脑记。3.0 要加世界模型表、协议表、联邦校准表——**没有迁移体系的 schema 演进是蒙眼开车**。回滚一次 schema 变更需要手工拼 SQL。

**动作**：
1. 建立迁移基线：当前 schema 快照生成第一个 migration（`prisma migrate diff` 从空库到当前 schema 生成基线），此后**禁止 `db push` 推生产**；
2. 写 `docs/eng/db-migration-playbook.md`：变更流程（改 schema → generate → migrate dev → 评审 → 生产 apply → 回滚预案）；
3. 数据库备份策略：生产库每日自动备份（Vercel Postgres/Neon 自带则配置保留期），回滚演练一次。

**验收**：`prisma/migrations/` 有基线迁移；生产环境部署命令从 `db push` 改为 `migrate deploy`；回滚演练记录在案。
**工作量**：2–3 天。

---

## 三、P1 硬骨头：不致命，但决定 3.0 楼能盖多快

### H5 API 安全网只有 6% 的覆盖——86 个路由，5 个有输入校验

**证据（实测）**：
- 86 个 `route.ts`，**仅 5 个用 zod**（~6%）——其余路由的用户输入直接进业务逻辑；
- ~30 个路由有明确鉴权模式（ADMIN_API_KEY / authOptions / getServerSession），**约 56 个没有**；
- rate limit 散落在 5 个文件里手工实现，无统一中间件。

**风险**：脏数据/超长输入直接灌进飞轮和数据库（校准数据被污染 = 护城河水质变差）；未鉴权路由被扫。**3.0 要开放"第三方签发/验证证书"的 API——现在连自己的 API 门都没锁好，就要开门迎客，顺序错了。**

**动作**：
1. 统一 zod 校验层：写一个 `withValidation(schema, handler)` 高阶函数，86 路由逐步迁移（先迁写入类路由：predict/feedback/arena/payment）；
2. 统一鉴权中间件：按路由分组声明鉴权等级（公开 / 用户 / 管理员），默认拒绝；
3. 统一 rate limit：抽成中间件（Vercel KV 或内存 LRU + 按 IP/用户维度），先在 predict/arena/payment 上启用；
4. 安全 headers 已有（vercel.json 的 CORS/X-Frame-Options 是对的），补 CSP。

**验收**：写入类路由 100% zod；所有非公开路由有鉴权声明；rate limit 中间件上线。
**工作量**：1–2 周。

### H6 巨型文件——6 个文件超过 1000 行，最大的 2766 行

**证据**：`modern-deep-analysis.ts` 2766 行、`classical-deep-analysis.ts` 2342 行、`app/page.tsx` 1453 行、`command-center/route.ts` 1238 行、`arena.ts` 1087 行。

**风险**：0% 覆盖 × 2000+ 行 = 每次改动都是盲改。3.0 要在这些文件上叠加新层。

**动作**：按职责拆分（modern-deep-analysis → 分析编排 / 提示构造 / 结果解析 / 后处理 4 个模块），每拆一个补接口测试。**排在 H2 之后**——先有测试再拆，否则拆分本身制造回归。

**验收**：单文件 <1000 行；拆分后原测试全绿 + 新增模块有测试。
**工作量**：2–3 周。

### H7 双仓库分裂——同一项目两套 git 历史

**证据**：`vercel-deploy/` 有独立 `.git`（remote 指向 `github.com/lm203688/oraclemind.git`），root 也有独立 `.git`（**无 remote**）且提交了 M02-P0-①、P0-2 红线修复、断链#6 修复——**同一项目的修复散落在两个没有关联的仓库里**。

**风险**：谁改了 schema 谁不知道；CI 在 vercel-deploy 触发，root 的 docs/数据资产变更完全不进 CI；3.0 的协议规范、数据版本、迁移历史必须在一个可审计的仓库里。

**动作**：决策一个主仓库（建议 vercel-deploy 为主，root 资产作为子目录纳入或明确两个仓库的分工契约写入 `docs/eng/repo-strategy.md`）；至少把 root 无 remote 的问题解决（加 remote 或并入）。

**验收**：单一审计线索；任何 schema/核心代码变更可在同一 git 历史追溯。
**工作量**：0.5–1 天（决策 + 执行）。

### H8 依赖栈踩在最前沿——Next 16 + React 19 + Prisma 6

**证据**：`next ^16.1.1`（2026 年新大版本）、`react ^19`、`@prisma/client ^6.11.1`——全是 12 个月内的大版本。构建本身 11.5 分钟（体量 + 新工具链冷缓存）。

**风险**：Next 16 生态（插件/示例/Stack Overflow 答案）成熟度低于 14/15；升级时 breaking change 吸收成本高。

**动作**：锁定精确版本（去掉 `^`，用 lockfile 为准）；记 `docs/eng/dependency-policy.md`：升级节奏（小版本跟、大版本等 1 个补丁周期）、升级必须在有测试网之后。

**验收**：lockfile 为准的生产安装；升级策略成文。
**工作量**：0.5 天。

---

## 四、为更高的楼预埋的安全与稳定结构（3.0 开工前必须就位）

3.0 要建世界模型层、群体智能层、开放协议层——**这些层对地基的要求比现在高一个数量级**。以下六件事现在做，是给 3.0 预埋的承重结构；3.0 开工后才补，就是拆了楼补地基。

| # | 预埋结构 | 为什么 3.0 必须有 | 现在做（复用现有资产） |
|---|---|---|---|
| S1 | **CI 门禁链**：`tsc → jest → coverage gate → build → deploy` | 世界模型层代码量翻倍，没有门禁 = 每天盲改 | 已有 GitHub Actions + jest，只差把 tsc/coverage 接进 deploy workflow |
| S2 | **错误零静默**：所有 catch 进 `JobRun` 账本 + 生产告警 | 飞轮静默失败一次 = 校准数据脏一个月；世界模型模拟失败同样不能静默 | 已有 `JobRun` 模型 + `calibration-backfill` 对账思路，升级为全局错误账本 |
| S3 | **数据库时间机器**：migrations + 备份 + 回滚演练 | 3.0 每加一层（世界模型表/协议表/联邦表）都要安全演进 schema | 已有 57 个索引的 schema 底子，缺迁移体系和流程 |
| S4 | **统一 API 安全中间件**：zod 校验 + 鉴权分级 + rate limit | 开放协议层（第三方签发/验证证书）开门之前，自己的门必须先锁好 | 已有 vercel.json headers + ADMIN_API_KEY 模式，抽成中间件 |
| S5 | **并发安全结构**：乐观锁（`version` 字段）+ JobRun 幂等 + 连接池配置 | 群体智能层 = 多用户同时写校准画像；世界模型模拟 = 长任务并发。现在 `update` 无版本控制，并发写会丢更新 | Prisma 加 `version Int @default(0)` + 更新带 `where version` 的乐观锁模式 |
| S6 | **可观测性结构**：结构化日志（替换 console.*）+ 关键指标看板 | 3.0 的北极星（不确定性压缩率/Swarm 增量）没有度量就没有迭代方向 | 现在 29 处 console.log + 静默 catch——先统一日志格式，再接看板 |

---

## 五、90 天地基工程路线图（四个冲刺，每周可验收）

> 铁律：**冲刺 1–2 完成前，冻结一切新功能开发**（包括 3.0 的任何一层）。地基没浇实就往上盖，是给自己埋雷。

### 冲刺 1（第 1–2 周）：止血 + 门禁上线
- H1 数据契约修复（generate + brierScore + 静默失败改造）→ 验收：tsc 生产 0 错误
- H3 类型错误清零 + strict 全开 → 验收：tsc 全仓 0 错误
- H4 迁移基线建立 → 验收：migrations/ 有基线 + 生产改 `migrate deploy`
- CI 门禁链上线（tsc + jest 进 deploy workflow）→ 验收：红测/红型阻断部署
- **周末验收会**：跑全量体检（tsc/jest/eslint/build），数据记档

### 冲刺 2（第 3–5 周）：补测试网（最大的硬骨头）
- H2 第一~三优先模块测试（飞轮/封存/校准/共形 ≥80%）→ 验收：覆盖率报告 + CI 门禁阈值
- `package.json` 补 test 脚本；错误账本（S2）第一版
- **周末验收会**：核心引擎覆盖率曲线只准上升

### 冲刺 3（第 6–8 周）：API 安全网
- H5 zod 校验层 + 鉴权分级 + rate limit 中间件 → 验收：写入路由 100% 校验
- S4 完成；CSP 补齐
- H7 仓库决策执行
- **周末验收会**：安全扫描（自写 checklist：鉴权/校验/限流/密钥）

### 冲刺 4（第 9–12 周）：结构预埋 + 收尾
- S5 乐观锁 + 并发模式落地（为群体智能层预埋）
- S6 结构化日志 + 看板第一版
- H6 巨型文件拆分（前 3 个，有测试后拆）
- H8 依赖锁定策略成文
- **最终验收**：全量体检全绿 + 3.0 开工评审（地基就绪签字）

---

## 六、纪律红线（贴在工位上的五条）

1. **门禁全绿之前，不新增任何业务功能**——包括 3.0 的任何一层。这不是保守，是 3.0 的前置条件。
2. **禁止 `console.warn` 吞异常**——数据写入失败必须进账本并告警。静默失败是校准数据的毒。
3. **schema 变更必须走 `prisma migrate`**——`db push` 只允许推本地开发库。
4. **新 API 必须带 zod schema + 鉴权等级声明**——无校验不上线。
5. **每周五跑全量体检**（tsc + jest --coverage + eslint + build），数据进 `.workbuddy-ai/memory/`——地基健康度是项目唯一的先行指标，比任何功能指标都优先。

---

## 七、这份报告与 3.0 方案的关系

- 3.0 方案（10-16）定义了"往上盖什么"（世界模型/群体智能/自主进化/开放协议）；
- 本报告定义了"往上盖之前必须浇实什么"（数据契约/测试网/类型安全/迁移体系/API 安全/并发结构）；
- **本报告的冲刺 1–2 = 3.0 阶段 0 的工程细化**。3.0 阶段 0 若只有"部署+冷启动"而没有本报告的门禁链和测试网，等于把 3.0 的 Φ/Ω/Ψ 层盖在裂缝上。
- 一句话：**先把这 90 天地基工程做完，再谈 3.0 开工。地基健康度从 3 分到 7 分之前，任何新功能都是负债。**

---

*本报告全部数据取自 2026-10-16 对 `C:\Users\xing\Desktop\oraclemind` 的实地实测（tsc 27s / jest 38s / eslint 52s / next build 11.5min 首次 + 43s 复跑通过 / 覆盖率实测）；`next build` 通过系因 `next.config.ts` 显式关闭构建期类型检查（`ignoreBuildErrors: true`），非代码无错。工作量估计以 1 名工程师 + AI 协作为单位（人天）。*
