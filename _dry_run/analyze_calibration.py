# -*- coding: utf-8 -*-
"""回填完成后运行：用真实 LLM 预测 + 真实结局，计算校准前后 Brier/ECE/LogLoss/Accuracy 对比。

与生产 calibrator.ts 严格对齐：
  - 温度网格 [0.30, 3.00] 步长 0.05（T_GRID_MIN/MAX/STEP）
  - 目标 = 最小化 BCE（Binary Cross Entropy，Guo et al. ICML 2017 标准做法）
  - 输出 Brier / ECE / LogLoss / Accuracy 前后对比（calibrator.ts 的度量集）
  - 概率夹到 [0.01, 0.99]（P_MIN/P_MAX，防 log(0)/log(1) 爆炸）
  - 样本 < 10 时温度缩放不适用（MIN_SAMPLES_FOR_CALIBRATION）

用法: python analyze_calibration.py
"""
import json, os, math

SEED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "backfill-events.seed.json")

# ── 与 calibrator.ts 常量对齐 ──
P_MIN = 0.01
P_MAX = 0.99
T_GRID_MIN = 0.30
T_GRID_MAX = 3.00
T_GRID_STEP = 0.05
MIN_SAMPLES = 10


def clamp(p):
    if p is None or not math.isfinite(p):
        return 0.5
    return max(P_MIN, min(P_MAX, p))


def logit(p):
    c = clamp(p)
    return math.log(c / (1 - c))


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def apply_temperature(p, T):
    if not math.isfinite(T) or T <= 0:
        return clamp(p)
    return clamp(sigmoid(logit(p) / T))


# ── 度量（与 calibrator.ts 度量工具一致）──
def brier(ps, ys):
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps)


def logloss(ps, ys):
    total = 0.0
    for p, y in zip(ps, ys):
        p = clamp(p)
        lp = math.log(max(p, 1e-6))
        l1mp = math.log(max(1 - p, 1e-6))
        total -= y * lp + (1 - y) * l1mp
    return total / len(ps)


def ece(ps, ys, bins=10):
    """Expected Calibration Error：分桶加权平均 |置信度 - 实际频率|"""
    total = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        bucket = [(p, y) for p, y in zip(ps, ys) if lo <= p < hi or (b == bins - 1 and p == 1.0)]
        if not bucket:
            continue
        conf = sum(p for p, _ in bucket) / len(bucket)
        freq = sum(y for _, y in bucket) / len(bucket)
        total += abs(conf - freq) * (len(bucket) / len(ps))
    return total


def accuracy(ps, ys, thresh=0.5):
    correct = sum(1 for p, y in zip(ps, ys) if (p >= thresh) == (y == 1))
    return correct / len(ps)


def fit_temperature(ps, ys):
    """网格搜索 T 最小化 BCE（与 calibrator.fitTemperature 一致）"""
    def bce_at(T):
        total = 0.0
        for p, y in zip(ps, ys):
            cp = apply_temperature(p, T)
            lp = math.log(max(cp, 1e-6))
            l1mp = math.log(max(1 - cp, 1e-6))
            total -= y * lp + (1 - y) * l1mp
        return total / len(ps)

    best_T, best_bce = 1.0, bce_at(1.0)
    t = T_GRID_MIN
    while t <= T_GRID_MAX + 1e-9:
        b = bce_at(t)
        if b < best_bce:
            best_bce, best_T = b, t
        t = round(t + T_GRID_STEP, 2)
    return best_T, best_bce


