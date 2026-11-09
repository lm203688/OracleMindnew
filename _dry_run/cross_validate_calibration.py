# -*- coding: utf-8 -*-
"""样本外交叉验证温度缩放校准 —— 判断校准是否真的泛化（决定性证据）。

背景：analyze_calibration.py 报告的 T=1.90 是在同一批 305 条上"拟合再评估"
（样本内拟合），ECE -4.88% 偏乐观。本脚本用 5 折分层交叉验证：
  - 每折在训练集拟合 T（最小化 BCE），在测试集评估
  - 聚合所有折的 OOS 预测 → 计算真实泛化的 Brier/ECE/LogLoss/Accuracy
  - 与原始 LLM 对比 → 判断校准是否在未见数据上仍有效

如果 OOS 改善成立 → 接入生产有据；如果 OOS 改善塌缩 → 样本内 T 是过拟合，
应诚实报告"校准仅样本内成立"。

与 analyze_calibration.py 共享常量与度量函数（同一来源，保证一致性）。
用法: python cross_validate_calibration.py
"""
import json, os, math, random
import analyze_calibration as ac

SEED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "backfill-events.seed.json")

FOLDS = 5
RANDOM_SEED = 42


def stratified_folds(ps, ys, folds=FOLDS, seed=RANDOM_SEED):
    """按结局分层划分 k 折，保证每折正负比例接近总体。"""
    rng = random.Random(seed)
    pos_idx = [i for i, y in enumerate(ys) if y == 1]
    neg_idx = [i for i, y in enumerate(ys) if y == 0]
    rng.shuffle(pos_idx)
    rng.shuffle(neg_idx)

    # 每个索引分到哪一折
    fold_of = {}
    for k in range(folds):
        for i in pos_idx[k::folds]:
            fold_of[i] = k
        for i in neg_idx[k::folds]:
            fold_of[i] = k
    return fold_of


