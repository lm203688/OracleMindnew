# -*- coding: utf-8 -*-
"""SCI 校准复现包 — 一键编排：回填完成后运行。

执行链：
  1. 校验 seed 回填完整度（缺数据则报告并退出）
  2. 运行校准分析（原始 vs 温度缩放 Brier/ECE/LogLoss/Accuracy）
  3. 生成可靠性图 SVG
  4. 汇编 SCI 复现报告 Markdown（含方法学 + 关键数字 + 分桶表）

与生产 calibrator.ts 严格对齐（BCE 目标、T 网格 [0.30,3.00]、clamp [0.01,0.99]、样本<10 不校准）。

用法: python run_sci_analysis.py
"""
import json, os, math, sys, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, "..", "data", "backfill-events.seed.json")
ANALYZER = os.path.join(HERE, "analyze_calibration.py")
DIAGRAM = os.path.join(HERE, "make_reliability_diagram.py")
SVG_OUT = os.path.join(HERE, "reliability-diagram.svg")
REPORT = os.path.join(HERE, "SCI-reproducibility-report.md")


def check_backfill():
    d = json.load(open(SEED, encoding="utf-8"))
    evs = d["events"]
    filled = [e for e in evs if e.get("predictedProbability") is not None]
    n = len(evs)
    return n, len(filled), evs, filled


def run_step(name, cmd):
    print(f"\n=== {name} ===", flush=True)
    r = subprocess.run([sys.executable, cmd], capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    print(out, flush=True)
    return out


def main():
    n, filled, evs, done = check_backfill()
    print(f"回填完整度: {filled}/{n}")
    if filled < n:
        print(f"⚠️ 仍有 {n-filled} 条未回填。请先等 backfill_pilot.py 完成（后台 PID 54736）。")
        print("    可先用当前部分数据试跑，但最终 SCI 数字必须等 100% 回填后才是权威结论。")
        return

    # 1) 分析
    out_analyze = run_step("校准分析（原始 vs 温度缩放）", ANALYZER)

    # 2) 可靠性图
    out_diagram = run_step("生成可靠性图 SVG", DIAGRAM)

    # 3) 汇编报告 —— 从 analyze 输出解析关键数字
    print(f"\n=== 汇编 SCI 复现报告 → {os.path.relpath(REPORT, HERE)} ===", flush=True)

    # 解析关键数字
    def grab_all(pattern, default=None):
        import re
        m = re.search(pattern, out_analyze)
        return list(m.groups()) if m else default

    def grab_one(pattern, default="—"):
        import re
        m = re.search(pattern, out_analyze)
        return m.group(1) if m else default

    # 原始 LLM 行：n, Brier, ECE, LogLoss, Acc
    raw_metrics = grab_all(r"原始 LLM \(n=(\d+)\):\s+Brier=([\d.]+)\s+ECE=([\d.]+)\s+LogLoss=([\d.]+)\s+Acc=([\d.]+)")
    # 温度缩放行：T, Brier, ECE, LogLoss, Acc
    cal_metrics = grab_all(r"温度缩放 T=([\d.]+):\s+Brier=([\d.]+)\s+ECE=([\d.]+)\s+LogLoss=([\d.]+)\s+Acc=([\d.]+)")
    n_samples = grab_one(r"有效样本: (\d+)")
    n_pos = grab_one(r"positive (\d+)")

    lines = []
    lines.append("# OracleMind 概率校准 SCI 复现报告")
    lines.append(f"\n> 生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 数据：seed 事件回填 {filled}/{n}（真实 LLM 预测 + 真实结局）")
    lines.append("> 校准方法：温度缩放（网格搜索最小化 BCE，与生产 `calibrator.ts` 严格对齐）")
    lines.append("")
    lines.append("## 1. 方法学")
    lines.append("")
    lines.append("- **框架**：open-ended probabilistic forecasting（个人生活事件概率预测），非时序外推")
    lines.append("- **校准目标**：回答「说 60% 时真的 60% 吗」——校准层把 LLM next-token 概率变校准概率")
    lines.append("- **校准方法**：`p_cal = sigmoid(logit(p) / T)`，温度 T 在 [0.30, 3.00] 网格以 0.05 步长扫，")
    lines.append("  目标最小化 **BCE**（Binary Cross Entropy，Guo et al. ICML 2017 标准做法）")
    lines.append("- **概率夹取**：`clamp(p) = min(0.99, max(0.01, p))`，防 log(0)/log(1) 爆炸")
    lines.append("- **最小校准样本**：n < 10 时温度缩放不适用（与生产逻辑一致）")
    lines.append("- **度量**：Brier / ECE / LogLoss / Accuracy（校准前后对比）")
    lines.append("")
    lines.append("## 2. 样本概览")
    lines.append("")
    lines.append(f"- 有效样本：**{n_samples}**（positive {n_pos} / negative {int(n_samples)-int(n_pos) if n_samples != '—' and n_pos != '—' else '—'}）")
    lines.append("")
    lines.append("## 3. 校准前后对比")
    lines.append("")
    lines.append("| 度量 | 原始 LLM | 温度缩放后 | 变化 |")
    lines.append("|---|---|---|---|")
    if raw_metrics and cal_metrics:
        # raw_metrics = [n, Brier, ECE, LogLoss, Acc]; cal_metrics = [T, Brier, ECE, LogLoss, Acc]
        labels = ["Brier", "ECE", "LogLoss", "Accuracy"]
        for i, label in enumerate(labels):
            rv = float(raw_metrics[i + 1])
            cv = float(cal_metrics[i + 1])
            dlt = rv - cv
            arrow = "改善" if dlt > 1e-9 else ("恶化" if dlt < -1e-9 else "持平")
            lines.append(f"| {label} | {rv:.4f} | {cv:.4f} | {arrow} {abs(dlt)*100:.2f}% |")
    else:
        lines.append("| Brier | — | — | — |")
    lines.append("")
    lines.append("## 4. 可靠性分桶")
    lines.append("")
    lines.append("```")
    # 提取可靠性分桶段（含校准前 + 校准后两个小节）
    in_bucket = False
    bucket_lines = []
    for line in out_analyze.splitlines():
        if "可靠性分桶" in line:
            in_bucket = True
        if in_bucket and ("差=" in line or "可靠性分桶" in line):
            bucket_lines.append(line)
    # 只保留含"差="的桶行，并按出现顺序 append（前10条=校准前，后10条=校准后）
    for line in bucket_lines:
        lines.append(line)
    lines.append("```")
    lines.append("")
    lines.append("## 5. 可靠性图")
    lines.append("")
    lines.append(f"![可靠性图]({os.path.relpath(SVG_OUT, HERE)})")
    lines.append("")
    lines.append("## 6. 结论与注意")
    lines.append("")
    lines.append("- 若 T > 1：LLM 系统性地**过度自信**（概率分布过于极端），压平后更准")
    lines.append("- 若 T < 1：LLM 系统性地**欠自信**，锐化后更准")
    lines.append("- **关键**：校准方向必须用实测数据判定，不能凭「LLM 天然过度自信」的直觉假设")
    lines.append("- **接线缺口**：`forecasting/calibrator.ts` 目前仅 dry-run 使用；生产 predict 路径仍走旧 `engines/calibration.ts`。")
    lines.append("  本报告为 SCI 论文复现包的核心产出（校准层有效性证明），生产接线属 owner 决策项。")
    lines.append("")

    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"报告已写入: {os.path.relpath(REPORT, HERE)}")


if __name__ == "__main__":
    main()
