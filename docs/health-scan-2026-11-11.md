# OracleMind 健康度扫描（2026-11-11）

> 模板：统一健康度扫描模板 v1（C:\Users\xing\.dsh\bot\workspace\intel\_boards\健康度扫描模板-v1.md）
> 扫描范围：OracleMind 项目（C:\Users\xing\Desktop\所有项目\7.oraclemind）

---

## 1. Git 状态
- 分支 `main`，HEAD `a9810fd`（2026-11-10 06:08，docs: NBA 跨赛季 hold-out 验证可行性排查报告归档）。
- 工作树 1 项未跟踪：`data/nba/`（本轮下载的原始 zip，未纳入版本控制）。
- 最近 3 commit：`a9810fd`（NBA hold-out 可行性报告）、`6195f30`（CodaBench 18486 提交包确认摘要）、`8ec4a35`（提交包状态确认）。

## 2. CI 闸门
- 闸门总数 0（**项目根目录无 `.github/` 目录，GitHub Actions 未配置**）。
- 本地存在可用脚本但未接入 CI：根 `package.json` 仅 `test/test:watch/test:coverage`（jest）；`vercel-deploy/package.json` 有 `typecheck`、`typecheck:ci`、`lint`。
- 最近一次运行时间：不适用（无 CI）。**未核实** `vercel-deploy` 是否经 Vercel CI 部署。

## 3. 文档完备度
- 核心文档存在但非最新：`README.md`/`docs/README.md`（11,847 B，2026-10-18）、`AGENTS.md`（845 B，2026-11-08）；**`PROJECT_VISION.md` 不存在**（有 `docs/00-core/ROADMAP.md`、`CORE-GOALS.md` 承接）。
- `docs/reports/` 下 26 份报告，最新 `oraclemind-nba-holdout-validation-feasibility-2026-11-10.md`，与代码演进基本同步。
- 诚实边界声明存在（多份报告含"模拟数据占位/未验证"标注），但 `vercel-deploy/submission-package/validation_report.json` 中文字段为 GBK 乱码（编码不一致），`"verified": false`。

## 4. 数据/资产新鲜度
- 关键资产 `data/nba/` 6 个 zip + `data/nba/sumitrodatta/nba-aba-baa-stats.zip`，下载时间 2026-11-11 16:48–16:53，**全部未解压、未校验字段**（未核实是否含 game_id/日期/主客队/收盘赔率/实际比分）。
- 数据来源可追溯：Kaggle 匿名下载，许可证 CC0 / CC BY 4.0 / MIT（cviaxmiwnptr、minmaxer、archangel0x01、erichqiu 等）。
- CodaBench 官方数据集不可得（API 被 Anubis 反爬拦截），存在过期/失效风险：提交包 game_id 仍为模拟格式 `NBAxxxxx`。

## 5. 未决问题
- TODO/FIXME 共 7 处（`vercel-deploy/src`），如 `lib/api/auth.ts:42`（TODO(3.0) 接入登录会话校验）。
- 待决策：①双轨实现方案执行（Chief `oraclemind-dualtrack-1111` 等待中）；②跨赛季 hold-out 可行性结论需复核——现已拿到 2024-25 真实数据，`a9810fd` 报告"2024-25 不可得"结论已过时。
- 阻塞项：无 CodaBench 官方 test 集 game_id → 无法满足"game_id 强校验"→ 真实提交仍不可能。

## 6. 能力边界自评
- 已完成（有证据）：提交包产出（`predictions.csv` 994 场、2 个 zip、manifest、validation_report）；4 套基线脚本 `scripts/nba-baselines.py`；Kaggle 真实数据获取（7 个数据集落盘）；CodaBench 18486 条款已核（CC BY 4.0、无奖金）。
- 未达成/负结果（如实标注）：**主轨真实模型尚未构建、真实数据未评估**；跨赛季 hold-out 未执行；CodaBench researcher access 路径确认走不通；提交包为**模拟数据占位**，不具预测能力。
- 与项目目标差距：承诺"使用 NBA 数据集构建模型 + 诚实披露基线差距"尚未兑现；两条铁律（模拟数据永不提交 / game_id 强校验）仅后者在当前提交包中未满足。

## 7. 本周建议动作（最多3项）
- 建议1：[高] 解压并校验 `data/nba/` 各 CSV 字段（game_id/日期/主客队/收盘赔率/实际比分），据此构建主轨真实模型并评估——这是兑现双轨承诺的唯一路径。
- 建议2：[高] 复核 `a9810fd` 跨赛季 hold-out 可行性结论（2024-25 数据现已可得），产出修订报告，避免后续基于过时结论决策。
- 建议3：[中] 补建 CI 闸门（`.github/workflows` 跑 typecheck + audit），满足 AGENTS.md 推送前置（0 错误/0 泄漏），并修复 `validation_report.json`/manifest 的 GBK 乱码编码。

---

## 回传摘要（≤10 行）
1. Git：`main` @ `a9810fd`，仅 `data/nba/` 未跟踪，其余干净。
2. CI：**0 闸门**——根目录无 `.github/`，仅有本地 typecheck/lint 脚本未接入。
3. 文档：README/AGENTS 存在但非最新，**无 `PROJECT_VISION.md`**；validation_report.json 中文乱码。
4. 数据：`data/nba/` 7 个 zip 为 11-11 新下载，**全部未解压校验字段**。
5. 未决：TODO/FIXME 7 处；双轨执行待推进；跨赛季 hold-out 结论因 2024-25 数据已过时需复核。
6. 阻塞：无 CodaBench 官方 game_id → 真实提交不可能，提交包仍为模拟占位。
7. 能力边界：提交包/基线/数据获取已达成；**真实模型与真实评估未达成**（负结果如实标注）。
8. 建议：①解压校验数据建真实模型；②复核 hold-out 结论；③补 CI 闸门+修编码。
9. 报告归档：`docs/health-scan-2026-11-11.md`。
