"""
OracleMind Forecasting Stack — Dry Run
=====================================
用 data/backfill-events.seed.json 的 305 条已决事件回算：
1. 几种基线预测器的 Brier / ECE / Log-loss
2. 模拟一个"过度自信的 LLM" 输出，量化 temperature scaling 能改进多少
3. 给出 AnyJev 式校准是否值得上的量化判断

不启动 LLM。用启发式预测来演示"有偏概率 → 校准"的差值。
"""
import json
import math
import statistics
from collections import defaultdict

# ---------- 加载数据 ----------
with open("../data/backfill-events.seed.json", encoding="utf-8") as f:
    d = json.load(f)
events = d["events"]

# outcome: positive=1, negative=0
def to_bin(o):
    if o == "positive": return 1
    if o == "negative": return 0
    return None  # neutral

# ---------- 基线 1: 全预测 0.5（无信息）----------
def baseline_flat():
    return [0.5] * len(events)

# ---------- 基线 2: category base rate ----------
def baseline_category():
    cat_pos = defaultdict(list)
    for e in events:
        y = to_bin(e["outcome"])
        if y is None: continue
        cat_pos[e["category"]].append(y)
    cat_rate = {c: sum(v)/len(v) for c, v in cat_pos.items()}
    return [cat_rate[e["category"]] for e in events]

# ---------- 基线 3: category × horizon 分层 ----------
def baseline_horizon():
    # 长 horizon 事件不确定性更大，向 0.5 收缩
    cat_pos = defaultdict(list)
    for e in events:
        y = to_bin(e["outcome"])
        if y is None: continue
        cat_pos[e["category"]].append(y)
    cat_rate = {c: sum(v)/len(v) for c, v in cat_pos.items()}
    preds = []
    for e in events:
        p = cat_rate[e["category"]]
        h = e["horizonDays"]
        # horizon 越长越向 0.5 收缩（不确定性更大）
        if h > 365:  shrink = 0.5
        elif h > 90: shrink = 0.3
        elif h > 30: shrink = 0.15
        else:        shrink = 0.05
        preds.append(p * (1-shrink) + 0.5 * shrink)
    return preds

# ---------- 模拟一个"过度自信的 LLM" ----------
# 假设：LLM 系统性高估自己——真值 0.5 时它倾向输出 0.7 或 0.3
# 用 category base rate 作为真值，然后施加"过度自信"变换
def simulate_overconfident_llm():
    preds = baseline_category()
    # 过度自信变换：p' = (p-0.5) * 1.8 + 0.5，然后 clip
    out = []
    for p in preds:
        p2 = (p - 0.5) * 1.8 + 0.5
        out.append(max(0.05, min(0.95, p2)))
    return out

# ---------- AnyJev 式校准：温度缩放 ----------
# 找最优 T 使得 calibrated logits 的 BCE 最小
def calibrate_temperature(preds, ys):
    """
    在 1D 上做网格搜索 T ∈ [0.3, 3.0]，选 BCE 最小的 T
    这是 AnyJev L1 层的核心操作之一（temperature scaling）
    """
    def bce(T):
        total = 0.0
        for p, y in zip(preds, ys):
            # 温度缩放：logit(p) = log(p/(1-p))
            logit = math.log(max(p, 1e-6) / max(1-p, 1e-6))
            logit_t = logit / T
            p_c = 1 / (1 + math.exp(-logit_t))
            p_c = max(p_c, 1e-6)
            p_c = min(p_c, 1 - 1e-6)
            total -= (y * math.log(p_c) + (1-y) * math.log(1 - p_c))
        return total / len(preds)
    best_T, best_loss = 1.0, float("inf")
    T = 0.3
    while T <= 3.0:
        l = bce(T)
        if l < best_loss:
            best_loss, best_T = l, T
        T += 0.05
    return best_T, best_loss

