#!/usr/bin/env python3
"""
OracleMind — Phase 1 符号回归试点 (方法验证)

重要声明（对齐 Precision Over Hype）：
    生产环境当前 11 条预测、0 条有验证结果(actualOutcome 全空)。
    因此本脚本**不在真实 outcome 上训练**——那会是演戏。
    这里用合成数据验证"符号回归能否从 (rawP, baseRate, sampleSize)
    反推出可解释校准公式"这一管线本身是否可行、产出是否可审计。

    一旦 /api/feedback/outcome 接到真实回报数据，把 SYNTHETIC 换成
    真实特征矩阵即可直接跑 Phase 1，公式可编译成 JS 供 Node 侧推理。

依赖：numpy pandas scikit-learn gplearn（managed venv）
运行：python scripts/symbolic-pilot.py
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from gplearn.genetic import SymbolicRegressor

RNG = 7
np.random.seed(RNG)

# ---------------------------------------------------------------------------
# 1) 合成数据：模拟"真实校准概率"如何由原始概率+基率+样本量决定
#    真实世界关系(我们假设的 ground truth，仅用于验证方法能学回来)：
#        trueP = baseRate + (rawP - baseRate) * (n/(n+20)) + 小噪声
# ---------------------------------------------------------------------------
N = 4000
rawP = np.random.uniform(0.05, 0.95, N)
baseRate = np.random.uniform(0.3, 0.7, N)
n = np.random.randint(0, 200, N)
noise = np.random.normal(0, 0.03, N)

shrink = n / (n + 20.0)
trueP = baseRate + (rawP - baseRate) * shrink + noise
trueP = np.clip(trueP, 0.01, 0.99)

df = pd.DataFrame({
    "rawP": rawP,
    "baseRate": baseRate,
    "sampleSize": n.astype(float),
    "trueP": trueP,
})

X = df[["rawP", "baseRate", "sampleSize"]].values
y = df["trueP"].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=RNG)

# ---------------------------------------------------------------------------
# 2) 符号回归：找可解释公式
# ---------------------------------------------------------------------------
est = SymbolicRegressor(
    population_size=4000,
    generations=40,
    tournament_size=20,
    stopping_criteria=0.001,
    const_range=(-1.0, 1.0),
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    feature_names=["rawP", "baseRate", "sampleSize"],
    parsimony_coefficient=0.01,
    random_state=RNG,
    n_jobs=1,
)

est.fit(X_train, y_train)
pred = est.predict(X_test)

r2 = r2_score(y_test, pred)
mse = mean_squared_error(y_test, pred)
print("=" * 64)
print("PHASE 1 SYMBOLIC REGRESSION — METHOD VALIDATION (synthetic data)")
print("=" * 64)
print(f"Samples (synthetic): {N}  | train/test split 75/25")
print(f"Discovered formula:")
print(f"    {est._program}")
print(f"Test R2 : {r2:.4f}")
print(f"Test MSE: {mse:.5f}")
print("-" * 64)
print("解读：")
print("  - 若 R2 接近 1，说明符号回归能从 (rawP, baseRate, sampleSize)")
print("    反推出稳定的可解释校准公式 —— Phase 1 管线可行。")
print("  - 该公式可直接编译成 JS，供 Node 侧推理(双轨制合规)。")
print("  - 真实上线时，把 X/y 换成 PredictionFeedback 的")
print("    (rawP, categoryBaseRate, categorySampleSize) -> actualOutcome 即可。")
print("=" * 64)
