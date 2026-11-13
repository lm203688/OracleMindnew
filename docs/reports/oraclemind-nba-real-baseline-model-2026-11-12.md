# OracleMind 主轨真实基线模型报告（2026-11-12）

> 任务来源：Chief `oraclemind-dualtrack-1111` 建议①（主轨 Kaggle NBA Game Forecasting）
> 执行：OracleMind 工程 Agent
> 脚本：`vercel-deploy/scripts/nba-real-baseline.py`
> 输出：`docs/reports/real_baseline_report.json` + `real_baseline_predictions.csv`

## 1. 数据校验（7 个 zip 解压后核验）

| 数据集 | 来源/许可 | 赛事级? | 2024-25 覆盖 | game_id | 备注 |
|---|---|---|---|---|---|
| nba-closing-lines-ats-2024-25 | minmaxer / CC BY 4.0 | 是 | 1314 场 ✅ | 9 位字母数字（如 `0ptyAqOi`） | 含开盘/收盘赔率、分差、大小分、主客比分 |
| nba-closing-lines-ats-2025-26 | minmaxer / CC BY 4.0 | 是 | 1315 场（测试） | 同上 | 同上 |
| nba-betting-data-october-2007-to-june-2024 | cviaxmiwnptr / CC0 | 是 | 含 2024 部分 | 无 | 24440 行 ×27 列，2008–2026 |
| nba-nhl-and-college-basketball-results-and-odds | archangel0x01 / MIT | 是 | 1386 场 ✅ | 数值型 | games.csv 178245×19 |
| nba-odds-and-scores | erichqiu / CC0 | 是 | ❌ 仅 2012-13–2018-19 | 10 位（0021200001） | 无 2024-25 |
| nba-aba-baa-stats | sumitrodatta / CC0 | 否（球员/球队统计） | — | — | 无赛事级赔率 |
| nba-money-line-betting-model-2025-2026 | ryancasey2 / CC0 | 否（xlsx/png） | — | — | 无赛事级 CSV |

**关键复核结论**：2024-25 赛季真实赛事级数据**现已可得**（minmaxer 2024-25 1314 场、archangel0x01 1386 场）。
因此 `docs/reports/oraclemind-nba-holdout-validation-feasibility-2026-11-10.md` 中"2024-25 数据不可得 → 跨赛季 hold-out 不可做"的
历史结论**需修正**：跨赛季 hold-out 现已可行（本报告 §3 即为实证）。

## 2. 诚实边界（铁律执行）

1. **模拟数据永不提交**：本次未提交任何内容。主轨评估使用 Kaggle 真实数据，非模拟。
2. **game_id 强校验**：CodaBench 官方 test 集 game_id 因 Anubis 反爬拦截**未取得**，
   因此本报告使用的 game_id 是 **Kaggle 数据内部 game_id**，**非 CodaBench 官方测试集 game_id**。
   → 当前**不具备真实提交资格**（无官方 game_id 映射），辅轨维持模拟占位不变。
3. 特征严格赛前化：仅用开盘/收盘赔率、分差、大小分、博彩公司数；赛后字段（比分、overtime、ats_result）不入特征，避免泄漏。

## 3. 模型与评估（跨赛季 hold-out：2024-25 训练 → 2025-26 测试，1315 场）

| 模型 | logloss | Brier | ECE | BSS | LL gap vs 收盘线 |
|---|---|---|---|---|---|
| 市场收盘线（baseline） | 0.5761 | 0.1970 | 0.0241 | 0.2056 | +0.0000 |
| 市场开盘线 | 0.5861 | 0.2013 | 0.0176 | 0.1885 | +0.0100 |
| 逻辑回归（赛前特征） | 0.5760 | 0.1968 | 0.0309 | 0.2067 | −0.0001 |
| 常数（训练主队胜率） | 0.6872 | 0.2470 | 0.0118 | 0.0042 | +0.1111 |

**诚实结论**：
- 逻辑回归模型与**市场收盘线几乎完全持平**（LL gap −0.0001），**未产生超越市场的 alpha**。
- ECE 反而略高于收盘线（0.0309 vs 0.0241），校准略差。
- 常数基线 logloss 0.6872 显著更差（+0.1111），说明市场线确有信息量。
- **不宣称预测能力，不宣称跑赢市场。**

## 4. 门禁状态

| 门禁 | 结果 | 说明 |
|---|---|---|
| typecheck | ✅ PASS (exit 0) | `tsc --noEmit` 通过 |
| audit（红线词） | ❌ FAIL (1 处) | `seo-factory.ts:215` 红线词检测器，属**既有提交代码**，非本次引入，需决策 |

audit 唯一命中 `vercel-deploy/src/lib/automation/seo-factory.ts:215`：
`const redLineTerms = [/horoscope/i, /fortune\s*tell/i, ..., /命盘/i, /八字/i, /紫微/i];`
该行是**防御性检测器**（检测到红线词即扣分），但 audit 白名单提示词表未覆盖 `redLineTerms`，故被误报为泄漏。
**属既有状态，非本次改动**；是否放行需 Chief/用户决策（见 §5）。

## 5. 未决与建议

1. **[需决策] audit 误报**：建议在 audit 白名单 `DEFENSIVE_HINTS` 增加 `redLineTerms` / `red-line-terms`（防御性包含），或对检测器做中性化改写。**属红线相关改动，需用户/Chief 确认后再动。**
2. 主轨真实模型已完成并归档；但**真实提交仍不可能**（缺 CodaBench 官方 game_id）。
3. 跨赛季 hold-out 可行性结论已修正为"可行"（见 §1）。
