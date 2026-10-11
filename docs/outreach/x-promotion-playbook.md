# X 开源算法驱动推广作战包（OracleMind）

> 适用对象：OracleMind（可复现概率场引擎，融合古典框架 + 现代数据科学；**非占卜/算命**）。
> 目标社区：预测 / 推演人群（Metaculus、Manifold、LessWrong、forecasting 圈在 X 上极活跃）。
> 依据：X 2026-05 二次开源算法 `xai-org/x-algorithm`（Rust 重写、可跑推理，含 Phoenix ranker）。权重为**方向性**，非精确小数——生产值持续调参，按「量级」用。

---

## 0. 一句话结论

X 是当前**最透明**的主流推荐算法。它按「行为」计分、不按粉丝数，且**回复对话的权重碾压被动点赞**。这恰恰对 OracleMind 这种「小号 + 垂直专业」最友好：我们不用买粉，靠在预测社区里制造有信息量的对话就能出圈。

**反直觉但关键**：不要广播式发链接。带 URL 的主帖在 For You 出现频率低 50–70%。链接必须放「首条回复」或「简介」。

---

## 1. 真实排序信号（来自开源代码，方向性）

Phoenix ranker 预测 19 种互动动作，各自概率 × 权重求和得最终分。相对「点赞(1×)」的近似权重：

| 动作 | 相对权重 | 含义 / 我们的对策 |
|---|---|---|
| **作者回复发帖者的回复** | **≈ +75（~150×）** | 全系统最高正信号。发帖后**首小时亲自回复每个评论者**。 |
| 直接回复你的帖子 | ≈ +13.5（~27×） | 回复 > 转发 > 点赞。主帖要用**问题/反直觉结论**钩子驱动回复。 |
| 主页点击 + 互动 | ≈ +12（~24×） | 主帖要勾起「想看这人是谁」的好奇；简介要立住。 |
| 书签 | ≈ +10（~20×） | 内容要「可回看 / 有方法框架」。给可复用清单。 |
| 链接点击(停留 2min+) | ≈ +10–11（~22×） | 注意：这是「点了且停留」才给分；**但带外链的主帖本身被降权**——链接放回复。 |
| 转发 / 引用 | ≈ +1（~2×） | 扩散信号。长文被转发 = 进新受众。 |
| 点赞 | +0.5（基准） | 最弱正信号。别为点赞优化。 |
| 静音 / 屏蔽 / 少看 | **−74（~−148×）** | 强负信号。标题党 /  rage-bait 短期涨、长期被埋。 |
| 举报 | −369 | 灾难性。合规红线不能碰（本项目禁 horoscope/算命词即为此）。 |

**其他已证实机制：**
- **外链惩罚**：含 URL 的主帖 For You 曝光低 50–70%（X 商业模式要留人在平台）。→ 主帖零链接，URL 只进首条回复 + 简介。
- **原生长文 > 碎片线程**（2026 改）：单篇 25k 字(Premium)长文把信号聚合在一处；"1/15" 线程把互动拆散、反而吃亏。
- **媒体加成**：原生图 / 视频有正向特征。
- **早期速度**：发后 30–60min 的互动是最大分发杠杆（决定能否进 out-of-network 候选）。
- **作者声誉 Tweepcred**：粉丝**质量 > 数量**；稳定互动历史加分；被静音 / 取关直接扣分。
- **Premium 可见性乘子**：约 1.3×→1.6×（按季度升）。建议开 Premium（同时解锁 25k 长文）。

---

## 2. OracleMind 的 X 打法（反推）

**核心定位：不做广播，做「预测 / 推演社区对话」。**

1. **楔子 = 交叉验证事件预测**。我们刚把事件引擎接上 Manifold 真实共识（部署 `673f115`），正好对上预测社区每天在吵的「这事概率多少」。话术不是「来用我的产品」，而是「我做了个可复现的概率场，可以和你手上的 Metaculus/Manifold 共识对照，看分歧在哪」。
2. **主帖格式**：英文、原生长文、以**问题或反直觉结论**开头驱动回复；**绝不带链接**。
3. **首条回复**：放 OracleMind URL + 一句「把我的概率场和你那边的共识对照一下，分歧点更有意思」。
4. **首小时互动 SOP**：发帖后亲自快速回每个评论者（触发 ~150× 最高信号）。
5. **日常借势**：在预测 KOL / Metaculus / Manifold 官方帖子下写**有信息量**的回复（借大号触达），末尾轻带「我做了个可复现概率场」——不硬广。
6. **书签诱饵**：每篇给一个「可回看的方法框架 / 对照清单」，吃书签信号。
7. **合规护栏**：全程不出现 horoscope / fortune-telling / 算命 词；定位「古代推演框架 + 现代概率场」，与占卜切割——既守红线，也避 −148× 的「被当 spam / 举报」负信号。

---

## 3. 现成帖子草稿（英文，直接可用）

> 每条结构：`[主帖长文]` → `[首条回复带链接]` → `[互动回复模板]`。
> 主帖**一律零链接**；URL 只在首条回复出现。

### 草稿 A — 对标预测市场共识（最强楔子）
**主帖：**
> Most forecasting tools stop at "here's the probability." The interesting part is *where your number disagrees with the market.*
>
> I built a reproducible probability-field engine: same inputs always return the same index, and for event questions it now pulls the live Manifold community consensus as an external anchor. So instead of one opaque number, you get: your field index vs the crowd consensus, and the deviation between them.
>
> The disagreement is the signal. If my field says 27% and Manifold says 1% on "Fed cuts ≥3 times," that gap is worth a thread by itself.
>
> What's your go-to for sanity-checking a forecast — Metaculus, Manifold, or something I'm missing?

