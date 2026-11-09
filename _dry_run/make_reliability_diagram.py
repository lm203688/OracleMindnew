# -*- coding: utf-8 -*-
"""生成校准可靠性图（纯 stdlib SVG，无 matplotlib 依赖）。

读取已回填 seed，计算原始 vs 温度缩放后的可靠性曲线，
输出 SVG 文件到 _dry_run/reliability-diagram.svg。

与生产 calibrator.ts 严格对齐（T 网格 [0.30,3.00] 步长 0.05，目标最小化 BCE）。
用法: python make_reliability_diagram.py [输出路径]
"""
import json, os, math, sys

SEED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "backfill-events.seed.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reliability-diagram.svg")

P_MIN, P_MAX = 0.01, 0.99
T_MIN, T_MAX, T_STEP = 0.30, 3.00, 0.05


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


def bce(ps, ys, T):
    total = 0.0
    for p, y in zip(ps, ys):
        cp = apply_temperature(p, T)
        lp = math.log(max(cp, 1e-6))
        l1mp = math.log(max(1 - cp, 1e-6))
        total -= y * lp + (1 - y) * l1mp
    return total / len(ps)


def fit_T(ps, ys):
    best_T, best = 1.0, bce(ps, ys, 1.0)
    t = T_MIN
    while t <= T_MAX + 1e-9:
        b = bce(ps, ys, t)
        if b < best:
            best, best_T = b, t
        t = round(t + T_STEP, 2)
    return best_T


def buckets(ps, ys, nbins=10):
    out = []
    for b in range(nbins):
        lo, hi = b / nbins, (b + 1) / nbins
        idx = [i for i, p in enumerate(ps) if lo <= p < hi or (b == nbins - 1 and p == 1.0)]
        if not idx:
            continue
        conf = sum(ps[i] for i in idx) / len(idx)
        freq = sum(ys[i] for i in idx) / len(idx)
        out.append((lo, hi, len(idx), conf, freq))
    return out


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    d = json.load(open(SEED, encoding="utf-8"))
    events = [e for e in d["events"] if e.get("predictedProbability") is not None]
    if not events:
        print("无已回填事件")
        return
    ps = [clamp(e["predictedProbability"]) for e in events]
    ys = [1 if e["outcome"] == "positive" else 0 for e in events]
    T = fit_T(ps, ys)
    cal_ps = [apply_temperature(p, T) for p in ps]
    n = len(ps)

    W, H, M = 720, 460, 60
    PLOT_W, PLOT_H = W - 2 * M, H - 2 * M

    def px(x):  # 概率→像素
        return M + x * PLOT_W

    def py(y):  # 概率(0..1) →像素（y 轴向下，0 在底）
        return H - M - y * PLOT_H

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI,Arial,sans-serif">')
    parts.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    parts.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-size="15" font-weight="bold" fill="#222">OracleMind 概率校准可靠性图（n={n}，T={T:.2f}）</text>')
    parts.append(f'<text x="{W/2}" y="42" text-anchor="middle" font-size="11" fill="#666">校准方法：温度缩放（网格最小化 BCE，与生产 calibrator.ts 对齐）</text>')

    # 网格
    for i in range(11):
        x = px(i / 10)
        parts.append(f'<line x1="{x:.1f}" y1="{py(0):.1f}" x2="{x:.1f}" y2="{py(1):.1f}" stroke="#eee" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="{py(0)+14:.1f}" text-anchor="middle" font-size="9" fill="#999">{i/10:.1f}</text>')
        y = py(i / 10)
        parts.append(f'<line x1="{px(0):.1f}" y1="{y:.1f}" x2="{px(1):.1f}" y2="{y:.1f}" stroke="#eee" stroke-width="1"/>')
        parts.append(f'<text x="{px(0)-6:.1f}" y="{y+3:.1f}" text-anchor="end" font-size="9" fill="#999">{i/10:.1f}</text>')

    # 理想对角线
    parts.append(f'<line x1="{px(0):.1f}" y1="{py(0):.1f}" x2="{px(1):.1f}" y2="{py(1):.1f}" stroke="#bbb" stroke-width="1.5" stroke-dasharray="5,4"/>')
    parts.append(f'<text x="{px(0.82):.1f}" y="{py(0.82)-6:.1f}" font-size="9" fill="#888">理想（校准完美）</text>')

    # 原始曲线（红/青）
    rb = buckets(ps, ys)
    if len(rb) >= 2:
        pts = " ".join(f"{px((lo+hi)/2):.1f},{py(freq):.1f}" for lo, hi, cnt, conf, freq in rb)
        parts.append(f'<polyline points="{pts}" fill="none" stroke="#e5484d" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        for lo, hi, cnt, conf, freq in rb:
            cx, cy = px((lo + hi) / 2), py(freq)
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="#e5484d"/>')
    parts.append(f'<text x="{px(0.98):.1f}" y="{py(0.06):.1f}" text-anchor="end" font-size="11" fill="#e5484d" font-weight="bold">原始 LLM</text>')

    # 校准后曲线（绿）
    cb = buckets(cal_ps, ys)
    if len(cb) >= 2:
        pts = " ".join(f"{px((lo+hi)/2):.1f},{py(freq):.1f}" for lo, hi, cnt, conf, freq in cb)
        parts.append(f'<polyline points="{pts}" fill="none" stroke="#30a46c" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        for lo, hi, cnt, conf, freq in cb:
            cx, cy = px((lo + hi) / 2), py(freq)
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="#30a46c"/>')
    parts.append(f'<text x="{px(0.98):.1f}" y="{py(0.15):.1f}" text-anchor="end" font-size="11" fill="#30a46c" font-weight="bold">校准后 (T={T:.2f})</text>')

    # 轴标签
    parts.append(f'<text x="{W/2}" y="{H-8:.1f}" text-anchor="middle" font-size="11" fill="#444">预测概率（声称）</text>')
    parts.append(f'<text x="14" y="{H/2:.1f}" text-anchor="middle" font-size="11" fill="#444" transform="rotate(-90 14 {H/2:.1f})">实际频率</text>')

    parts.append("</svg>")
    svg = "\n".join(parts)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"已生成: {OUT}")
    print(f"样本 n={n}，最优 T={T:.2f}")
    print(f"分桶（原始）: " + ", ".join(f"[{lo:.1f}-{hi:.1f}):n{cnt}/f{freq:.2f}" for lo, hi, cnt, conf, freq in rb))
    print(f"分桶（校准后）: " + ", ".join(f"[{lo:.1f}-{hi:.1f}):n{cnt}/f{freq:.2f}" for lo, hi, cnt, conf, freq in cb))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        OUT = sys.argv[1]
    main()
