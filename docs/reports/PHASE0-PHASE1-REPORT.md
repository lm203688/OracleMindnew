# OracleMind 推演准确率提升 — Phase 0 基线 & Phase 1 路线（2026-08-11）

> 一句话结论：**"准确率不高"的根因不是算法差，是反馈闭环没有收到任何结果回报。**
> PySR / 符号回归 / 因果推断现在**跑不了**——它们都需要 `actualOutcome` 作训练目标，而目标是空的。
> 本轮先交付**诚实校准层**（零数据也能用）+ **符号回归管线就位**（数据一到即切换）。

---

## 一、Phase 0 基线实测（生产数据）

| 指标 | 数值 | 说明 |
|---|---|---|
| 预测记录总数 | **11** | `PredictionFeedback` 表 |
| 已验证结果数 | **0** | `actualOutcome` 全为空 → 校准循环**无信号** |
| 按类别分布 | general=11 | 其他类别（career/love/finance…）0 条 |
| avgBrierScore | 0.25 | 默认值（无验证数据时的退化值） |
| calibration / refinement | 1 / 0 | 退化值 |
| 通用用户反馈 | 9 条 | `userFeedback` 表（bug/建议类，非结果回报） |

> 注：`/api/feedback/stats` 返回的 `denied=11` 是 `total−verified` 的**误标**，并非"11 条都被判错"。真实情况是 **11 条全未验证**。

**结论**：系统能"记录预测"，但**从不让用户回报结果**。校准循环是死的，LLM 给的概率从未被校正过——这正是"感觉不准/太满"的来源。

---

## 二、为什么 PySR 现在不能上（诚实判断）

符号回归（PySR）、因果推断（DoWhy/EconML）、概率编程（NumPyro）都遵循同一范式：
```
特征 X  ──学──>  目标 y
```
这里的 `y` 必须是**真实发生的结果**（`actualOutcome: positive/neutral/negative`）。
当前 `y` 为 0 条 → 模型无东西可学 → 硬跑 = 用合成数据假装训练 = 演戏（违反项目"Precision Over Hype"红线）。

**所以真正要补的是数据漏斗，不是算法。**

---

## 三、本轮已交付（真实有用，不演戏）

### 1. 经验贝叶斯校准层 `src/lib/engines/calibration.ts`（新）
- `calibrateProbability(rawP, {sampleSize, baseRate})`：把 LLM 的过自信概率**收缩到诚实区间**。
  - `sampleSize=0` → 收缩到 0.5（"我们不知道"，最诚实）；
  - 数据增多 → 逐渐信任原始概率。
- 纯函数、可单测、**零数据安全**。
- **它本身就是未来 PySR 要消费的特征管线**：Phase 1 学到 `calibratedP = f(rawP, baseRate, sampleSize)`，现在先用保守先验 `f=收缩`，数据够了再替换成学到的公式。
- 已轻量接入 `getHistoricalAccuracyContext`：prompt 注入"建议最大声明置信度"（当前数据量下约 50–58%），抑制幻觉式笃定。

### 2. 符号回归试点脚本 `scripts/symbolic-pilot.py`（新）
- 用 **gplearn**（纯 Python，无需 500MB Julia）在**合成数据**上验证方法管线：
  能否从 `(rawP, baseRate, sampleSize)` 反推出可解释校准公式、R² 多少、能否编译成 JS。
- **明确标注**：这是"方法验证"，**非真实训练**。真实上线只需把 X/y 换成
  `PredictionFeedback` 的 `(rawP, categoryBaseRate, categorySampleSize) → actualOutcome`。
- Python 环境已就位（managed venv + numpy/pandas/sklearn/gplearn）。

---

## 四、真正的解锁点（需你拍板）

以下任一项才能开始**真实** Phase 1（在真实 outcome 上训练）：

**A. 结果回报漏斗（最高杠杆，强烈建议）**
当前 `/api/feedback/outcome` 接口能用，但**没接到任何 UI**。用户在预测结果页看不到"准了吗？👍/😐/👎"。
→ 我可在分享/结果页加一个 1-tap 回报组件（**新增、不改核心 UX**），让信号开始累积。
约 2–4 周就能攒到可训练的样本量。

**B. 给 DIRECT_URL / 或我加只读原始行导出端点**
一旦有 verified 数据，导出行级 `(特征 → outcome)` 即可跑 PySR。

**C. 先用 PySR(Julia) 替换 gplearn**
gplearn 是纯 Python 平替；生产级用 PySR 需装 Julia（~500MB），精度/可解释性更好。

---

## 五、建议落地顺序

1. ✅ 校准层已上线（诚实化当前输出）
2. ⏳ **你确认做 A（结果回报漏斗）** → 数据开始累积
3. ⏳ 数据 ≥ ~50 条/类别 → 跑真实 PySR（脚本已就绪）
4. ⏳ PySR 公式编译成 JS → Node 侧推理（双轨制合规，不暴露 substrate）

**不先补 A，任何算法都是空中楼阁。** 要我现在动手做 A 吗？
