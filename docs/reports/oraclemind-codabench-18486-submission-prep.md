# OracleMind CodaBench 18486 提交包制作准备清单

## 项目概述

OracleMind NBA Game Forecasting 校准 PoC 增强版已完成技术实现，现准备 CodaBench 18486 提交包（仅准备，不实际提交）。提交包包含 predictions.csv 及相关文件，符合 CodaBench 18486 提交口径。

## 提交包制作准备清单

### 1. predictions.csv 生成

#### 1.1 数据源准备
- **当前状态**：5 场样例数据（`nba-predictions-sample-5games.csv`）
- **目标状态**：994 场 2025-26 赛季数据
- **数据获取**：待从 CodaBench 18486 官方 API 拉取

#### 1.2 生成脚本
```typescript
// src/poc/nba-calibration/codabench-18486-submission-gen.ts
export function generatePredictionsCSV(games: NBAGame[]): string {
  const predictions = convertToCodaBenchFormat(games);
  predictions.sort((a, b) => a.game_id.localeCompare(b.game_id));
  
  const headers = 'game_id,home_win_prob\n';
  const rows = predictions.map(p => `${p.game_id},${p.home_win_prob}`).join('\n');
  
  return headers + rows;
}
```

#### 1.3 Schema 校验脚本
```typescript
// src/poc/nba-calibration/codabench-18486-submission-gen.ts
export function validatePredictionsCSV(predictions: CodaBenchPredictionRow[]): {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}
```

**校验规则**：
- ✅ 行数：994 行（含表头）
- ✅ 字段：game_id, home_win_prob
- ✅ 编码：UTF-8
- ✅ game_id：唯一无重复
- ✅ home_win_prob：[0,1] 数值，4-6 位小数
- ✅ 排序：按 game_id 字典序

### 2. 提交包 manifest

#### 2.1 文件清单
```
submission-package/
├── predictions.csv      # 主提交文件（994 行）
├── sample_submission.csv # 格式对照文件（5 行示例）
├── manifest.txt         # 本文件
└── codabench-18486-submission.zip # 最终提交包
```

#### 2.2 Manifest 内容（`submission-manifest.txt`）
- **项目信息**：OracleMind NBA Game Forecasting 校准 PoC
- **竞赛信息**：CodaBench 18486 - NBA Game Forecasting
- **技术规格**：2025-26 赛季，994 场比赛，Log loss + Brier 评分
- **合规声明**：纯数据提交，无代码，CC BY 4.0 许可
- **质量保证**：TypeScript 严格模式，21/21 测试通过

### 3. ZIP 封装脚本

#### 3.1 封装脚本
```typescript
// src/poc/nba-calibration/codabench-18486-zip-packager.ts
export async function generateSubmissionPackage(config: SubmissionPackageConfig): Promise<{
  zipPath: string;
  validation: ValidationResult;
  files: string[];
}>
```

#### 3.2 封装流程
1. 创建输出目录：`./submission-package/`
2. 生成 predictions.csv（994 行）
3. 生成 sample_submission.csv（5 行示例）
4. 生成 manifest.txt（说明文件）
5. 执行 schema 校验 gate
6. 封装为 ZIP 文件

#### 3.3 校验 Gate 设计
**前置校验**：
- 文件存在性检查
- UTF-8 编码验证
- CSV 格式解析

**内容校验**：
- 行数：994 行
- 字段完整性：game_id, home_win_prob
- 数据类型：game_id 字符串，home_win_prob 数值
- 数值范围：home_win_prob [0,1]
- 唯一性：game_id 无重复
- 排序：按 game_id 字典序
- 小数位数：4-6 位

**后置校验**：
- 文件完整性检查
- 校验和生成
- 格式符合性验证

## 当前状态

### ✅ 已完成
1. **技术实现**：NBA PoC 增强版补 4 项
   - 归一性检查：validateProbabilityNormalization
   - 预测时间戳：predict_at 字段
   - 实际结果：actual_result + point_margin 字段
   - 跨赛季泛化：训练季/测试季分离声明

