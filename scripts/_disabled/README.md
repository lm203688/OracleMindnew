# ⚠️ Disabled Scripts — 禁止在生产/论文中使用

本目录中的脚本因**学术诚信风险**或**已废弃**而被停用，**绝不可**用于：
- 校准飞轮的数据来源
- SCI 论文的实验数据
- 生产环境的冷启动
- 任何形式的实验产物

---

## 目录内容

### `cold-start-seed.mjs`（已停用 2026-10-19）

**停用原因（SCI 报告 2026-10-19 第三节 · 红色警报）**：

该脚本是 OracleMind 唯一向 `PredictionFeedback` 灌数据的脚本，但其数据本质是**编造**：

1. **自洽循环**：`actualOutcome` 与 `predictedDirection` 取同一值 → Brier 是人为构造的低值，不是模型在真实世界上的表现。
2. **非真实决议**：事件是"未来式猜测"（如 2025 年发新 GPU），`reportedAt` 却填当前时间，没有真实决议真值。
3. **零外部可核验**：没有任何 `source` URL，不可被审计，不属于任何公开预测基准。

**替代方案**：`scripts/coldstart-backfill.mjs`（读取 `data/backfill-events.seed.json` 的真实已决事件）。

**清理历史遗留数据**：
```bash
# 已执行的标记（见 prisma/migrations/add_backfill_integrity_fields.sql）
UPDATE "PredictionFeedback"
SET "isBackfilled" = TRUE
WHERE "question" LIKE '[cold-start-seed]%';
```

---

## 复活规则

如需恢复使用某脚本，必须：
1. 完整改造以移除造假逻辑（改为读取外部真实数据源）
2. 补齐 source URL 追溯链
3. 通过 `scripts/audit-public-terms.mjs` 与新增的数据完整性 lint
4. 在 `docs/paper/` 中留下变更说明
5. 通过至少 1 位非作者的同行 review

在此之前，**保持停用状态**。
