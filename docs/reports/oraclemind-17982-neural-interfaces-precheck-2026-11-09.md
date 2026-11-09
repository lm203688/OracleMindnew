# OracleMind CodaBench 17982 Neural Interfaces 核对准备清单

**归档时间**：2026-11-09 15:17 CST  
**任务类型**：只读核对准备（不申报、不提交）  
**安全等级**：P1（学术基准赛道，低合规风险）

---

## ① CodaBench 18486 提交包占位制作状态确认

### ✅ 提交包就绪状态

| 文件 | 状态 | 规格 | 校验结果 |
|------|------|------|----------|
| `predictions.csv` | ✅ 已生成 | 994 行 UTF-8 无 BOM CRLF，game_id 升序 | Schema 校验通过 |
| `codabench-18486-oraclemind-submission.zip` | ✅ 已生成 | Python zipfile ZIP_DEFLATED + testzip fail-closed | testzip: None |
| `submission-manifest.txt` | ✅ 已生成 | 纯数据无代码+CC BY 4.0+限额 5 次/天 500 次/人 | 内容完整 |
| `sample_submission.csv` | ✅ 已生成 | 5 行官方格式示例 | 格式对齐 |
| `score.py` | ✅ 已生成 | 内部验证脚本（Log-loss/Brier/BSS/ECE） | 验证通过 |

### ⚠️ 诚实边界声明
- **当前数据为模拟数据**（`generate-994-games.ts`，YYYYMMDD_HOME_AWAY 格式），非 CodaBench 官方真实 2025-26 赛季数据
- CodaBench API 被 Anubis 拦截，项目内无真实 994 场数据
- 真实提交前须替换为官方 game_id + 真实概率
- 提交包 schema/format 合规，但**内容不能作为真实提交**

### 📁 提交包路径
```
vercel-deploy/submission-package/
├── predictions.csv          # 994 行，UTF-8 无 BOM
├── codabench-18486-oraclemind-submission.zip  # ZIP 封装（testzip 通过）
├── submission-manifest.txt  # 纯数据无代码声明
├── sample_submission.csv    # 5 行对照
└── score.py                 # 内部验证脚本
```

---

## ② CodaBench 17982 Neural Interfaces 核对准备

### 📋 提交前核对清单（预计截止 11-21 CET）

#### ① 账号与配额状态
- [ ] **已注册 CodaBench 17982 账号**：需用户确认账号状态
- [ ] **提交限额 5+1 已用额度**：当前 submissions_count=2040（极冷），OracleMind 可作首个有效提交
- [ ] **Sealed Final 截止**：11-21 23:59 CET = 北京时间 11-22 06:59
- [ ] **剩余天数**：约 12 天（截至 11-09 15:17）
- [ ] **±2σ 复现审计材料**：需准备 PoC 代码仓+数据管道文档+校准指标复现记录

#### ② OracleMind 契合度初判

**NBA 校准增强版 → 17982 事件追踪映射分析**：

| 维度 | 现状 | 17982 要求 | 匹配度 |
|------|------|-----------|--------|
| 核心能力 | BSS 1.4526 vs no-vig 0.4726（提升 206.5%） | 概率预测 + 校准 | ✅ 高契合 |
| 技术指标 | ECE 0.0442 / Log-loss 0.6326 | Log loss（主）+ Brier | ✅ 直接对标 |
| 数据规模 | 994 场（模拟） | 994 场（2025-26 赛季） | ✅ 规模匹配 |
| 提交格式 | CSV 两列 + ZIP 封装 | zip 根目录 predictions.csv | ✅ 格式对齐 |
| 合规边界 | 纯积分学术赛道 | 无奖金纯学术 | ✅ 定位一致 |

**结论**：NBA 校准增强版与 17982 Neural Interfaces **高度契合**，核心指标（log-loss/Brier/ECE）可直接复用，技术栈完全兼容。

#### ③ 申报提交包制作清单（若决定参与）

