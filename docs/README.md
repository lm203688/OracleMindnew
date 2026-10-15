# OracleMind 文档索引

> 更新：2026-10-10 ｜ **只需读两份：`00-core/CORE-GOALS.md`（目标）+ `00-core/OracleMind-综合方案-2026-10.md`（一切）。**

## 阅读顺序

```
1. 00-core/CORE-GOALS.md                  ← 权威目标，一切决策的根据
2. 00-core/OracleMind-综合方案-2026-10.md  ← 【唯一权威综合材料】诊断/战略/产品/协议化/商业/合规/执行/决策
3. 00-core/ROADMAP.md                     ← 历史留档：已落地物 ↔ 文件索引（查实现细节看这里）
4. 其余按需查阅
```

> 📌 2026-10-10 起，此前分散的四份材料（全面提升报告 / 概率层提案 / 商业预测方案 / 执行方案）**已全部合并进第 2 项**，原件移入 `docs/archive/2026-10-已合并/`。

> ⚠️ **双工程提醒**：仓库里有两套独立工程，勿混用。
> - **主应用** = `vercel-deploy/`（Next.js 16 + React 19 + Prisma，部署到 oraclemind.cc）。
> - **根级测试工程** = 根目录的 `package.json`(474B) + `node_modules` + `babel.config.js` + `coverage/`，只为跑 `TESTING-SUMMARY.md` 那套根级 Jest 单测。**主应用的构建/回归测试在 `vercel-deploy/` 内**（含仍待修的 32 个伪集成套件，对应 ROADMAP P1-16）。
> - **推送通道**：本地 `git push github.com:443` 被墙，统一走 `vercel-deploy/scripts/push-om.py`（Python Contents API）。改完 `vercel-deploy/` → 本地提交 → `python vercel-deploy/scripts/push-om.py` → 复验远端 blob。Vercel 部署由 webhook 自动触发（主仓 `lm203688/oraclemind`）。

---

## 00-core — 权威目标层（最高优先级）

| 文件 | 内容 |
|---|---|
| `CORE-GOALS.md` | **唯一权威目标定义**。定位、双轨结构、三大原则、合规闸门、北极星指标、数据策略 |
| **`OracleMind-综合方案-2026-10.md`** | ⭐ **唯一权威综合材料**：现状诊断、战略定位（概率层+记分板）、产品设计、协议化、商业预测、海外合规、四阶段执行、Stop Doing List、8 项 owner 决策、新北极星。**取代 ROADMAP** |
| `ROADMAP.md` | 历史留档：**已落地物 ↔ 文件索引**（P0 交付明细、部署通道诊断、波次状态）。查实现细节看这里 |
| `PRODUCT-PLAN.md` | 免费/付费产品形态与功能分层细则 |

> 目标层有任何变更，先改 CORE-GOALS。

---

## reports — 评估与提升报告（证据层）

| 文件 | 日期 | 内容 |
|---|---|---|
| `OracleMind-技术壁垒与国际化提升方案-2026-10-12.md` | 2026-10-12 | **最新全仓扫描**：技术壁垒深挖（真/伪壁垒）、国际竞品三矩阵、科学先进性分层、**新发现两处错配（专利与技术主体无关 / 古典 substrate 实体仅 2/5）**、最新科技融合（贝叶斯更新 / TSFM / L3 事件×数值）、P0-P2 提升方案。含 **2026-10-13 附录 A**（增量复扫：P0-1 已接通 / 新断链 #6 / ForecastBench 实时榜单 AI 69.0>超预 68.6 / TSFM 3.0 开源）。同名 `.html` 为可预览版 |
| `OracleMind-逐板块提升评估总报告-2026-10-14.md` | 2026-10-14 | **逐板块独立评估（9 板块）**：每板块单独评流程走通/人类习惯、竞品与需求、开源融合、单板块提升方案 + 5 维健康度分。含 9 份分报告 `docs/reports/per-module/M01–M09-*.md` 与导航 `docs/reports/per-module/index.html`。核心结论：架构完整 4.7 但数据走通 1.8（全局冷启动死锁）；三大断裂（冷启动/古典 substrate 残缺/差异化未可见）；三件事最高杠杆（修 M02 节气+OCR → 冷启动注入 → M07 公开验证页+OpenTimestamps）。**复扫确认断链 #6 已修复、arena 断链 #5 已修** |
| `OracleMind-全面提升报告-2026-10-08.md` | 2026-10-08 | 全面扫描：核心目标对标、14 板块完成度、国际竞品对标、2026 技术杠杆、五大断裂点、P0-P2 路线图 |
| `PHASE0-PHASE1-REPORT.md` | 2026-08-11 | Phase 0/1 实施报告 |
| `TESTING-SUMMARY.md` | 2026-09-24 | 测试现状摘要 |

