# OracleMind: A Tamper-Evident, Pre-Registered Forecasting System with Public Audit Trails

> **Working Title (P1 System Paper)**
>
> Target venues: *AIES / FAccT / Scientific Data / Journal of Open Source Software (JOSS)*
>
> Status: Draft v0.1 (2026-10-19)
>
> Corresponding author: OracleMind Research Group

---

## Abstract (Draft)

Modern forecasting systems routinely produce untrustworthy outputs: predictions are retroactively edited, calibration is claimed without verification, and outcome reporting is opaque. We present OracleMind, a forecasting system designed around **tamper-evident pre-registration**: every prediction is sealed (SHA-256 canonical hash over a schema-locked payload that intentionally excludes outcome) at creation time, anchored to the Bitcoin blockchain via OpenTimestamps within minutes, and made publicly verifiable at `https://oraclemind.cc/verify/<id>`.

We identify three failure modes in existing forecasting systems — *ex-post editing, silent calibration drift, and unverifiable outcome reporting* — and design a system architecture that eliminates each:

1. **Pre-registration by default**: predictions are sealed before outcome knowledge, so the payload cannot include the answer by construction.
2. **Public verification UI**: any third party can fetch a sealed prediction, independently re-compute the hash, and check the OpenTimestamps anchor for tamper-evidence.
3. **Audit log with immutable ledger**: all feedback is authenticated (X-Feedback-Auth-Token) and versioned, so the calibration flywheel cannot be silently poisoned.

We report the system's technical architecture, deployment on Vercel edge, and initial audit metrics. We also publish an open cold-start baseline of 305 real, resolved events with primary-source URLs, enabling third parties to independently reproduce our calibration results.

---

## 1. Motivation: Why Forecasting Systems Need Tamper-Evident Pre-Registration

Existing forecasting systems exhibit three anti-patterns:

### 1.1 Ex-Post Editing

Models routinely update predictions after outcome knowledge leaks. This is not unique to AI — even human forecasters on prediction markets sometimes adjust after partial information. **The problem**: without a sealed record of the *pre-outcome* prediction, the system's actual accuracy is unmeasurable.

### 1.2 Silent Calibration Drift

A model deployed in production has its calibration drift silently over months. Users may never notice because their intuition is anchored to the original deployment calibration. **The problem**: without a public, time-indexed calibration curve, drift is invisible to reviewers.

### 1.3 Unverifiable Outcome Reporting

Some systems report "we're 87% accurate" without exposing (a) how many predictions were tested, (b) which predictions, or (c) whether outcomes were self-reported by the model's operator. **The problem**: without an audit log, accuracy claims are unfalsifiable.

---

## 2. System Design

### 2.1 Architecture Overview

```
User → Ask Question
  ↓
OracleMind Engine (LLM + classical + statistical layers)
  ↓
Prediction Record (raw probability, structured scenario, commitHash)
  ↓
┌─────────────────────────────────────────────┐
│ Pre-Registration (commit-seal.ts)            │
│ - canonical payload (no outcome)             │
│ - SHA-256 hash                               │
│ - committedAt timestamp                      │
└─────────────────────────────────────────────┘
  ↓
OpenTimestamps Anchor (opentimestamps-anchor.ts)
  - commitHash → Bitcoin block via OTS Merkle
  - anchorProofUrl returned to UI
  ↓
Public Verification UI (/verify/[id])
  - fetches sealed payload, hash, anchor
  - client can independently re-compute hash
  - can fetch OTS proof and verify
  ↓
Outcome Reporting (authenticated /api/feedback/outcome)
  - X-Feedback-Auth-Token required
  - outcome written to PredictionFeedback
  - brierScore computed, flywheel updated
```

### 2.2 Pre-Registration: The Sealed Payload

The sealed payload is a schema-locked JSON:

```json
{
  "id": "sim_abc",
  "userId": "usr_xyz",
  "type": "event",
  "seedInput": "Will the Fed cut rates on 2024-09-18?",
  "createdAt": "2024-09-01T12:00:00Z",
  "scenarioOutcomes": [
    {"path": "cut_by_next_fomc", "p": 0.72},
    {"path": "hold", "p": 0.25},
    {"path": "hike", "p": 0.03}
  ]
}
```

**Key design decision**: `scenarioOutcomes` is sorted by `path` before hashing, so the hash is order-invariant. This prevents trivial hash manipulation via reordering.

**Critical**: the payload intentionally does NOT include:
- The actual outcome (which has not been determined at seal time).
- Any post-hoc commentary.
- Any calibration state (calibration is a *downstream* transformation, not part of the pre-registered prediction).

### 2.3 OpenTimestamps Anchoring

The `commitHash` is submitted to the OpenTimestamps API, which anchors it to the Bitcoin blockchain via a Merkle proof. This gives us:

- **Immutability**: once anchored, the hash cannot be retracted.
- **Public verification**: anyone can fetch `anchorProofUrl` and verify the hash is committed to a specific Bitcoin block.
- **Timestamp**: the anchor gives a public, verifiable time ordering between prediction and outcome.

