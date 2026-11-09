# OracleMind SCI 论文复现包

> **一句话**：所有实验数字都可以在本 README 指引下由第三方独立复现，无需信任作者。

---

## 目录

- [1. 数据集（复现核心）](#1-数据集复现核心)
- [2. 校准/共形对比实验](#2-校准共形对比实验)
- [3. 前瞻注册 & 防篡改验证](#3-前瞻注册--防篡改验证)
- [4. 依赖与环境](#4-依赖与环境)
- [5. 学术诚信自检清单](#5-学术诚信自检清单)

---

## 1. 数据集（复现核心）

### 1.1 主数据集

**`data/backfill-events.seed.json`** — 305 条真实已决事件。

- 每条事件包含：`id`, `question`, `resolutionDate`, `outcome`, `category`, `source` (公开主源 URL), `horizonDays`
- 所有 outcome 均可通过 `source` URL 独立核验
- 覆盖类别：宏观（FOMC、ECB、BOJ）、政治（US/UK/India/Turkey）、金融（BTC、S&P、Gold）、科技（GPT-4、Chandrayaan-3）、政策（EU AI Act）、自然（USGS 地震、NOAA 飓风、WMO 温度）

### 1.2 校验数据集完整性

```bash
node scripts/validate-backfill.mjs
```

该脚本验证：
- 所有 `outcome` ∈ {`positive`, `negative`, `neutral`}
- 所有 `resolutionDate` 早于采集日
- 所有 `source` URL 格式合法
- 所有 `id` 唯一

---

## 2. 校准/共形对比实验

### 2.1 一键跑

```bash
cd vercel-deploy
node experiments/conformal-coldstart.mjs
```

输出到 `experiments/results/conformal-coldstart-<timestamp>.json`。

### 2.2 4 种校准器

| 方法 | 实现位置 | 说明 |
|---|---|---|
| Identity | `experiments/conformal-coldstart.mjs` | 无校准，baseline |
| Platt Scaling | 同上 | Sigmoid 参数拟合 |
| Isotonic Regression | 同上 | PAVA 算法 |
| **Empirical Bayes Shrink** | `src/lib/engines/calibration.ts` | 本项目的核心方法 |

### 2.3 4 项指标

- **Brier Score** — 二次损失
- **Log-Loss** — 交叉熵
- **ECE (10 bins)** — 期望校准误差
- **Bootstrap 95% CI** — 500 次重采样

### 2.4 关键学术诚信声明

**当前 Table 1 使用的 raw 概率是"模拟的"**（`simulateRawProbabilities` 函数），**不是 OracleMind 真实预测**。最终论文必须用真实 OracleMind 预测替换。参见 `docs/paper/P2-method-distribution-free-coldstart.md` §5.3。

---

## 3. 前瞻注册 & 防篡改验证

### 3.1 封存一个预测

```typescript
// commit-seal.ts
import { sealSimulation } from '@/lib/engines/commit-seal';
const result = await sealSimulation(simulationId);
// result.commitHash = "sha256:<64-hex>"
// result.committedAt = Date
```

### 3.2 锚定到 OpenTimestamps

```typescript
import { anchorCommitHash } from '@/lib/engines/opentimestamps-anchor';
const anchor = await anchorCommitHash(commitHash, simulationId);
// anchor.anchorProofUrl = "https://api.opentimestamps.com/file/xxx.json"
// anchor.blockHeight = 850000
```

### 3.3 公开验证页

访问 `https://oraclemind.cc/verify/<simulationId>`：

- 显示 sealed payload、hash、committedAt
- 显示 OpenTimestamps anchor URL 与比特币区块高度
- 客户端可独立复算 hash 校验完整性

### 3.4 离线验证（论文复现）

```typescript
import { verifyAnchor } from '@/lib/engines/opentimestamps-anchor';
const { verified, error } = await verifyAnchor(commitHash, anchorProofUrl);
console.log(verified ? '锚定有效' : `锚定失败: ${error}`);
```

---

## 4. 依赖与环境

### 4.1 Node.js

- Node 22+（推荐 22.22.2）
- npm

### 4.2 核心依赖

```
next 15.x
prisma
@prisma/client
crypto（Node 内建）
```

### 4.3 数据库（生产）

- PostgreSQL（Neon）
- 迁移：`prisma db push`
- 关键迁移文件：`prisma/migrations/add_backfill_integrity_fields.sql`

### 4.4 环境变量

```bash
# 生产环境必需
FEEDBACK_AUTH_TOKEN=<long-random-string>  # 防投毒
DATABASE_URL=postgres://...
DIRECT_URL=postgres://...
```

### 4.5 本地验证

```bash
# 类型检查
node node_modules/typescript/bin/tsc --noEmit

# Jest 测试
node node_modules/jest/bin/jest.js

# 红线词审计（SCI 合规）
node scripts/audit-public-terms.mjs
```

---

## 5. 学术诚信自检清单

投稿前逐条勾选：

### 5.1 数据完整性

- [ ] `cold-start-seed.mjs` 已移到 `scripts/_disabled/`（编造脚本已停用）
- [ ] `backfill-events.seed.json` 每条都有 `source` URL
- [ ] 所有 DB 记录（isBackfilled=true）都有 sourceEventId + resolvedAt + sourceUrl
- [ ] 论文中 Table 1 的数字**不是**用 cold-start-seed 编造的数据得出的

### 5.2 校准方法正确性

- [ ] `calibration.ts` 使用 `shrink = n / (n + K)`，`n=0` 时诚实回 0.5
- [ ] `conformal-prediction.ts` 使用 `ceil((n+1)·q)` 有限样本修正
- [ ] 论文明确写"边际覆盖"而非"条件覆盖"

### 5.3 因果层诚实

- [ ] `structured-reasoning.ts` **不出现** "causal inference" 学术用语
- [ ] 论文中不使用 "causal" 描述启发式推理
- [ ] 参考范围见 `src/lib/engines/domain-prior.ts`

### 5.4 领域先验诚实

- [ ] `domain-prior.ts` 已定义 Bazi/Zi Wei/Qi Men/Feng Shui 的 `isHeuristic=true`
- [ ] `assertNotUsedAsStatisticalEvidence` 在关键路径上调用
- [ ] 论文方法学章节显式声明"structured domain heuristic prior"，禁称科学先验

### 5.5 防篡改 & 可审计

- [ ] `commit-seal.ts` 生成 sha256，载荷不含结局
- [ ] `opentimestamps-anchor.ts` 提供 OTS 锚定入口
- [ ] `/verify/[id]` 页面公开可访问
- [ ] `/api/feedback/outcome` 生产环境强制 `X-Feedback-Auth-Token` 鉴权

### 5.6 CI & 部署

- [ ] `.github/workflows/ci-gates.yml` 存在（lint/test/build 门禁）
- [ ] 本地 `tsc --noEmit` 无错误（除 `__tests__` 基线）
- [ ] Jest 测试全通过
- [ ] 红线词审计 `audit-public-terms.mjs` exit 0

---

## 附录：文件清单

```
vercel-deploy/
├── schema.prisma                                # 加 isBackfilled/sourceEventId/resolvedAt
├── prisma/migrations/
│   └── add_backfill_integrity_fields.sql         # 新迁移
├── src/lib/engines/
│   ├── calibration.ts                            # 经验贝叶斯收缩（SCI 级）
│   ├── conformal-prediction.ts                   # Split Conformal（SCI 级）
│   ├── commit-seal.ts                            # 前瞻注册封存
│   ├── opentimestamps-anchor.ts                  # 防篡改锚定（新）
│   ├── domain-prior.ts                           # 领域启发式先验声明（新）
│   └── structured-reasoning.ts                   # 已改名为"结构化推理"
├── src/app/
│   ├── verify/[id]/page.tsx                     # 公开验证页
│   └── api/feedback/outcome/route.ts             # 已加鉴权
├── experiments/
│   ├── conformal-coldstart.mjs                   # 4 校准器对比实验
│   └── results/                                  # 实验产物
├── .github/workflows/                            # CI 门禁（已存在）
│   ├── ci-gates.yml
│   └── ...
data/
└── backfill-events.seed.json                     # 305 条真实事件
scripts/
├── coldstart-backfill.mjs                        # 真实回填脚本（新）
├── validate-backfill.mjs                         # 数据集校验
├── audit-public-terms.mjs                        # 红线词审计
└── _disabled/
    └── cold-start-seed.mjs                       # 已停用（编造脚本）
docs/
├── paper/
│   ├── P1-system-tamper-evident-forensics.md     # 系统论文草稿
│   └── P2-method-distribution-free-coldstart.md  # 方法论文草稿
└── reports/
    └── OracleMind-SCI达标性核查与评价-2026-10-19.md  # 原始核查报告
```

---

## 联系与贡献

- 论文草稿位于 `docs/paper/`
- Bug / 数据补正 → GitHub Issues
- 学术诚信疑问 → 参考本 README §5

*Generated 2026-10-19 by OracleMind Research Group.*
