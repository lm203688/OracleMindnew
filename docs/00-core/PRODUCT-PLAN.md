# OracleMind Product Plan: Free vs Paid Differentiation

> 项目定位：虚拟实验室（Virtual Laboratory）——融合中国古代哲学框架与现代数据科学的多维概率场推演引擎。详见 `ORACLEMIND_MANIFESTO.md`。
> 本文档为 Phase 1 产品规划基线，部分措辞（如"probability %"）已随引擎升级调整为「综合倾向指数」，以符合 Precision Over Hype 原则。

## Core Philosophy
Free users get a "taste" — fast, simple, one answer.  
Paid users get a "deep dive" — comprehensive analysis, personal profile, history, and ongoing insights.

---

## 1. User Profile System

### Profile Fields
- Name (optional display name)
- Birth Date (year/month/day)
- Birth Time (hour)
- Birth Place
- Current Location
- Saved as localStorage for guests, DB for logged-in users

### Auto-fill Behavior
- If profile exists, pre-fill all birth fields in config panel
- Daily forecast auto-runs with profile data (no re-entry)
- "My Profile" page accessible from nav dropdown

---

## 2. Free vs Paid Result Pages

### FREE — "Quick Insight"
- 综合倾向指数（Composite Tendency Index，非统计概率，附方法说明：贝叶斯先验15% + 蒙特卡洛45% + Agent共识40%）
- One plain-English sentence
- 3 scenario bars (Best/Moderate/Tough)
- "Upgrade for full report" CTA

### PAID — "Deep Analysis Report"
- All of FREE, plus:
- **Executive Summary** (3-4 paragraph narrative)
- **Timing Guidance** (when to act, when to wait)
- **Key Turning Points** (specific dates/timeframes)
- **Risk/Reward Breakdown** (detailed pros/cons)
- **Historical Context** (compare to past similar forecasts in the lab notebook)
- **Action Items** (3 specific next steps)
- **Download as PDF** button

---

## 3. Feedback System
- Floating feedback button (bottom-right)
- Modal form: Type (Bug / Feature Request / General), Message, Email (optional)
- Submit to /api/feedback endpoint
- Store in database

---

## 4. Implementation Phases

### Phase 1: Profile + Auto-fill
- Profile page UI
- localStorage persistence
- Auto-fill in config panel

### Phase 2: Paid Report Expansion
- Extended result data structure
- Full report UI component
- PDF generation

### Phase 3: Feedback System
- Floating button + modal
- API endpoint
- Admin dashboard (optional)

### Phase 4: Daily Convenience
- Daily forecast auto-run on login
- Quick re-forecast from history
- Trend dashboard