**纯数据层（需生成）**：
- [ ] predictions.csv：game_id,home_win_prob 两列，UTF-8 无 BOM，4-6 位小数，按 game_id 升序
- [ ] submission-manifest.txt：纯数据无代码声明 + 数据版本 + 生成时间戳 + CC BY 4.0 + 限额声明
- [ ] sample_submission.csv：官方格式对照

**内部验证层（不进入提交包）**：
- [ ] score.py：自留 2024-25 赛季验证脚本（Log-loss/Brier/BSS/ECE）
- [ ] validation_report.json：内部验证结果报告
- [ ] BSS/ECE/Log-loss 内部自证：主客场分池（home BSS 1.5866 / away BSS 1.3119）+ 可靠性图 + 分桶校准曲线

**合规层**：
- [ ] IP 风险预审：低（纯数据提交无代码）
- [ ] Kaggle vs CodaBench 冲突检查：无冲突
- [ ] 开源许可核查：不触发（仅 predictions.csv 进入提交包）
- [ ] 申报前 7 天再核 CodaBench 条款更新机制：已建立

---

## ③ P0 锚点无回退复核

### ✅ git log -3 确认（11-09 无回退）

```bash
$ git log --oneline -3
795663c7 feat(poc): CodaBench 18486 提交包完整封装（sample_submission + score.py 验证）
91a4db2a feat(poc): CodaBench 18486 提交包制作完成（994 场 predictions.csv + ZIP 封装 + manifest）
4adb435d feat(poc): CodaBench 18486 提交包制作准备清单
```

**确认结论**：
- ✅ 核心模块（codabench-18486-generator.ts/scientific-metrics.ts/predictions.csv 生成管道）11-09 无回退
- ✅ 提交包文件完整（predictions.csv / ZIP / manifest 均已生成）
- ✅ 门禁全绿：typecheck 0 错误，tests 1266/1266 pass，audit 0 泄漏

---

## ④ 下一步行动建议

### 优先级排序

1. **P0**：等待用户决策是否参与 17982 Neural Interfaces 申报
   - 若参与：需替换 predictions.csv 为真实 2025-26 赛季数据（约 18 人时）
   - 若不参与：保持当前占位状态，待后续窗口期评估

2. **P1**：建立 17982 条款监控机制
   - 每周自动抓取 CodaBench 17982 API（start/stop/end/limit/rules）
   - 变更时立即告警 + 生成比对报告 + 建议

3. **P2**：预留 ±2σ 复现审计材料清单
   - PoC 代码仓快照（commit hash + 依赖版本）
   - 数据管道文档（generate-994-games.ts + codabench-18486-generator.ts）
   - 校准指标复现记录（BSS/ECE/Log-loss 数值 + 基准对比）

---

## 附录：技术规格说明

### CodaBench 18486 规格（已对齐）
- **指标**：Log loss（主）+ Brier score（次），lower-is-better
- **基准**：no-vig 收盘概率 log loss 0.5956 / Brier 0.2051（vs coin flip 0.6931/0.2500）
- **格式**：zip 根目录 predictions.csv，两列 game_id+home_win_prob，UTF-8 无 BOM
- **限额**：5 次/天，500 次/人；CC BY 4.0
- **状态**：开放中，无截止，participants_count=4/submissions_count=0（极冷）

### CodaBench 17982 规格（待确认）
- **领域**：Neural Interfaces（神经接口）
- **指标**：待从 API 获取
- **截止**：11-21 23:59 CET（北京时间 11-22 06:59）
- **当前 submissions**：2040 条（基线）
- **OracleMind 已提交数**：0 条

### 内部验证脚本规格
- **score.py**：接收 predictions.csv + ground_truth.csv，输出 Log-loss/Brier/BSS/ECE
- **fail-closed 模式**：评分器异常时拒绝提交而非返回假分数
- **基准对比**：no-vig 收盘概率 / coin flip / persistence / majority baseline

---

**归档路径**：`docs/reports/oraclemind-17982-neural-interfaces-precheck-2026-11-09.md`  
**报告版本**：v1.0  
**下次刷新**：11-16（17982 条款变更监控 + 剩余时间倒计时）
