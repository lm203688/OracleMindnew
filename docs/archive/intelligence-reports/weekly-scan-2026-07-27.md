# OracleMind Weekly Intelligence Scan

**Date:** 2026-07-27
**Scan Type:** Automated weekly ecosystem intelligence
**Status:** COMPLETE (platform DB offline — research scan proceeded)

---

## 1. Platform Metrics

| Metric | Value | Source |
|--------|-------|--------|
| Total Forecasts | 0 | `GET https://oraclemind.cc/api/automation/weekly-scan` |
| Total Users | 0 | `GET https://oraclemind.cc/api/automation/weekly-scan` |
| API Status | `degraded` | API response |
| Scan Date (API) | 2026-07-26 | API response |

> **Note:** Platform metrics returned `0 forecasts / 0 users` with error `"Database query failed, returning defaults"`. The production database is not yet connected to the oraclemind.cc deployment. The `/api/automation/weekly-scan` endpoint correctly falls back to a no-op proxy per the project's defensive design, so the API itself is reachable — only persistence is broken. This must be resolved before any user-traffic or conversion metrics can be collected.

---

## 2. GitHub Repos — Trending Prediction / Forecasting (Past 7 Days)

### 2.1 Nixtla/nixtla (PRIMARY — highest relevance)

| Field | Detail |
|-------|--------|
| Repo | [Nixtla/nixtla](https://github.com/Nixtla/nixtla) |
| Description | SDK for **TimeGPT**, the first production foundation model for time-series forecasting and anomaly detection. Zero-shot inference, fine-tuning, prediction intervals, irregular timestamps, exogenous variables. |
| Latest Release | **v0.8.0** — released **Jul 21, 2026** [$TRAE_REF](https://github.com/Nixtla/nixtla/releases/tag/v0.8.0) |
| Key Recent Change | PR #836 switched the **default model from `timegpt-1` to `timegpt-2.1`** (Jul 13, 2026) — major accuracy/ capability uplift [$TRAE_REF](https://github.com/Nixtla/nixtla) |
| Activity | 1,086 commits; last commit Jul 23, 2026; 49 releases; 150 dependents |
| Star Count | [unverified — not displayed on fetched page; repo is a widely-adopted forecasting SDK] |
| License | Apache 2.0 (SDK); TimeGPT model is closed-source (API access) |
| **Relevance to OracleMind** | **Very High.** OracleMind's core value prop is probabilistic forecasting. TimeGPT-2.1 offers zero-shot forecasting across domains (finance, web traffic, events) with prediction intervals — directly aligned with OracleMind's "answer → probability → scenarios" result structure. The shift to timegpt-2.1 as default signals a measurable accuracy jump worth benchmarking. |

### 2.2 Nixtla/neuralforecast (SECONDARY — supporting relevance)

| Field | Detail |
|-------|--------|
| Repo | [Nixtla/neuralforecast](https://github.com/Nixtla/neuralforecast) |
| Description | Unified interface for training/forecasting with neural architectures (N-BEATS, N-HITS) and traditional statistical methods. Self-hostable, no API dependency. [$TRAE_REF](https://blog.csdn.net/weixin_42612804/article/details/160536996) |
| Star Count | [unverified] |
| **Relevance to OracleMind** | **Medium-High.** Provides a fully open-source, self-hostable forecasting backbone — useful if OracleMind wants to avoid vendor lock-in on the closed-source TimeGPT API and keep user data on its own infrastructure (aligns with the user-data-ownership principle). N-HITS has shown SOTA long-horizon performance. |

### 2.3 Hicruben/world-cup-2026-prediction-model (CONTEXTUAL — low relevance)

| Field | Detail |
|-------|--------|
| Repo | github.com/Hicruben/world-cup-2026-prediction-model |
| Description | Open-sourced (MIT) World Cup 2026 prediction model, no ML — rule/statistics-based forecast. [$TRAE_REF](https://dev.to/jerry_chen_dbaa6838e17336/i-open-sourced-a-world-cup-2026-prediction-model-and-tested-it-honestly-44d1) |
| **Relevance to OracleMind** | **Low.** Domain-specific and non-ML, but demonstrates the "honest forecast + open methodology" narrative that resonates with prediction audiences. Marketing/positioning reference only. |

---

## 3. HuggingFace Models — New Forecasting Models (2026)

### 3.1 taharnbl/TS-ICL (PRIMARY — most relevant new model)

| Field | Detail |
|-------|--------|
| Model | [taharnbl/TS-ICL](https://huggingface.co/taharnbl/TS-ICL) |
| Full Name | TS-ICL: A Flexible Time-Indexed Foundation Model for Time Series via In-Context Learning |
| Published | **Jun 4, 2026** (arXiv v2: Jun 13, 2026) [$TRAE_REF](https://huggingface.co/papers/2606.05878) |
| Authors | Etienne Le Naour, Tahar Nabil, Adrien Petralia (EDF R&D) |
| arXiv | 2606.05878 [$TRAE_REF](https://arxiv.org/html/2606.05878) |
| Approach | Probabilistic **in-context learning** foundation model; flexible time-indexed architecture. Accompanied by a pretraining corpus (JuaAI/ts-icl-pretraining-corpus). |
| License | tsicl-v1 (custom — review before commercial use) |
| **Relevance to OracleMind** | **High.** In-context learning means the model adapts to a new series from examples at inference time — no per-domain fine-tuning. This matches OracleMind's need to forecast arbitrary user-posed questions across heterogeneous topics. Probabilistic outputs map directly onto OracleMind's probability-display requirement. |

### 3.2 amazon/chronos-bolt-base (SECONDARY — mature, license-friendly)

| Field | Detail |
|-------|--------|
| Model | [a12354/chronos-bolt-base (Chronos-Bolt⚡ Base)](https://huggingface.co/a12354/chronos-bolt-base) |
| Architecture | T5-based time-series foundation model; pretrained, zero-shot forecasting [$TRAE_REF](https://huggingface.co/a12354/chronos-bolt-base) |
| arXiv | 2403.07815 |
| License | **Apache 2.0** (commercial-friendly) |
| **Relevance to OracleMind** | **Medium-High.** Permissively licensed and self-hostable — the safest choice if OracleMind must run forecasting on its own infra to honor user-data-ownership. Bolt variant is optimized for fast inference. Less recent than TS-ICL but far more mature and deployment-ready. |

---

## 4. Actionable Recommendations

1. **Benchmark TimeGPT-2.1 as the primary forecasting backend.** Nixtla switched its SDK default to `timegpt-2.1` on Jul 13, 2026 — the first default-model change in over a year and a strong signal of a real accuracy uplift [$TRAE_REF](https://github.com/Nixtla/nixtla). OracleMind should run a side-by-side accuracy/latency benchmark (TimeGPT-2.1 vs. current backend) on a fixed evaluation set; if TimeGPT-2.1 wins, migrate the `/api/forecast` path to it. Prediction-interval support aligns with OracleMind's probability display layer.

2. **Resolve the production DB connection before any growth work.** Platform metrics are stuck at 0/0 because the database is not connected. Per prior session notes, `DATABASE_URL` in Vercel is malformed ("invalid domain character"). This is the single highest-leverage fix this week — without it, no user, forecast, or conversion data can be captured, and the entire automated customer-acquisition loop cannot measure itself.

---

## 5. ACTION ITEMS (This Week)

- [ ] **[BLOCKER] Fix `DATABASE_URL` / `DIRECT_URL` in Vercel environment variables** for the `oraclemind` project (malformed — "invalid domain character"). Reverify via `GET /api/feedback/stats` returning real data. This unblocks all metrics collection.
- [ ] **Integrate TimeGPT-2.1** via the Nixtla SDK (v0.8.0) as a candidate forecasting backend; wrap in try/catch with English fallback per existing ZAI SDK pattern. Benchmark accuracy + latency vs. current backend on 20–30 sample OracleMind questions.
- [ ] **Pilot Chronos-Bolt-Base (Apache 2.0)** as a self-hostable, privacy-preserving fallback/alternative backend — directly supports the user-data-ownership constraint and removes single-vendor API dependency.
- [ ] **Evaluate TS-ICL license (tsicl-v1)** for commercial compatibility; if cleared, prototype in-context-learning forecasting for heterogeneous user questions (no per-domain fine-tuning needed).
- [ ] **Monitor Nixtla/neuralforecast (N-HITS)** as the fully open-source self-host path if vendor API cost or data-residency concerns escalate.

---

*Scan generated 2026-07-27. Platform metrics reflect DB-disconnected state; ecosystem findings are independent of platform status.*