def apply_temperature(preds, T):
    out = []
    for p in preds:
        logit = math.log(max(p, 1e-6) / max(1-p, 1e-6))
        logit_t = logit / T
        p_c = 1 / (1 + math.exp(-logit_t))
        out.append(p_c)
    return out

# ---------- 指标计算 ----------
def brier(preds, ys):
    return sum((p-y)**2 for p, y in zip(preds, ys)) / len(preds)

def logloss(preds, ys):
    total = 0.0
    for p, y in zip(preds, ys):
        p = max(p, 1e-6); p = min(p, 1-1e-6)
        total -= (y * math.log(p) + (1-y) * math.log(1-p))
    return total / len(preds)

def ece(preds, ys, bins=10):
    """Expected Calibration Error, 等宽分箱"""
    bin_edges = [(i/bins, (i+1)/bins) for i in range(bins)]
    total = 0.0
    N = len(preds)
    for lo, hi in bin_edges:
        idx = [i for i, (p, y) in enumerate(zip(preds, ys)) if lo <= p < hi]
        if not idx: continue
        n = len(idx)
        avg_p = sum(preds[i] for i in idx) / n
        avg_y = sum(ys[i] for i in idx) / n
        total += (n / N) * abs(avg_p - avg_y)
    return total

def accuracy(preds, ys, thr=0.5):
    return sum(1 for p, y in zip(preds, ys) if (p >= thr) == (y == 1)) / len(ys)

# ---------- 主流程 ----------
ys = []
for e in events:
    y = to_bin(e["outcome"])
    if y is None: continue
    ys.append(y)

# 对齐事件（跳过 neutral）
events_aligned = [e for e in events if to_bin(e["outcome"]) is not None]
N = len(ys)
print(f"有效样本数：{N}  (positive={sum(ys)}, negative={N-sum(ys)})")
print(f"整体正例率：{sum(ys)/N:.3f}")
print()

results = []

# 1. 无信息基线
p = baseline_flat()
results.append(("A. Flat 0.5 (无信息)", p))

# 2. Category base rate
p = baseline_category()
results.append(("B. Category base rate", p))

# 3. Category × horizon
p = baseline_horizon()
results.append(("C. Category × horizon", p))

# 4. 模拟过度自信的 LLM
p = simulate_overconfident_llm()
results.append(("D. Overconfident LLM (模拟)", p))

# 5. 校准后的过度自信 LLM
p_cal = p
T, bce_loss = calibrate_temperature(p, ys)
p_cal = apply_temperature(p, T)
results.append((f"E. Overconfident + TempScale(T={T:.2f})", p_cal))

print(f"{'方法':40s} | {'Brier':>7s} | {'LogLoss':>7s} | {'ECE':>6s} | {'Acc':>6s}")
print("-" * 80)
for name, preds in results:
    b = brier(preds, ys)
    ll = logloss(preds, ys)
    e = ece(preds, ys)
    a = accuracy(preds, ys)
    print(f"{name:40s} | {b:7.4f} | {ll:7.4f} | {e:6.4f} | {a:6.3f}")

print()
print("=" * 80)
print("结论分析")
print("=" * 80)

# 对比 D 和 E
d_brier = brier(results[3][1], ys)
e_brier = brier(results[4][1], ys)
d_ece = ece(results[3][1], ys)
e_ece = ece(results[4][1], ys)
print(f"\n过度自信 LLM (D) → 温度缩放校准 (E):")
print(f"  Brier: {d_brier:.4f} → {e_brier:.4f}   Δ={e_brier-d_brier:+.4f}")
print(f"  ECE:   {d_ece:.4f} → {e_ece:.4f}   Δ={e_ece-d_ece:+.4f}")

# 对比 C 和 E
print(f"\nCategory×horizon 基线 (C) vs 校准后 LLM (E):")
print(f"  Brier: {brier(results[2][1], ys):.4f} vs {e_brier:.4f}")
print(f"  ECE:   {ece(results[2][1], ys):.4f} vs {e_ece:.4f}")