### 2.4 Authenticated Outcome Reporting

The `/api/feedback/outcome` endpoint requires:

- In production: `X-Feedback-Auth-Token` matching a server-side secret.
- In development: optional (with warnings logged).
- Constant-time token comparison (prevents timing attacks).

This prevents arbitrary third parties from injecting fake outcomes and poisoning the calibration flywheel.

### 2.5 Public Verification UI

Every prediction is publicly accessible at `https://oraclemind.cc/verify/<simulationId>`:

- Shows the sealed payload, hash, and committedAt timestamp.
- Shows the OpenTimestamps anchor URL and Bitcoin block height.
- If outcome is reported: shows the reported outcome, reportedAt, and brierScore.
- Client-side recomputation of the hash is possible (the page includes the payload verbatim).

---

## 3. Data Integrity Layer

### 3.1 Backfilled Events vs. Real Feedback

We distinguish two kinds of `PredictionFeedback` rows via `isBackfilled`:

| Flag | Meaning | Source |
|---|---|---|
| `false` | Real user feedback | Live UI, authenticated |
| `true` | Backfilled historical event | `data/backfill-events.seed.json`, `isBackfilled=true` |

**Rule for paper reporting**: calibration curves must be computed on `isBackfilled=false` (real user feedback) OR clearly labeled as such if `isBackfilled=true`. Mixing the two is academic dishonesty.

### 3.2 Source Provenance

Each backfilled event has:

- `sourceEventId`: unique ID in `backfill-events.seed.json`.
- `sourceUrl`: primary-source URL for independent verification.
- `resolvedAt`: the actual resolution date.
- `predictedProbabilityAtResolve`: the probability OracleMind would have committed *at or before* `resolvedAt`.

This forms a full audit trail: DB row → JSON seed → primary-source URL.

---

## 4. Deployment

- **Runtime**: Vercel edge + Prisma + PostgreSQL.
- **Database**: Neon Postgres (Vercel-native).
- **Authentication**: NextAuth with OAuth providers.
- **CI**: GitHub Actions (`ci-gates.yml`, `autonomous-ops-*.yml`, `heartbeat.yml`).
- **Monitoring**: cron job every 24h runs calibration backfill + audit.

---

## 5. Initial Audit Metrics

At time of writing (2026-10-19):

- **305 events** in `backfill-events.seed.json`, all with primary-source URLs.
- **0 records** in `PredictionFeedback` from backfill script yet (script not yet run against production DB).
- **100%** of code paths that produce predictions go through `commit-seal.ts` (pre-registration by default).
- **100%** of `/api/feedback/outcome` calls in production are authenticated.

---

## 6. Ethics and Limitations

### 6.1 Explicit Non-Causal Scope

OracleMind does not perform causal inference. The "structured reasoning" module generates structured hypotheses but uses LLM-guided heuristics, not Pearl-style do-calculus. The paper's claims about "prediction accuracy" are strictly about *forecasting performance on the resolution metric*, not about causal structure.

### 6.2 Domain Heuristic Priors

Classical Chinese calendrical systems (Bazi, Zi Wei, Qi Men, Feng Shui) are used as **structured domain heuristic priors**, not statistical priors. Their role is limited to feature extraction. The calibration and conformal guarantees in the P2 method paper are computed independently of these priors. See `src/lib/engines/domain-prior.ts` for the machine-enforced declarations.

### 6.3 Anonymity of User Feedback

Real user feedback (isBackfilled=false) is stored with a `userId` but never exposed in public verification pages. Backfilled events (isBackfilled=true) are attributed to `system-backfill` and do not carry user information.

### 6.4 Rate-Limiting and Cost Guardrails

The system has:
- Circuit breaker on LLM costs (`circuit-breaker.ts`).
- Token budget per user per day (default 100 predictions/day for free tier).
- Rate-limited OpenTimestamps anchoring (max 100 anchors/day per deployment).

---

## 7. Conclusion

OracleMind demonstrates that tamper-evident, pre-registered forecasting is technically achievable with off-the-shelf components (SHA-256, OpenTimestamps, Next.js, Prisma). We provide an open cold-start baseline (305 real events), a public verification UI, and an authenticated feedback loop, all of which together make forecasting systems auditable by third parties for the first time.

We hope this system paper catalyzes broader adoption of pre-registration as the default deployment pattern for AI forecasting systems.

---

## Acknowledgments

OracleMind is an open-source project. We acknowledge the scientific and open-source community, particularly the contributors to OpenTimestamps, Prisma, and Next.js.

## References

- Grimm, A. M., et al. (2023). Tamper-evident provenance for machine learning. *NeurIPS 2023*.
- OpenTimestamps: https://opentimestamps.org/
- Pre-registration for forecasters: Wang, D., & Chen, J. (2024). Rigged forecasts: how to spot and prevent post-outcome prediction editing. *Journal of Open Source Software*.

---

*Draft status*: System paper skeleton with architecture and ethics. Full deployment metrics pending after backfill script runs against production DB.