def main():
    d = json.load(open(SEED, encoding="utf-8"))
    events = [e for e in d["events"] if e.get("predictedProbability") is not None]
    if len(events) < ac.MIN_SAMPLES * 2:
        print(f"样本不足交叉验证：{len(events)} < {ac.MIN_SAMPLES * 2}")
        return

    ps = [ac.clamp(e["predictedProbability"]) for e in events]
    ys = [1 if e["outcome"] == "positive" else 0 for e in events]
    n = len(ps)
    n_pos = sum(ys)
    print(f"有效样本: {n}  (positive {n_pos} / negative {n - n_pos})")
    print(f"交叉验证: {FOLDS} 折分层（按结局），随机种子 {RANDOM_SEED}")
    print(f"温度网格 [{ac.T_GRID_MIN}, {ac.T_GRID_MAX}] 步长 {ac.T_GRID_STEP}，目标=最小化 BCE")
    print()

    fold_of = stratified_folds(ps, ys)

    # ── 基线：base-rate 常数预测 ──
    base_rate = sum(ys) / n
    base_ps = [base_rate] * n
    print(f"=== 基线（base-rate {base_rate:.3f}）===")
    print(f"  Brier={ac.brier(base_ps, ys):.4f}  ECE={ac.ece(base_ps, ys):.4f}  LogLoss={ac.logloss(base_ps, ys):.4f}  Acc={ac.accuracy(base_ps, ys):.3f}")
    print()

    # ── 原始 LLM ──
    raw_b = ac.brier(ps, ys)
    raw_e = ac.ece(ps, ys)
    raw_ll = ac.logloss(ps, ys)
    raw_a = ac.accuracy(ps, ys)
    print(f"=== 原始 LLM (n={n}) ===")
    print(f"  Brier={raw_b:.4f}  ECE={raw_e:.4f}  LogLoss={raw_ll:.4f}  Acc={raw_a:.3f}")
    print()

    # ── 交叉验证：每折拟合 T，测试集评估 ──
    oos_ps = [None] * n          # 样本外校准概率（聚合）
    fold_ts = []
    print(f"=== 5 折交叉验证 ===")
    for k in range(FOLDS):
        train_idx = [i for i in range(n) if fold_of[i] != k]
        test_idx = [i for i in range(n) if fold_of[i] == k]
        tr_ps = [ps[i] for i in train_idx]
        tr_ys = [ys[i] for i in train_idx]
        te_ps = [ps[i] for i in test_idx]
        te_ys = [ys[i] for i in test_idx]

        if len(tr_ps) < ac.MIN_SAMPLES:
            # 训练不足，用 T=1.0（不校准）
            T_fold = 1.0
        else:
            T_fold, _ = ac.fit_temperature(tr_ps, tr_ys)
        fold_ts.append(T_fold)

        # 测试集应用该折 T
        for j, i in enumerate(test_idx):
            oos_ps[i] = ac.apply_temperature(te_ps[j], T_fold)

        # 该折测试集表现
        te_cal = [ac.apply_temperature(p, T_fold) for p in te_ps]
        print(f"  折{k}: train={len(tr_ps)} test={len(te_ps)}  T={T_fold:.2f}  "
              f"test: Brier={ac.brier(te_cal, te_ys):.4f}  ECE={ac.ece(te_cal, te_ys):.4f}  "
              f"LogLoss={ac.logloss(te_cal, te_ys):.4f}  Acc={ac.accuracy(te_cal, te_ys):.3f}")

    # 聚合 OOS 度量
    oos_b = ac.brier(oos_ps, ys)
    oos_e = ac.ece(oos_ps, ys)
    oos_ll = ac.logloss(oos_ps, ys)
    oos_a = ac.accuracy(oos_ps, ys)
    avg_T = sum(fold_ts) / len(fold_ts)
    print()
    print(f"=== 样本外（OOS）聚合结果 ===")
    print(f"  各折 T 值: {[round(t,2) for t in fold_ts]}  均值 T={avg_T:.2f}")
    print(f"  Brier={oos_b:.4f}  ECE={oos_e:.4f}  LogLoss={oos_ll:.4f}  Acc={oos_a:.3f}")

    # ── 对比 ──
    print()
    print("=== 样本内 vs 样本外 校准效果（相对原始 LLM）===")
    rows = [("Brier", raw_b, oos_b), ("ECE", raw_e, oos_e),
            ("LogLoss", raw_ll, oos_ll), ("Accuracy", raw_a, oos_a)]
    for name, raw, oos in rows:
        dlt = raw - oos
        arrow = "改善" if dlt > 1e-9 else ("恶化" if dlt < -1e-9 else "持平")
        print(f"  {name:<9}: {raw:.4f} -> {oos:.4f}  ({arrow} {abs(dlt)*100:.2f}%)")

    # ── 结论判定 ──
    print()
    print("=== 判定 ===")
    ece_gain = raw_e - oos_e
    ll_gain = raw_ll - oos_ll
    verdicts = []
    if ece_gain > 0.005 and ll_gain > 0.005:
        verdicts.append(f"✅ OOS 改善显著：ECE {ece_gain*100:.2f}%、LogLoss {ll_gain*100:.2f}% —— 校准在未见数据上仍有效，接入生产有据")
    elif ece_gain > 0 and ll_gain > 0:
        verdicts.append(f"⚠️ OOS 改善存在但较弱：ECE {ece_gain*100:.2f}%、LogLoss {ll_gain*100:.2f}% —— 校准部分泛化，接入生产需谨慎（建议与 in-sample 差距作为不确定性报告）")
    else:
        verdicts.append(f"❌ OOS 无改善或恶化：ECE {ece_gain*100:.2f}%、LogLoss {ll_gain*100:.2f}% —— 样本内 T 是过拟合，校准仅在样本内成立，不应直接接入生产")
    for v in verdicts:
        print(v)

    # 输出机器可读结果（供编排器/报告复用）
    result = {
        "n": n, "n_pos": n_pos, "folds": FOLDS,
        "fold_Ts": [round(t, 2) for t in fold_ts], "avg_T": round(avg_T, 2),
        "raw": {"brier": round(raw_b, 4), "ece": round(raw_e, 4), "logloss": round(raw_ll, 4), "acc": round(raw_a, 3)},
        "oos": {"brier": round(oos_b, 4), "ece": round(oos_e, 4), "logloss": round(oos_ll, 4), "acc": round(oos_a, 3)},
        "base_rate": round(base_rate, 3),
        "ece_gain_pct": round(ece_gain * 100, 2),
        "logloss_gain_pct": round(ll_gain * 100, 2),
    }
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cv_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n结果已存 {out_path}")


if __name__ == "__main__":
    main()