def main():
    d = json.load(open(SEED, encoding="utf-8"))
    events = [e for e in d["events"] if e.get("predictedProbability") is not None]
    if not events:
        print("没有已回填事件！先跑 backfill_pilot.py 或等待其完成。")
        return
    ps = [clamp(e["predictedProbability"]) for e in events]
    ys = [1 if e["outcome"] == "positive" else 0 for e in events]
    n = len(ps)
    n_pos = sum(ys)
    print(f"有效样本: {n}  (positive {n_pos} / negative {n - n_pos})")
    print(f"原始概率分布: min={min(ps):.3f} max={max(ps):.3f} mean={sum(ps)/n:.3f}")

    # ── 基线：base-rate 常数预测 ──
    base_rate = sum(ys) / n
    base_ps = [base_rate] * n
    print(f"\n=== 基线对比 ===")
    print(f"Base-rate {base_rate:.3f}:  Brier={brier(base_ps,ys):.4f}  ECE={ece(base_ps,ys):.4f}  LogLoss={logloss(base_ps,ys):.4f}  Acc={accuracy(base_ps,ys):.3f}")

    # ── 原始 LLM ──
    raw_b = brier(ps, ys)
    raw_e = ece(ps, ys)
    raw_ll = logloss(ps, ys)
    raw_a = accuracy(ps, ys)
    print(f"原始 LLM (n={n}):   Brier={raw_b:.4f}  ECE={raw_e:.4f}  LogLoss={raw_ll:.4f}  Acc={raw_a:.3f}")

    # ── 温度缩放校准 ──
    if n >= MIN_SAMPLES:
        T, fit_bce = fit_temperature(ps, ys)
        cal_ps = [apply_temperature(p, T) for p in ps]
        cal_b = brier(cal_ps, ys)
        cal_e = ece(cal_ps, ys)
        cal_ll = logloss(cal_ps, ys)
        cal_a = accuracy(cal_ps, ys)
        print(f"温度缩放 T={T:.2f}:  Brier={cal_b:.4f}  ECE={cal_e:.4f}  LogLoss={cal_ll:.4f}  Acc={cal_a:.3f}")

        print(f"\n=== 校准效果 ===")
        for name, raw, cal in [("Brier", raw_b, cal_b), ("ECE", raw_e, cal_e),
                               ("LogLoss", raw_ll, cal_ll), ("Accuracy", raw_a, cal_a)]:
            dlt = raw - cal
            arrow = "改善" if dlt > 1e-9 else ("恶化" if dlt < -1e-9 else "持平")
            print(f"  {name:<9}: {raw:.4f} -> {cal:.4f}  ({arrow} {abs(dlt)*100:.2f}%)")
    else:
        print(f"\n样本 < {MIN_SAMPLES}，温度缩放不适用（与生产逻辑一致）")
        return

    # ── 分桶可靠性（校准前）──
    print(f"\n=== 可靠性分桶（校准前, 10桶）===")
    for b in range(10):
        lo, hi = b / 10, (b + 1) / 10
        bucket = [(p, y) for p, y in zip(ps, ys) if lo <= p < hi or (b == 9 and p == 1.0)]
        if not bucket:
            continue
        conf = sum(p for p, _ in bucket) / len(bucket)
        freq = sum(y for _, y in bucket) / len(bucket)
        print(f"  [{lo:.1f}-{hi:.1f}) n={len(bucket):3d}  声称={conf:.3f}  实际={freq:.3f}  差={conf-freq:+.3f}")

    # ── 分桶可靠性（校准后）──
    if n >= MIN_SAMPLES:
        print(f"\n=== 可靠性分桶（校准后 T={T:.2f}, 10桶）===")
        for b in range(10):
            lo, hi = b / 10, (b + 1) / 10
            bucket = [(p, y) for p, y in zip(cal_ps, ys) if lo <= p < hi or (b == 9 and p == 1.0)]
            if not bucket:
                continue
            conf = sum(p for p, _ in bucket) / len(bucket)
            freq = sum(y for _, y in bucket) / len(bucket)
            print(f"  [{lo:.1f}-{hi:.1f}) n={len(bucket):3d}  声称={conf:.3f}  实际={freq:.3f}  差={conf-freq:+.3f}")


if __name__ == "__main__":
    main()
