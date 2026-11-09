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
| `OracleMind-3.0-自演化预测智能-下一个阶段愿景与提升方案-2026-10-16.md` | 2026-10-16 | **最新下一阶段方案（超越 2.0 的再下一代）**：2026-10 复扫基线（节气 bug 真修闭环/2.0 α 仍开路）；三条交汇曲线（世界模型开源 V-JEPA2+Cosmos / AI Scientist v2 自主科学循环 / 预测市场基础设施化 ICE×Polymarket）；3.0 愿景 = 自演化世界模型驱动的预测智能网络；四大新增层 Φ 世界模型（神经符号 SCM+不确定性双分解+TSFM）/ Ω 群体智能（Swarm+联邦校准）/ Ψ 自主进化（AI Scientist 式循环+RL 元预测器）/ Π 开放预测网络（协议 2.0+OpenTimestamps+可复现科学）；六大科学内核升级；四阶段路线（阶段0 关地基→Φ→Ω→Ψ→Π）；北极星 +4 先行指标。同名 `.html` 为可预览版 |
| `OracleMind-地基加固工程报告-2026-10-16.md` | 2026-10-16 | **地基体检与加固方案（啃硬骨头，不打滑）**：全部为本地实测（tsc 34 错误含 4 个生产 / jest 289 全绿但覆盖率实测仅 17.86% / eslint 23 errors / CI 不跑测试 / next build 带类型错误通过因 `ignoreBuildErrors:true`）。P0 四硬骨头：H1 数据契约裂缝（schema↔client↔代码三方漂移 + brierScore 缺失 + 飞轮写入静默失败 + db no-op proxy 假成功）/ H2 测试幻觉（飞轮·封存·因果核心 0% 覆盖）/ H3 类型安全洞（strict 被削弱 + 构建期类型检查被显式关闭）/ H4 数据层无迁移无回滚；P1 四硬骨头（API 校验仅 6%·巨型文件·双仓库分裂·依赖踩前沿）；**为 3.0 预埋的六大承重结构**（CI 门禁链/错误零静默/数据库时间机器/统一 API 安全中间件/乐观锁并发结构/可观测性）；90 天四冲刺路线图 + 五条纪律红线。同名 `.html` 为可预览版 |
| `OracleMind-查缺报告-2026-10-17.md` | 2026-10-17 | **全仓查缺清单（Q-01~Q-52，可直转工单）**：16 个总览数字 + 六类缺口（A 说了没做 / B 做了没接线 / C 接了没数据 / D 安全与数据完整性 / E 配置工程 / F 文档漂移）。头号发现：**5 个文件（公开验证页 + OpenTimestamps 锚定 + 个人竞技场）放在根 `src/app/`，因 Next 根是 vercel-deploy 而永不部署**；致命缺口：`feedback/outcome` 无鉴权=校准数据投毒入口；另：15 孤儿 API、4 死代码引擎、4 语言包 0 使用、28 页零 loading/error、48 env vs 2 配置、P2 加固 0/8。附四波修复顺序（第一波 8 项 <3 天）。同名 `.html` 为可预览版 |
| `OracleMind-科学性与SCI论文可行性评估-2026-10-18.md` | 2026-10-18 | **科学性与 SCI 可行性评估（实地读源码+测试+实证核验）**：内核 8/10、整体 7/10；统计内核方法正确（经验贝叶斯收缩 / Split-Conformal 有限样本修正 / Murphy 分解 / ECE / Bootstrap CI / climatology 技巧分）且含**统计真值级单测**（200 样本断言覆盖下界 1-1/(n+1)）；calibration/forecast-guard/conformal 达发表级。SCI 判定：**能发但非现在**——venue 选 UQ 方法 / 可信预测系统 / 数据集（IJF、Conformal workshop、AIES/FAccT、Scientific Data），非核心 ML。5 个论文选题（P1 密码学前瞻注册 / P2 冷启动共形校准 / P3 覆盖度感知技巧分 / P4 神经符号可审计预测 / P5 人机混合纵向基准）。**唯一阻断=0 条已验证结局**（代码自述 0 验证）；红线：古典层不得作科学先验宣称、因果层须改名/升级（假因果）、所有准确率数字须来自真验证集。同名 `.html` 为可预览版 |
| `OracleMind-SCI就绪执行方案-2026-10-18.md` | 2026-10-18 | **SCI 就绪直接落地执行方案（承接科学性评估）**：6 Sprint / 14 周路线图，每张任务到文件级 + 验收标准 + 完成定义。Sprint 0 数据解锁（冷启动回填→真实 (p,y) 数据集，硬前置）；S1 方法硬化（P2 共形校准对比实验 Platt/Isotonic/本项目 + 测试加固≥60% + 统计真值测试）；S2 系统资产（commit-seal 归位部署+OpenTimestamps 锚定+防投毒）；S3 因果层治理（去假因果：真后门调整 / 改名二选一）；S4 古典层重构（八字→结构化领域启发式先验+诚信声明）；S5 论文撰写（P2 方法投 IJF/Conformal workshop、P1 系统投 AIES/FAccT/Scientific Data）。附 5 条学术诚信红线 + 工作量（40–51 人天）。**T0-1 已改为"AI 代理自动采集公开可核验真值源（Metaculus 已决问题/GDELT/官方主源），无需人工数据输入"**；另交付可执行脚手架：`data/backfill-events.seed.json`（14 条真实已决事件，经 WebSearch 核验+validate 通过）+ `scripts/validate-backfill.mjs`（强制决议日已过+来源可达，实测通过）。同名 `.html` 为可预览版 |
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
