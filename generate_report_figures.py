from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "report_assets"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.facecolor": "#F7F9FC",
    "axes.facecolor": "#F7F9FC",
    "text.color": "#162536",
    "axes.labelcolor": "#425466",
    "xtick.color": "#425466",
    "ytick.color": "#425466",
})

# Data verified from https://oraclemind.cc/api/public/accuracy on 2026-10-27.
categories = ["政治", "政策", "科技", "经济", "科学", "加密货币"]
counts = [17, 5, 17, 15, 12, 10]
briers = [0.083, 0.092, 0.139, 0.146, 0.160, 0.177]
overall = 0.133

fig, ax = plt.subplots(figsize=(11.5, 6.4), dpi=180)
colors = ["#2A9D8F", "#2A9D8F", "#4E7CA1", "#4E7CA1", "#D99A3D", "#D99A3D"]
bars = ax.barh(categories[::-1], briers[::-1], color=colors[::-1], height=0.58)
ax.axvline(overall, color="#7C5CBF", linestyle=(0, (5, 4)), linewidth=2, label="总体 Brier 0.133")
for bar, value, n in zip(bars, briers[::-1], counts[::-1]):
    ax.text(value + 0.003, bar.get_y() + bar.get_height()/2, f"{value:.3f}  ·  n={n}", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(0, 0.215)
ax.set_xlabel("Brier 分数（越低越好）")
ax.set_title("公开 76 题回测的分域表现", loc="left", fontsize=18, fontweight="bold", pad=20)
ax.text(0, 1.025, "同一回测内部仍有明显分域差异；政策仅 5 题，不能据此作稳定领域结论。", transform=ax.transAxes, fontsize=10.5, color="#5B6B7C")
ax.legend(loc="lower right", frameon=False)
ax.grid(axis="x", color="#DDE4EC", linewidth=0.8, alpha=0.8)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.text(0.01, 0.012, "来源：OracleMind /api/public/accuracy，2026-10-27 实测。该图不是与外部产品的同题比较。", fontsize=9, color="#6A7785")
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig(OUT / "oraclemind-category-brier.png", bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close(fig)

# Target operating loop: a conceptual diagram, not a statistical claim.
fig, ax = plt.subplots(figsize=(14, 7.5), dpi=180)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis("off")
ax.text(0.4, 7.45, "OracleMind 目标闭环：从一次答案到可验证决策资产", fontsize=20, fontweight="bold")
ax.text(0.4, 6.98, "每一次预测都带结算标准、证据时点、同题基线、模型版本与更新条件。", fontsize=11, color="#5B6B7C")

steps = [
    ("1", "澄清问题", "个人 / 公共事件\n行动选项与期限"),
    ("2", "定义结算", "可观察结果\n来源与到期时间"),
    ("3", "冻结证据", "来源时间戳\n证据独立性"),
    ("4", "建立基线", "50/50 · 类别基率\n同题市场 / 人群"),
    ("5", "输出预测", "原始概率 + 校准概率\n数值 / 日期 / 条件分布"),
    ("6", "形成决策", "关键驱动与反证\n下一步与更新触发器"),
    ("7", "跟踪更新", "概率变化及原因\n到期提醒与可取消运行"),
    ("8", "客观结算", "独立结局来源\n满意度另行记录"),
    ("9", "复盘学习", "同题 BSS 与校准曲线\n个人 / 模型 / 领域分层"),
]
positions = [(0.5, 5.15), (3.25, 5.15), (6.0, 5.15), (8.75, 5.15), (11.5, 5.15),
             (11.5, 2.15), (8.75, 2.15), (6.0, 2.15), (3.25, 2.15)]
box_colors = ["#E4F2EF", "#E4F2EF", "#E8EEF5", "#E8EEF5", "#EAE5F5", "#F8EEDD", "#F8EEDD", "#F4E7E4", "#E4F2EF"]

for i, ((num, title, body), (x, y), color) in enumerate(zip(steps, positions, box_colors)):
    box = FancyBboxPatch((x, y), 2.0, 1.35, boxstyle="round,pad=0.04,rounding_size=0.12", linewidth=1.1, edgecolor="#C8D3DF", facecolor=color)
    ax.add_patch(box)
    ax.text(x + 0.16, y + 1.08, num, fontsize=10, fontweight="bold", color="#7C5CBF")
    ax.text(x + 0.45, y + 1.06, title, fontsize=12.5, fontweight="bold")
    ax.text(x + 0.16, y + 0.42, body, fontsize=9.5, color="#425466", va="center")

arrow_positions = []
for i in range(4):
    x, y = positions[i]
    nx, ny = positions[i+1]
    arrow_positions.append(((x+2.02, y+0.68), (nx-0.04, ny+0.68)))
arrow_positions.append(((12.5, 5.1), (12.5, 3.55)))
for i in range(5, 8):
    x, y = positions[i]
    nx, ny = positions[i+1]
    arrow_positions.append(((x-0.04, y+0.68), (nx+2.04, ny+0.68)))
for start, end in arrow_positions:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15, linewidth=1.5, color="#6C8296"))

# Feedback loop back to calibration and evidence, avoiding a claim of automatic improvement.
ax.add_patch(FancyArrowPatch((3.25, 2.45), (1.5, 5.05), connectionstyle="arc3,rad=-0.28", arrowstyle="-|>", mutation_scale=16, linewidth=1.6, linestyle=(0, (5, 4)), color="#2A9D8F"))
ax.text(0.45, 3.25, "仅客观结算进入校准\n反馈用于产品改进", fontsize=10, color="#237A70", fontweight="bold")

ax.text(0.5, 0.55, "护城河不在 Agent 数量，而在不可篡改的历史记录、同题增量、真实结算与用户长期决策上下文。", fontsize=12, color="#162536", fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "oraclemind-target-operating-loop.png", bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close(fig)

print(OUT / "oraclemind-category-brier.png")
print(OUT / "oraclemind-target-operating-loop.png")