---

## evaluations — 历史评估（证据层）

| 文件 | 日期 | 内容 |
|---|---|---|
| `EVALUATION-2026-08-19.md` | 2026-08-19 | 四视角终评 + 自动化闭环逐任务审计（含 N1-N10 补位清单） |
| `EVALUATION-2026-08-09.md` | 2026-08-09 | 早期全面评估 |
| `OracleMind-评估与自动化闭环诊断.md` | 2026-08-04 | 自动化闭环诊断 |
| `OracleMind-健康巡检.md` | 2026-08-05 | 健康巡检记录 |

---

## strategy — 战略与商业化（决策层）

| 文件 | 日期 | 内容 |
|---|---|---|
| `profitability-review-2026-09-10.md` | 2026-09-10 | 盈利性诊断：瓶颈在转化与信任，非产品 |
| `strategic-review-2026-08-14.md` | 2026-08-14 | 战略回顾 |
| `strategy-review-2026-08-07.md` | 2026-08-07 | 战略回顾 |
| `PAYPAL-IPN-SETUP.md` | 2026-08-12 | PayPal IPN 配置指引（**P0-1 待执行**） |
| `creem-compliance-checklist.md` | 2026-08-06 | Creem 合规清单 |
| `domestic-payment-evaluation.md` | 2026-08-12 | 国内收单方案评估 |

---

## research — 算法与技术研究（方法层）

| 文件 | 日期 | 内容 |
|---|---|---|
| `event-inference-pivot-2026.md` | 2026-08-13 | **事件轨战略转向论证**：为何事件比个人更适合验证 + 国际基准数据 |
| `inference-algorithms-math-2026.md` | 2026-08-13 | 推演算法数学基础调研 |
| `derivation-algorithm-evaluation.md` | 2026-08-11 | 开源数理推演算法评估与落地路线（PySR / NumPyro / DoWhy） |

---

## outreach — 推广素材

| 文件 | 内容 |
|---|---|
| `ai-directory-submission.md` | AI 目录提交文案 |
| `x-promotion-playbook.md` | X（Twitter）推广手册 |

---

## archive — 历史留档（**不作决策依据**）

| 内容 | 说明 |
|---|---|
| `PRODUCT_PLAN-superseded.md` | 旧产品计划，已被 `00-core/PRODUCT-PLAN.md` 取代 |
| `OracleMind推广落地计划.docx` | 早期推广计划 |
| `incidents/` `intelligence-reports/` | 2026-07 至 08 的巡检与情报报告 |
| `oraclemind-data-gap-analysis/` | 数据差距分析 HTML |
| `oracemind-intake/` | 2026-09-15 的素材入库暂存 |
| `_workbuddy-memory/` | 三角诊断笔记 |

---

## 仓库外的重要资产（不在 docs 内）

| 路径 | 内容 |
|---|---|
| `vercel-deploy/` | **生产代码仓库**（Next.js 16 + React 19 + Prisma），与 GitHub `lm203688/oraclemind` 同步 |
| `五本古籍/` | 古典 substrate 原始文本（5 本 txt + PDF） |
| `data/event-corpus.json` | 事件语料（引擎审计权威集） |
| `patent-backup/` | 专利申请材料（DMTL 3 轮迭代 + 5 张附图） |
| `scripts/` | 根级脚本（symbolic-pilot.py 等） |
| `intelligence-reports/` | 2026-08-03 的情报报告 |
| `oraclemind-acquisition-strategy/` | 获客策略 HTML |
| `coverage/` | 测试覆盖率产物（可清理） |

---

## 冲突解决规则

```
CORE-GOALS  >  ROADMAP / PRODUCT-PLAN  >  reports / strategy / research  >  archive
```

同一层级内，**以日期最新者为先**。