**首条回复：**
> Engine + method writeup here if you want to cross-check your own numbers: https://oraclemind.cc/geo/cross-check-event-forecasts.md — it's a reproducible field, not a black box, so you can re-run the same input and get the same output.

**互动回复模板（对评论者）：**
> Good push. The deviation is exactly what I'd look at first — want to paste the event and I'll show the field vs your source side by side?

---

### 草稿 B — 诚实自黑（"每次算都差不多"反思，引流）
**主帖：**
> Honest failure mode from building a forecast engine: early versions returned basically the same number every time. Not because the math was wrong — because the "intelligence" layer was silently returning zero results in production.
>
> The fix wasn't better math, it was real external signal. We wired in live prediction-market consensus so the index actually *moves* with evidence instead of echoing a prior.
>
> Lesson that transfers: if your model's outputs all look alike, suspect the data feed before the formula.
>
> What's the most embarrassing "it was just a null value" bug you've shipped?

**首条回复：**
> Writeup of the diagnosis + the market-consensus fix: https://oraclemind.cc/geo/forecast-accuracy-calibration.md

**互动回复模板：**
> Exactly — a null that gets silently defaulted is the worst kind. We made ours surface explicitly so it can't hide again.

---

### 草稿 C — 古典框架不证其对错（诚实护栏，立差异化）
**主帖：**
> A lot of "ancient framework + AI" products quietly claim the ancient part is *true*. I took the opposite stance.
>
> The classical substrate (here: a Chinese astrological tradition) is treated as a given prior — a structured starting point, not a truth claim. The part we actually validate is the modern computation: is it reproducible? Does it move with real signal? Does it stay non-degenerate across inputs?
>
> You can respect a 1,000-year-old reasoning structure without pretending it predicts your life.
>
> Where do you draw the line between "using a framework" and "believing it"?

**首条回复：**
> How we separate substrate from validation: https://oraclemind.cc/geo/classical-substrate.md

**互动回复模板：**
> Right — substrate is cheap to include, expensive to verify. We only verify the modern half.

---

### 草稿 D — 给预测者的实用对照清单（书签诱饵）
**主帖：**
> A 5-step habit for not fooling yourself on a forecast:
>
> 1. State your prior in writing *before* looking at anything.
> 2. Pull the live crowd consensus (Manifold / Metaculus).
> 3. Run your own reproducible model on the same input.
> 4. Compute the deviation between the two.
> 5. Write down which one you'd act on — and why the other is wrong.
>
> The deviation step is where most people shortcut. A forecast you can't disagree *with* isn't a forecast, it's a vibe.
>
> Save this and try it on one question this week. What breaks first?

**首条回复：**
> We turned step 3–4 into a reusable field engine: https://oraclemind.cc/geo/probability-vs-prediction.md — reproducible, so step 4 is auditable.

**互动回复模板：**
> The "write it before looking" part is underrated. Hindsight bias eats unrecorded priors for breakfast.

---

### 草稿 E — 反直觉：概率场不是算命（合规 + 切割）
**主帖：**
> "Probability field" sounds mystical. It isn't.
>
> It's a deterministic function: inputs → a number in [0,1], same input always same output. No spirits, no fate, just a reproducible score you can audit and disagree with.
>
> The mystic-sounding name is the baggage of the framework it's built on. The math is boring on purpose.
>
> What's a term in your field that scares newcomers but is actually just a function?

**首条回复：**
> The boring version, with the method spelled out: https://oraclemind.cc/geo/beyond-horoscopes.md

**互动回复模板：**
> Naming is half the battle — a good acronym does more onboarding work than a doc page.

---

## 4. 首小时互动 SOP + 节奏

- **频次**：每周 2–3 条主帖（草稿 A–E 轮替）+ 每日 5–10 条「借大号回复」。
- **窗口**：美东工作日白天（预测社区活跃；用 UTC 调度时对齐 ~14:00–20:00 UTC）。
- **发帖后 60 分钟**：主号亲自守，回复**每一个**评论者（触发 ~150× 最高信号）。哪怕只回一句「good point, here's the deviation…」。
- **借势回复模板**（贴在大号预测帖下）：
  > Solid thread. One thing I've found useful: cross-check the consensus against a *reproducible* field, not just another crowd. Differences surface the assumptions. (I put mine here: oraclemind.cc — no link in main, it's in my reply.)
  > *——链接放你自己的这条回复里，不污染人家主帖。*
- **书签驱动**：每条主帖至少有一个「可回看框架」，引导「save this」。
- **禁区**：主帖零外链；不碰 horoscope / 算命 / 医疗健康断言；不 rage-bait（−148× 负信号会埋帖）。

---

## 5. 诚实边界 / 下一步

- **本环境无法代发**：X 在国内直连不通、无 X 连接器，我**不能替你实际发帖**。本包交付物 = 策略 + 现成草稿，你或发帖通道拿去即用。
- **你需要**：(a) 一个 X 账号（建议 Premium，吃可见性乘子 + 25k 长文）；(b) 发帖通道——手动发，或提供 X API key（经代理可用）我可建**定时发帖 + 首小时自动互动**自动化。
- **可选进阶（暂不做）**：本地复刻 Phoenix ranker 的「19 动作打分」思路，做一个草稿打分器筛帖——成本高、边际收益低，先用手动草稿跑 4–8 周看信号。
- **与现有 GEO 资产的衔接**：`cross-check-event-forecasts.md` / `forecast-accuracy-calibration.md` / `classical-substrate.md` / `probability-vs-prediction.md` / `beyond-horoscopes.md` 五篇已上线，正是草稿里引流的落点；Bing/Yandex/indexnow.org 已提交（3/3 OK），X 引流会反哺这些页面的 LLM 引用。
