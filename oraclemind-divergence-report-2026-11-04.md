# OracleMind 推送分叉差异报告

## 结论
远程 `origin/main`（`6490639f`）与本地 HEAD（`5b92019b`）**分叉**，非快进。合并需人工消解，属语义裁决。

## 关键数据
- 合并基 BASE = `4de5c49f`（10-08 08:44）
- 远程领先 161 提交（10-08~10-27，全部 lm203688）
- 本地领先 26 提交（11-04 合规四项 + ziwei/裁决/匿名化工程）
- 共享文件 74 个：29 内容相同（无冲突）、45 内容不同
- merge-tree 预判：**34 个真冲突**（16 add/add + 18 content）

## 冲突分类
### 16 add/add（双方各自独立新增同名文件，BASE 均不存在）
- .github/workflows/ci-gates.yml、prisma/migrations/migration_lock.toml
- 测试：bazi-solar-term/calibrator/science-layer/streak.test.ts
- 路由：accuracy/page.tsx、api/forecast、api/opentimestamps/anchor、api/public/accuracy
- 其他：outcome-return.tsx、global.d.ts、analytics.ts、domain-prior.ts、opentimestamps-anchor.ts、tsconfig.ci.json

### 18 content（双方改了同一文件不同内容）
- package.json、package-lock.json、schema.prisma、scripts/push-om.py
- 路由：feedback/outcome、arena/page、page.tsx
- 组件：landing-page-v3、pricing-page
- 库：automation/arena、bazi-engine、classical/bazi-foundation、classical/classical-llm-enhancer、engines/agent-factory、engines/event-corpus、engines/prediction-feedback、engines/structured-reasoning、science-layer

## 语义裁决要点
1. **合规四项是本地独有**：financial-scope.ts、payment-mode.ts、north-star.ts、ziwei-*、adjudication-* 远程均不存在 → 合并时**保留本地**，无覆盖风险。
2. **重复实现（本地 vs 远程独立完成同一功能）**：
   - calibrator.ts：**双方 329 行完全相同**（从同一来源同步）
   - science-layer.ts：双方做同一断链#6修复 + 温度校准接线（实现细节不同）
   - bazi-engine.ts：双方做同一 M02-P0-① 八字节气修复（实现细节不同）
   - schema.prisma：双方加同一批概率/校准字段（本地额外 calibratedBrierScore/predictedProbabilityAtResolve/version，远程额外 AnyJev/Certified）
3. **推送前置修复是本地独有且必要**：tsconfig.json exclude 测试文件（远程缺失，远程 next build 会含测试类型检查）；移除 next/font/google 网络依赖（远程仍有）；turbopack.root 锚定。
4. **远程含本地不需要的东西**：大量 chore（停用 auto-fix + 清理调试残留，141 个）、SCI-P0 论文实验、conformal-coldstart。

## 建议
- **保留本地合规四项**（金融排除、支付降级、北极星、推送前置）+ 本地 ziwei/裁决/匿名化/多基准。
- **重复实现择一**：calibrator（同内容）、science-layer/bazi-engine/schema 需人工挑选更完整实现或合两者。
- 远程的 141 个 chore + SCI-P0 论文实验属远程自身工作，合入无碍（不冲突）。
- 合并后**必须完整重测**（本地 398 测试基线基于旧 BASE，合并后需重验 + 类型检查 + build）。

## 风险
- schema.prisma 重复字段消解错误 → 生产迁移失败（需谨慎）
- 合并引入远程的调试残留/半成品（需确认远程质量）
- 合并后 Vercel 构建需验证（tsconfig exclude 是否与远程 CI 兼容）