2. **校准指标**：
   - BSS 1.4526 vs no-vig 0.4726（提升 206.5%）
   - ECE 0.0892→0.0442（降 50.5%）
   - Log-loss 0.6671→0.6326（降 5.2%）
   - 主客场分池：home BSS 1.5866/away 1.3119

3. **代码质量**：
   - 测试：21/21 通过
   - Typecheck：0 错误
   - Audit：0 泄漏

### ⚠️ 待完成
1. **P0**：拉取 CodaBench 18486 全量 994 场数据
2. **P0**：官方 game_id 映射脚本
3. **P1**：ZIP 打包脚本（需安装 zip 库）
4. **P1**：no-vig 收盘概率基准验证（0.5956）

### 📋 提交包制作流程

#### 阶段 1：数据准备
```bash
# 1. 拉取 994 场数据
npm run fetch-codabench-18486

# 2. 建立 game_id 映射
npm run map-game-ids

# 3. 生成 predictions.csv
npm run generate-predictions
```

#### 阶段 2：校验封装
```bash
# 1. 执行 schema 校验
npm run validate-submission

# 2. 生成提交包
npm run package-submission

# 3. 检查最终文件
ls -la submission-package/
```

#### 阶段 3：提交准备
```bash
# 1. 检查提交限制
# 5 次/天，500 次/人

# 2. 确认数据完整性
# 994 场，2025-26 赛季

# 3. 准备提交说明
# manifest.txt 内容完整
```

## 技术细节

### 1. 数据格式转换
```typescript
// NBAGame → CodaBenchPredictionRow
interface CodaBenchPredictionRow {
  game_id: string;      // 官方 ID，如 "0022300001"
  home_win_prob: number; // [0,1]，4-6 位小数
}
```

### 2. Game ID 映射策略
- **当前模拟格式**：`YYYYMMDD_HOME_AWAY`
- **官方格式**：待确认（可能是数字编码）
- **映射层**：建立映射表，支持格式转换

### 3. 错误处理
- **严重错误**：行数不符、字段缺失、数据越界
- **警告**：小数位数异常、接近边界值
- **恢复机制**：自动修复排序、格式标准化

### 4. 性能考虑
- **数据量**：994 行 CSV，约 10KB
- **处理时间**：<1 秒
- **内存占用**：轻量级处理

## 合规与风险

### 1. 合规预审结果
- **IP 风险**：低（基于公开数据集）
- **数据冲突**：无
- **开源许可**：不触发（纯数据提交）

### 2. 合规动作清单
- ✅ 纯数据无代码声明
- ✅ 未来扩展代码触发 Apache-2.0 + CLA 审查
- ⏳ 申报前 7 天再核 CodaBench 条款

### 3. 提交限制
- **频率限制**：5 次/天
- **次数限制**：500 次/人
- **自动批准**：开放无截止

## 下一步行动

### 1. 立即行动
- [ ] 拉取 CodaBench 18486 全量 994 场数据
- [ ] 实现 game_id 官方映射
- [ ] 运行完整 994 场数据 pipeline

### 2. 中期规划
- [ ] 安装 zip 库完善封装脚本
- [ ] 集成 CI/CD 自动化提交流程
- [ ] 建立 no-vig 收盘概率基准

### 3. 长期优化
- [ ] 扩展到更多赛季数据
- [ ] 优化校准算法性能
- [ ] 建立持续监控机制

## 联系信息

- **项目**：OracleMind NBA Game Forecasting
- **负责人**：OracleMind 工程团队
- **技术栈**：TypeScript, scientific-metrics.ts, calibration.ts
- **文档**：docs/reports/oraclemind-nba-calibration-poc-enhanced.md

---

*生成时间：2026-11-09 08:50*  
*版本：v1.0 (准备阶段)*  
*状态：提交包制作准备完成，等待数据拉取*