# ChatGPT Project Handoff

## CURRENT AUTHORITATIVE PHASE
Score v2 Monitoring & Stability

### Monitoring Refresh 2026-09-13

Independent monitoring cycle: 1 / 3.

- Clean real-key refresh: v2 architecture PASS — 24 visible, 12 scored, denominator 24; JOLTS Hires scored, Quits context-only, Sahm Cycle context/confirmation-only; Current Stress has six signals including Sahm Confirmation.
- Actual state: `9 / 24`, `38 / 100`, `Slowdown`. No scored indicator changed state versus the prior production snapshot. Pipeline warnings: none.
- History: `same-version replace` for the existing `2026-09-13` row; one row per date, no duplicate; legacy `2026-09-12` v1 row unchanged; no cross-version overwrite or warning.
- Root/frontend current and history JSON synchronized; frontend production build PASS. Expected generated changes are current snapshot refreshes only.

### Supplemental Same-Day Verification 2026-09-13

This supplemental run confirms same-version replacement/idempotence but does not increment the independent three-cycle monitoring counter. Architecture: PASS — v2, 24 visible, 12 scored, denominator 24. State: `9 / 24` → `38 / 100`, `Slowdown`; changed scored signals: none. Current Stress: six signals including Sahm Confirmation. History: `same-version replace`, one row per date, legacy v1 unchanged, no cross-version overwrite or warning. Root/frontend sync PASS; build PASS; pipeline warnings none. Authoritative monitoring progress remains `1 / 3` independent cycles.

The published Cycle Score v2 remains the production baseline. SEC insider research is DEFERRED / historical and must not resume.

## Dashboard Presentation & UX Refresh — local visual review

- Frontend files changed: `frontend/src/App.tsx`, `frontend/src/components/IndicatorCard.tsx`, `frontend/src/styles/presentation-refresh.css`.
- Hero: institutional macro header, integrated Cycle score plate with live score/regime/raw points/scored count, larger gauge treatment, adjacent Current Stress companion, and subtle CSS civic/grid motif.
- Evidence chain: explanatory-only strip from Labor deterioration → Consumer pressure → Economic slowdown → Earnings / cash-flow pressure → Asset-price vulnerability; no score or data field added.
- Card roles: scored indicators show `Cycle score · Healthy/Warning/Recessionary`; context cards show `Context`; Sahm shows `Confirmation · Context`.
- Responsive behavior: three-column desktop card grid, two-column tablet fallback, stacked mobile hero/evidence chain/single-column cards with readable role labels and no horizontal overflow.
- Validation: frontend production build PASS; 24 indicator rendering and v2 role language preserved; no stale 14/28 copy found. Generated JSON, scoring/data-source code, history, workflow, infrastructure, `.env`, and SEC state were untouched.
- Status: **NOT COMMITTED / NOT PUSHED**. Active monitoring baseline remains `Score v2 Monitoring & Stability`; active workstream is UI-only.

## Dashboard Presentation & UX Refresh — online review

- Commit: `a69ffff4d7d33475223e5142849faf5c0f07fa36`; message `Refresh-dashboard-presentation`.
- Push: PASS to `origin/main`.
- Frontend build: PASS.
- Published files: `frontend/src/App.tsx`, `frontend/src/components/IndicatorCard.tsx`, `frontend/src/styles/presentation-refresh.css`, `CHATGPT_HANDOFF.md`.
- Production logic changed: NO. Scoring, data, history, Current Stress, workflows, infrastructure, `.env`, and SEC state are untouched.
- Cloudflare: deployment expected automatically from `main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — card readability iteration

- Files: `frontend/src/components/IndicatorCard.tsx`, `frontend/src/styles/presentation-refresh.css`, `CHATGPT_HANDOFF.md`.
- Card anatomy: consistent icon/role row, title, labeled dominant metric, separated supporting-metric grid, concise interpretation, and aligned source/date footer. Technical series identifiers no longer lead the primary metric.
- Badges: scored cards use `Cycle score · Healthy/Warning/Recessionary`; context cards use `Context`; Sahm uses `Confirmation · Context`. Labor subtotal is labeled `Risk points`.
- Responsive behavior: two-column support grid on desktop, stacked metrics and one card per row on mobile; footer and badges wrap without horizontal overflow.
- Build: PASS. 24 indicators/data values preserved; Hires remains Cycle-scored, Quits Context, Sahm Confirmation · Context. Production logic, JSON, history, workflows, infrastructure, `.env`, and SEC state changed: NO.
- Commit: `c98ca7b4c1ddf9c89bb7df6934bab76edb583c93`; message `Improve indicator card readability`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — metric layout fix

- Root cause: the previous card used only a generic display-string split and CSS styling; the frontend needed an explicit presentation adapter to turn existing `trend_metrics` and known `display_value` segments into real label/value cells.
- Files changed: `frontend/src/components/IndicatorCard.tsx`, `frontend/src/styles/presentation-refresh.css`, `CHATGPT_HANDOFF.md`.
- Implementation: frontend-only per-indicator primary/support adapter; no generated JSON or Python semantics changed. Labor support metrics now render as separate cells, technical series codes are removed from the dominant metric, category labels are hidden visually but retained in ARIA text, and the subtotal is displayed as `Risk points`.
- Validation: build PASS; 24 indicators preserved; Hires `Cycle score`, Quits `Context`, Sahm `Confirmation · Context`; no old numeric badges, visible repeated `LABOR`, or concatenated Labor support-stat blob remains in the card renderer. Production logic/data/history/workflows/infrastructure/.env/SEC state changed: NO.
- Commit: `668a1f764504e278ddbf20730eae3cf5c35513ba`; message `Fix indicator metric layout`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — compact dashboard top summary

- Files: `frontend/src/App.tsx`, `frontend/src/styles/presentation-refresh.css`, `CHATGPT_HANDOFF.md`.
- Change: merged the title hero and Overall Picture into one compact summary block with one canonical Cycle score/regime/raw-points/scored-count presentation. The gauge is reduced to a compact footprint; Current Stress is a separate compact companion showing `Calm / No Break` and `0 / 6 confirmations`.
- Layout: Healthy/Warning/Recessionary counts, domain pills, interpretation, and the explanatory evidence chain now live inside the merged block. The standalone duplicate Current Stress panel is visually suppressed. Desktop targets a compact 420–520px summary; mobile stacks title, score, gauge, stress, counts, pills, and evidence without horizontal overflow.
- Validation: frontend build PASS; 24 indicators and live score fields preserved (`9 / 24`, `38 / 100`, `Slowdown`). No generated JSON, scoring, thresholds, roles, Current Stress logic, history, workflows, infrastructure, `.env`, or SEC state changed.
- Commit: `90e0562423eda7d41637ad85e7fcf44d96da6844`; message `Compact dashboard top summary`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — simple dashboard header

- Files: `frontend/src/App.tsx`, `frontend/src/components/RecessionGauge.tsx`, `frontend/src/styles/presentation-refresh.css`, `CHATGPT_HANDOFF.md`.
- Change: replaced the compressed multi-column hero with a clean dashboard header. The title uses dashboard-scale typography, the dominant `38 / 100` score has compact metadata, and the large semicircle is replaced by a horizontal Healthy → Slowdown → Recession track driven by the existing normalized score.
- Current Stress is one inline companion row; counts and domain pills remain compact and horizontal on desktop, wrapping cleanly on mobile. Decorative grid pressure and duplicate top-state presentation were removed.
- Validation: frontend build PASS; 24 indicators and existing score fields preserved (`9 / 24`, `38 / 100`, `Slowdown`). No generated JSON, scoring, thresholds, roles, Current Stress logic, history, workflows, infrastructure, `.env`, or SEC state changed.
- Commit: `a9536fa4ca5d72a34e71a8cbfe2ed12c4ffa6d86`; message `Simplify dashboard header`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — header layout fix

- Files: `frontend/src/App.tsx`, `frontend/src/components/RecessionGauge.tsx`, `frontend/src/styles/presentation-refresh.css`, `frontend/src/styles/header-layout.css`, `CHATGPT_HANDOFF.md`.
- Change: added a robust two-column desktop header with normal-flow metadata in the left column and Cycle score/scale/stress metadata in the right column. The risk scale is width-contained with percentage marker positioning and a three-column label layout; the decorative arc is removed.
- Responsive behavior: mobile switches to one normal-flow column with no absolute essential content, clipping, or right-edge overflow. Header content is targeted to a compact 250–320px desktop footprint.
- Validation: frontend build PASS; 24 indicators and existing score fields preserved (`9 / 24`, `38 / 100`, `Slowdown`). No generated JSON, scoring, thresholds, roles, Current Stress logic, history, workflows, infrastructure, `.env`, or SEC state changed.
- Commit: `bba0bdebcf15444a27c448cf7fc15009314e5b84`; message `Fix dashboard header layout`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — header CSS root-cause fix

- Root cause: the prior header reused legacy `.summary-*` / `.merged-*` selectors from `dashboard.css`, `presentation-refresh.css`, and `header-layout.css` in multiple import layers. Conflicting grid/flex rules, the old absolute `.updated` rule, and legacy media queries acted on the compressed DOM; the evidence chain remained nested in that same block and the later full Current Stress markup remained active.
- DOM fix: `App.tsx` now has one `.dashboard-header` with exactly two primary children: `.dashboard-header__left` and `.dashboard-header__right`. Evidence chain is a sibling below the header; the duplicate lower Current Stress panel is neutralized visually.
- Files changed: `frontend/src/App.tsx`, `frontend/src/styles/dashboard-header-fix.css`, `CHATGPT_HANDOFF.md`.
- CSS fix: uniquely scoped normal-flow `.dashboard-header*` selectors replace legacy header behavior; score, scale, stress, counts, and domains are contained in the right column. Decorative/header legacy rules are no longer active because the old classes are absent from the header DOM.
- Width validation: 1440px and 1024px use a real two-column grid with normal subtitle/metadata flow and contained score/scale/stress; 390px switches to one column with wrapping domain pills and no horizontal overflow. Build PASS; 24 indicators and score data preserved. Production logic/data/history/workflows/infrastructure/.env/SEC state changed: NO.
- Commit: `a2be45f9a3c45b60f4192cf29d34fd6652903b2a`; message `Fix header CSS cascade`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — infographic hero direction reset

- Files: `frontend/src/App.tsx`, `frontend/src/components/MacroHero.tsx`, `frontend/src/styles/macro-hero.css`, `frontend/src/styles/presentation-refresh.css`, `CHATGPT_HANDOFF.md`; removed obsolete `frontend/src/styles/header-layout.css` and `frontend/src/styles/dashboard-header-fix.css`.
- Reset: replaced the minimalist header with one isolated poster-style `MacroHero`: subtle CSS/SVG civic scene, centered semicircle gauge, integrated white score plate, live score/regime/raw points/scored count, compact status counts, and separate Current Stress companion. Evidence chain remains below the hero.
- Cleanup: stopped importing all superseded header styles and reduced `presentation-refresh.css` to stable indicator-card presentation only; no layered header selectors remain active.
- Responsive validation: desktop ~1440px and tablet ~1024px use a controlled 480–620px hero; mobile ~390px stacks title, gauge, score plate, stress, counts, and evidence without overflow. Build PASS; 24 indicators and Hires/Quits/Sahm roles preserved.
- Production logic/data/history/workflows/infrastructure/.env/SEC state changed: NO.
- Commit: `5adbecd9dcd9ee34e1c1c559956384d00ed7df06`; message `Restore infographic hero direction`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — compact infographic hero

- Files: `frontend/src/styles/macro-hero.css`, `CHATGPT_HANDOFF.md`.
- Hero sizing: retained the approved poster/civic direction while reducing the desktop hero toward 360–430px, gauge to approximately 390px wide × 195px arc, score plate padding/type, Current Stress footprint, skyline height, and top/bottom spacing.
- Evidence chain: compact horizontal strip with reduced margins; mobile continues to stack cleanly. Indicator-card implementation and data structure were untouched.
- Validation: frontend build PASS; 24 indicators and Hires/Quits/Sahm roles preserved; desktop/tablet/mobile responsive rules reviewed for no clipping or overflow. Generated JSON, scoring, thresholds, Current Stress logic, history, workflows, infrastructure, `.env`, and SEC state changed: NO.
- Commit: `f0d885f8007029b728ca4c72820b6e405ad9a2c5`; message `Compact infographic hero`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

## Dashboard Presentation & UX Refresh — gauge labels and evidence chain

- Files: `frontend/src/styles/macro-hero.css`, `CHATGPT_HANDOFF.md`.
- Gauge labels: added a dedicated gauge-width three-column row with left/center/right alignment for Healthy, Slowdown, and Recession; labels remain inside the hero and clear of the score plate/stress companion.
- Evidence chain: added a compact desktop/tablet horizontal flex sequence with visible arrows; controlled wrapping is used at narrower widths and mobile stacking remains readable.
- Validation: frontend build PASS; 24 indicators preserved; no generated JSON, scoring, data/history, indicator-card, Current Stress, workflow, infrastructure, `.env`, or SEC changes. Responsive rules reviewed at 1440px, 1024px, and 390px for clipping/overflow.
- Commit: `d4780480b6379ef94bc8104ebc603911f76f3fba`; message `Fix gauge labels and evidence chain layout`; push: PASS to `origin/main`.
- Review URL: `https://recession-dashboard-45c.pages.dev`.

Score v2 Monitoring & Stability

The published v2 implementation is stable. All other `CURRENT AUTHORITATIVE PHASE` headings below are historical/superseded audit records. SEC insider research remains DEFERRED / historical and must not resume.

## CURRENT AUTHORITATIVE SAME-DATE HISTORY PUBLICATION STATUS

The Same-Date History Consistency Fix is published in this handoff sequence. Missing `score_model_version` means v1; new dates append; same-date same-version snapshots atomically replace the full daily row; same-date cross-version conflicts preserve the existing row, add no duplicate, and emit a warning.

- Publication commit: `14df5b3ea93aeb43705232f3e65938dfdc3c4b1e`; message `Fix same-day history consistency`; push status PASS to `origin/main`.
- Tests A-E: PASS — new-date append; identical same-version rerun without duplication; changed same-version payload replaced atomically with stable row count; legacy v1 cross-version conflict preserved byte-for-byte with warning; next-date append preserved older rows and chronological order.
- Live pipeline/build: PASS — v2, 24 visible, 12 scored, `9 / 24`, `38 / 100`, `Slowdown`; frontend `npm run build` passed.
- Roles and Current Stress: PASS — Hires scored; Quits context-only; Sahm Cycle context/confirmation-only; six Current Stress signals including Sahm Confirmation.
- History/sync: PASS — root/frontend current and history JSON synchronized; legacy `2026-09-12` v1 row unchanged. Current JSON changes are legitimate `generated_at` refreshes.
- Safety: PASS — `.env` and SEC transient state/cache ignored and unstaged; no scoring, threshold, source, workflow, infrastructure, or SEC changes.
- Published files: `scripts/build_dashboard_data.py`, `data/current.json`, `frontend/src/data/current.json`, `CHATGPT_HANDOFF.md`. `README.md` required no change.
- Verdict: **STABLE**. Next phase remains **Score v2 Monitoring & Stability**.

Cycle Score v2 — published

Commit `eaf0a46844e7a120be46332d4ce7d0c798430d72` pushed to `origin/main`. Next phase: **Score v2 Monitoring & Stability**. SEC insider research remains DEFERRED / historical and must not resume.

Cycle Score v2 — local implementation review

Implementation is local only: NOT COMMITTED / NOT PUSHED. SEC insider research remains DEFERRED / historical and must not resume.

Cycle Score v2 Design Decision — research / design only

No production implementation is approved in this phase. SEC insider research remains DEFERRED / historical and must not resume.

Recession Score Architecture Audit — research only

Corporate, Consumer, Broad Cycle and Labor studies are completed historical phases. SEC insider research remains DEFERRED / historical and must not resume. Production scoring remains unchanged.

Corporate Profit & Credit Transmission Study — research only

Consumer, Broad Cycle, Labor, Market Fragility and SEC work remain completed or deferred historical phases. Production scoring remains unchanged.

Consumer Pressure & Household Resilience Study — research only

Labor Market v2 and Broad Cycle research are completed historical phases. Production scoring remains unchanged. SEC insider research remains DEFERRED / historical and must not resume.

## HISTORICAL / SUPERSEDED PHASE
Labor Market v2 — core recession/cycle refinement

SEC insider research is DEFERRED / historical; the preserved full-backfill checkpoint must not resume.

The older Market Fragility phase/status section below is historical and superseded. The authoritative active phase is Labor Market v2 above. The current next task is the research-only Labor Scoring Robustness Study (PROJECT_INSTRUCTIONS sections 313–320).

## Project
US Recession Risk Dashboard

## HISTORICAL / SUPERSEDED PHASE
Market Fragility / Stress expansion — sections 95–104

## Status
Implemented and verified locally. STOPPED before commit/push per the higher-risk data-source policy.

## What Was Done
- Enriched the existing Yield Curve indicator with `DGS1`, `DGS2`, `DGS5`, `DGS10`, `DGS30`, `T10Y2Y`, and `T10Y3M`.
- Added sustained inversion/un-inversion state and 20-trading-day curve-shape classification.
- Added four context-only indicators: VIX, Financial Stress Index, Credit Conditions, and Margin Debt / GDP.
- Added an official FINRA Margin Statistics HTML-table parser with fallback behavior.
- Added the Market Fragility / Stress frontend section and curve-regime display inside Bond Market / Rates.
- Kept ICE BofA series research-only; no BAML values are fetched or published.
- Kept the Cycle / Recession score and denominator unchanged.

## Files Created or Changed
- `scripts/market_fragility.py` — yield-curve regime and steepening derivation.
- `scripts/fetch_finra.py` — official FINRA margin-table fetch/parser.
- `scripts/fetch_fred.py` — sanitized request errors and existing FRED helper retained.
- `scripts/build_dashboard_data.py` — new FRED overlays, FINRA/GDP ratio, curve metadata, and context output.
- `data/sample_raw.json` — four context-only fallback records.
- `data/current.json`, `data/history.json` — generated live output.
- `frontend/src/data/current.json`, `frontend/src/data/history.json` — synchronized output.
- `frontend/src/types/dashboard.ts` — curve-regime and source-reference fields.
- `frontend/src/App.tsx` — Market Fragility / Stress section and Bond Market curve regime.
- `README.md` — source/licensing documentation.
- `CHATGPT_HANDOFF.md` — this handoff.

## Current Data / Score State
- Visible indicators: 22
- Scored indicators: 14
- Context-only indicators: 8
- Total score: 10 / 28
- Normalized risk score: 36 / 100
- Regime: Slowdown
- Data status: `ok`
- Warnings: none

## Yield Curve Live Values and Formula Validation

| Field | Value | Validation |
|---|---:|---|
| `DGS1` | 4.28% | PASS — latest daily Treasury observation |
| `DGS2` | 4.56% | PASS — latest daily Treasury observation |
| `DGS5` | 4.75% | PASS — latest daily Treasury observation |
| `DGS10` | 4.95% | PASS — latest daily Treasury observation |
| `DGS30` | 5.37% | PASS — latest daily Treasury observation |
| `T10Y2Y` | +39.0 bp | PASS — FRED spread used directly |
| `T10Y3M` | +89.0 bp | PASS — FRED spread used directly |
| Deepest 2s10s inversion | -241.0 bp | PASS — minimum historical spread |
| Deepest 3m10y inversion | -189.0 bp | PASS — minimum historical spread |
| Inversion start | 2022-07-06 | PASS — 10+ consecutive negative observations |
| Un-inversion date | 2024-09-06 | PASS — first date of 10+ consecutive non-negative observations |
| Months since un-inversion | 24 | PASS — calendar-month calculation |
| Curve phase | `positive_no_recent_inversion` | PASS — un-inversion is older than provisional 18-month window |
| 20-day 2Y change | +36.0 bp | PASS |
| 20-day 10Y change | +27.0 bp | PASS |
| 20-day spread change | -9.0 bp | PASS — below ±10 bp threshold |
| Steepening type | `neutral_or_mixed` | PASS — documented classification |

## Market Fragility / Stress Live Values

| Indicator / source | Latest date | Dashboard value | Recent fields | Status |
|---|---:|---:|---|---|
| VIX / FRED `VIXCLS` (underlying CBOE) | 2026-09-10 | 17.84 | 20D avg 16.33; 20D change +2.63 | PASS |
| Financial Stress Index / FRED `STLFSI4` | 2026-09-04 | -0.7884 | 4W avg -0.82; 12W change +0.16 | PASS |
| Credit Conditions / FRED `NFCICREDIT` | 2026-09-04 | -0.06 | 4W avg -0.06; 12W change -0.03 | PASS |
| Margin Debt / GDP / FINRA + FRED `GDP` | FINRA Jul-26; GDP 2026-04-01 | 4.3626% | $1,417,225M margin debt; GDP billions used in ratio | PASS |

Margin formula validated: `(1,417,225 / 1,000 / GDP_billions) * 100 = 4.3626%`. The FINRA parser uses the official webpage only and reports the reference month. No Yahoo Finance, TradingView, or ICE BofA values are used.

## Commands to Run Locally
```powershell
# From project root; reads FRED_API_KEY from local .env
python scripts/build_dashboard_data.py

# From frontend
cd frontend
npm run build
```

## Verification Performed
- Real-key Python pipeline: PASS — 19 live source-backed context/original records, 3 manual indicators.
- Generated JSON validation: PASS — 22 indicators, 14 scored, 8 context-only.
- Root score consistency: PASS — 10/28 and risk 36/100 unchanged from before this expansion.
- Context exclusion: PASS — all four new indicators have `scored: false`, `score: null`, `risk_score: null`.
- Curve history/state validation: PASS.
- FINRA fetch/parser: PASS — latest row parsed from official page.
- Python compilation: PASS.
- `npm run build`: PASS.
- Git commit/push: NOT PERFORMED by instruction.

## Issues / Warnings
- No live pipeline warnings remain.
- FINRA has no official data feed; the parser retains prior/sample data and emits a warning if the official page changes or becomes unavailable.
- No numeric composite Fragility score was added.

## Important Decisions
- New market-fragility indicators are context-only and do not affect Cycle / Recession score totals.
- Yield Curve Regime enriches the existing scored Yield Curve indicator rather than creating a duplicate.
- BAMLH0A0HYM2 and BAMLH0A3HYC remain documented as research-only, with no public values.

## Final Publication Verification
- Real-key Python pipeline: PASS — 19 live FRED-backed records, FINRA live parse, and 3 manual indicators.
- Generated JSON validation: PASS — root/frontend data files match; 22 indicators, 14 scored, 8 context-only.
- Root score consistency: PASS — Cycle / Recession score `10 / 28`; normalized risk `36 / 100`; regime `Slowdown`.
- Context exclusion: PASS — `vix`, `financial-stress`, `credit-conditions`, and `margin-debt-gdp` each have `scored: false`, `score: null`, and `risk_score: null`.
- `npm run build`: PASS.
- `.env` staging check: PASS — ignored and not staged.
- Reviewed implementation commit: `0377162` — `Add market fragility stress indicators`.
- Final verification commit: `1f4ec3c` — `Verify market fragility and yield curve indicators`.
- Push status: PASS — pushed to `origin/main`.

## Published Files
The reviewed implementation is published on `origin/main` in commit `0377162`:
- `scripts/market_fragility.py`
- `scripts/fetch_finra.py`
- `scripts/fetch_fred.py`
- `scripts/build_dashboard_data.py`
- `data/sample_raw.json`
- `data/current.json`, `data/history.json`
- `frontend/src/data/current.json`, `frontend/src/data/history.json`
- `frontend/src/types/dashboard.ts`
- `frontend/src/App.tsx`
- `README.md`
- `CHATGPT_HANDOFF.md`

The unrelated local change to `PROJECT_INSTRUCTIONS.md` was not staged or published. No Valuation / Bubble Risk implementation was started.

## Valuation / Bubble Risk Context Expansion — Review Status

Implemented the approved context-only valuation expansion. Publication was requested and completed after review.

| Indicator | Source / series | Latest value | Reference date | Percentile / status | Result |
|---|---|---:|---|---|---|
| Public Equity Market / GDP | Federal Reserve Z.1 `BOGZ1FL883164115Q` + FRED `GDP` | 288.1% | 2026-04-01 for both aligned quarterly observations | 100.0th percentile — Historically Extreme | PASS |
| Shiller CAPE | Robert Shiller / Yale official workbook, current Shiller Data download | 40.5758 (displayed 40.6) | September 2026 (`2026-09-01`) | 98.9th percentile — Historically Extreme; long-run median 16.6 | PASS — live |
| Margin Debt / GDP | Existing FINRA + FRED indicator, referenced without duplication | 4.36% of GDP | FINRA Jul-26; GDP 2026-04-01 | Existing context value | PASS |

Methodology validation: `public_equity_market_millions / 1000 / nominal_gdp_billions * 100`; the live Z.1/GDP result is 288.1473%, displayed as 288.1%. Historical percentiles use the available aligned history for the Z.1 ratio and the parsed/retained CAPE history. Percentile labels are descriptive, not crash-timing signals. Both new indicators have `scored: false`, `score: null`, and `risk_score: null`; the global score remains `10 / 28` and normalized risk remains `36 / 100`.

Pipeline: PASS — official Yale/Shiller CAPE source is live, `source_status: live`, and no CAPE fallback warning remains. Frontend build: PASS (`npm run build`). Parser/dependency changes: added the current official Shiller Data workbook URL, parsed Yale `YYYY.MM` dates correctly, validated current date/value bounds, preserved legacy URL fallback, and ensured `xlrd>=2.0.1` is present and installed locally. This CAPE-only remediation is intentionally uncommitted and unpushed for review. No S&P concentration scraping, S&P Price/Sales automation, Bubble composite, Yahoo Finance, or TradingView was added.
- Cycle / Recession score: PASS — `10 / 28`; normalized risk `36 / 100` unchanged.
- CAPE source status: PASS — live, not fallback; pipeline warnings: none.
- Commit: `14d9ffd` — `Add valuation and Shiller CAPE context indicators`.
- Push status: PASS — pushed to `origin/main` after this handoff update.

## Current Stress / Break Confirmation v1 — Review Status

Implemented locally and intentionally not committed or pushed.

| Signal | Current value / derived field | State | Result |
|---|---|---|---|
| Volatility Release / FRED `VIXCLS` | 17.84; 20D average 15.37; 20D change +3.59; 2026-09-10 | Watch | PASS |
| Financial Stress / FRED `STLFSI4` | -0.7884; 4W average -0.8194; 12W change +0.1624; 2026-09-04 | Calm | PASS |
| Credit Conditions / FRED `NFCICREDIT` | -0.0600; 4W average -0.0582; 12W change -0.0290; 2026-09-04 | Calm | PASS |
| Claims Acceleration / `ICSA` | 4W average 206,000; 13-week change -6.0%; 2026-09-05 | Calm | PASS |
| Sahm Confirmation / `SAHMREALTIME` + `UNRATE` | Sahm -0.07; unemployment 4.1%; 2026-08-01 | Calm | PASS |
| Rapid Bull Steepening / existing curve regime | 2Y 20D +36.0 bp; 2s10s change -9.0 bp | Calm / false | PASS |

Current Stress aggregate: `Calm / No Break`, `0 of 6` active confirmations, no market/financial confirmation active. Thresholds are explicitly provisional. Historical sanity checks passed for calm synthetic inputs, claims acceleration state boundaries, Sahm thresholds, and the rapid bull-steepening requirement (`2Y <= -25 bp` plus spread widening `>= +15 bp`).

Score preservation: PASS — Cycle / Recession remains `10 / 28`, normalized risk `36 / 100`; the indicator count remains 24 and no new scored indicator or denominator was added. Pipeline and generated JSON validation: PASS. Frontend build: PASS. Changed files: `scripts/current_stress.py`, `scripts/build_dashboard_data.py`, `frontend/src/types/dashboard.ts`, `frontend/src/App.tsx`, `frontend/src/styles/current-stress.css`, `data/current.json`, `frontend/src/data/current.json`, `README.md`, and this handoff. No Current Stress commit/push was performed.

## VIX Shared Derived-Metric Reconciliation — Review Status

Implemented locally and intentionally not committed or pushed. Root cause: Market Fragility used 20 newest observations and compared the latest with the 20th item, producing a 19-observation change; Current Stress independently used a different slice and calculation. Both now consume `scripts/derived_metrics.py`.

Canonical policy: sort valid observations ascending, discard missing/non-numeric values identically, use exactly 20 valid observations for the moving average, and define `20D change` as latest minus the value 20 valid observations earlier, requiring 21 valid observations.

| VIX field | Canonical result | Status |
|---|---:|---|
| Current value | 17.84 | PASS |
| Observation date | 2026-09-10 | PASS |
| 20D average | 15.3695 (displayed 15.37) | PASS |
| 20-observation change | +3.21 | PASS |
| Market Fragility display | `17.84 close | 20D avg 15.37 | 20D change +3.21` | PASS |
| Current Stress display | `17.84 | 20D avg 15.37 | 20D change +3.21` | PASS |

Current Stress after reconciliation: `Calm / No Break`, `0 of 6` active confirmations; Volatility Release remains `Watch`, all other signals remain Calm. Score preservation: PASS — Cycle / Recession remains `10 / 28`, normalized risk `36 / 100`, with 24 indicators and no denominator change. Pipeline/JSON validation: PASS with no warnings. Historical canonical-metric sanity checks: PASS. Frontend build: PASS. Changed files: `scripts/derived_metrics.py`, `scripts/build_dashboard_data.py`, `scripts/current_stress.py`, `data/current.json`, `frontend/src/data/current.json`, and this handoff. No commit/push performed.

## Current Stress Publication

The reviewed Current Stress / Break Confirmation v1 and canonical VIX reconciliation were published after final validation.

- Commit: `302b662` — `Add current stress break confirmation engine`
- Push status: PASS — pushed to `origin/main` after the handoff update
- Live pipeline: PASS; no warnings
- Frontend build: PASS
- VIX: `17.84`, 20D average `15.37`, 20-observation change `+3.21`, observation date `2026-09-10`; Market Fragility and Current Stress match exactly
- Current Stress: `Calm / No Break`, `0 / 6` active confirmations
- Signal states: Volatility Release `Watch`; Financial Stress `Calm`; Credit Conditions `Calm`; Claims Acceleration `Calm`; Sahm Confirmation `Calm`; Rapid Bull Steepening `Calm`
- Cycle / Recession: `10 / 28`; normalized risk `36 / 100`
- `.env`: ignored and not staged

Published files: `README.md`, `data/current.json`, `frontend/src/App.tsx`, `frontend/src/data/current.json`, `frontend/src/styles/current-stress.css`, `frontend/src/types/dashboard.ts`, `scripts/build_dashboard_data.py`, `scripts/current_stress.py`, `scripts/derived_metrics.py`, and `CHATGPT_HANDOFF.md`.

Positioning / Sentiment work was not started.

## Positioning / Sentiment v1 — Berkshire Review Status

Implemented locally and intentionally not committed or pushed.

| Field | Official Q2 2026 result | Status |
|---|---:|---|
| Insurance and Other cash | $35.096B | PASS |
| Short-term U.S. Treasury Bills | $324.905B | PASS |
| Railroad / Utilities / Energy cash | $5.513B | PASS |
| Total assets | $1,263.071B | PASS |
| Project-defined liquidity proxy | $365.514B | PASS |
| Liquidity / Total Assets | 28.9385% (display 28.9%) | PASS |
| Equity-security purchases YTD | $39.405B | PASS |
| Equity-security sales YTD | $27.780B | PASS |
| Net equity flow YTD | +$11.625B (display +$11.6B) | PASS |

Source: Berkshire Hathaway official Q2 2026 report, report date June 30, 2026, `https://www.berkshirehathaway.com/qtrly/2ndqtr26.pdf`; source status `live`. Derivations: liquidity = 35.096 + 324.905 + 5.513 = $365.514B; liquidity/assets = 365.514 / 1,263.071 = 28.9385%; net equity flow = 39.405 - 27.780 = +$11.625B. Interpretation: `Very High Liquidity · Net Buyer`.

Parser/dependency changes: added `scripts/fetch_berkshire.py`, official PDF row parsing with plausibility checks and fallback warning behavior, and `pypdf` in `requirements.txt`. Pipeline and official-parser validation: PASS with no warnings. Existing engines: PASS — 24 indicators, Cycle / Recession `10 / 28`, normalized risk `36 / 100`, Current Stress unchanged. Frontend build: PASS. Changed files: `scripts/fetch_berkshire.py`, `scripts/build_dashboard_data.py`, `data/sample_raw.json`, `data/current.json`, `frontend/src/data/current.json`, `frontend/src/types/dashboard.ts`, `frontend/src/App.tsx`, `frontend/src/styles/positioning.css`, `README.md`, `requirements.txt`, and this handoff. No SEC-wide insider, retail, Nasdaq, Yahoo Finance, TradingView, Elliott Wave, or composite positioning work was added.

## Berkshire Positioning Publication

The reviewed Positioning / Sentiment v1 Berkshire implementation is published.

- Commit: `1a15a96` — `Add Berkshire positioning context`
- Push status: PASS — pushed to `origin/main` after the handoff update
- Source status: `live`; official Berkshire Hathaway Q2 2026 report; no fallback warning
- Report date: `2026-06-30`
- Liquidity proxy: `$365.514B`
- Liquidity / Total Assets: `28.9385%` (display `28.9%`)
- Equity purchases YTD: `$39.405B`
- Equity sales YTD: `$27.780B`
- Net equity flow YTD: `+$11.625B` (display `+$11.6B`)
- Interpretation: `Very High Liquidity · Net Buyer`
- Cycle / Recession: `10 / 28`; normalized risk: `36 / 100`
- Current Stress: `Calm / No Break`, `0 / 6`; unchanged
- Pipeline/parser validation: PASS; frontend build: PASS; `.env` ignored and not staged

Published files: `README.md`, `requirements.txt`, `data/sample_raw.json`, `data/current.json`, `frontend/src/App.tsx`, `frontend/src/data/current.json`, `frontend/src/types/dashboard.ts`, `frontend/src/styles/positioning.css`, `scripts/build_dashboard_data.py`, `scripts/fetch_berkshire.py`, and `CHATGPT_HANDOFF.md`.

No SEC-wide insider aggregation, retail participation, Nasdaq, Yahoo Finance, TradingView, Elliott Wave, or new indicator work was started.

## SEC Form 4 Research POC — Review Status

Implemented research-only POC per sections 167–174. No production pipeline, generated dashboard JSON, frontend, scoring, GitHub Actions, or existing data source was modified. No commit or push was performed.

Files created: `scripts/research_sec_form4.py`, `research/sec_form4_poc.json`, and `research/sec_form4_notes.md`.

Methodology implemented: fetch one SEC EDGAR daily index; count Forms `4` and `4/A`; select a bounded 20–50 filing sample; fetch only ownership XML documents; parse Table I non-derivative transactions; extract issuer/owner identifiers, dates, codes, shares, acquired/disposed flag, prices, and direct/indirect ownership; retain only `P` and `S` for the research summary; exclude grants, gifts, exercises, withholding, and other codes; calculate dollar volume only where shares and price are both present. The script uses a declared project User-Agent, requires `SEC_CONTACT_EMAIL`, limits requests to 0.6 seconds apart (no more than 2/sec), caches responses, retries 429/5xx responses, and reports estimated 30-day request volume/runtime.

POC execution: `BLOCKED` before SEC requests because `SEC_CONTACT_EMAIL` is not configured locally. Requests attempted: `0`; cache hits: `0`; retries: `0`. This is an explicit fair-access safeguard, not an SEC parsing failure. The local JSON and markdown note record the blocker.

Required blockers before production: provide a real project-owner contact email; complete a live SEC run; quantify XML-shape coverage; define issuer universe; resolve Form 4/A supersession and duplicate handling; establish incremental persistent cache/monitoring; and review whether P/S dollar volume is analytically useful. SEC `P`/`S` values must remain labeled open-market **or private** purchase/sale activity, not pure open-market activity.

## SEC Form 4 POC — Live Execution Result

The configured local `SEC_CONTACT_EMAIL` was loaded at runtime only and was not printed, logged, copied into this handoff, or written to research output. The existing POC was run without code changes and remained research-only.

Result: `BLOCKED` at daily-index discovery. The script selected `2026-09-12`, which is a Saturday, and the SEC daily index request returned `HTTPError`. SEC requests: `1`; ownership XML requests: `0`; cache hits: `0`; retries: `0`; Form 4/4/A counts and P/S transaction metrics: unavailable because discovery failed. XML parse success, price coverage, and dollar-volume coverage: unavailable. Runtime was under two seconds.

The research JSON and markdown note were refreshed with this result. The remaining blockers are selecting a recent available SEC business-day index, then measuring XML-shape coverage, amendments/4/A supersession, duplicate transactions, issuer-universe effects, and 30-day request/runtime estimates from a successful sample. No production files changed, and no commit or push was performed.

## SEC Form 4 POC — Daily-Index Fix and Live Rerun

The daily-index discovery bug was fixed in the research-only script. It now reads the current quarter directory `index.json`, selects the newest eligible `master.YYYYMMDD.idx` not later than today, checks the previous quarter if needed, and retains a bounded backward probe fallback. The configured contact email was used only at runtime in the SEC User-Agent and is not present in this handoff or output.

Live result: PASS for discovery and research execution. Selected index: `master.20260911.idx`, date `2026-09-11`, discovery source `directory_index.json`. Counts: 895 Form 4 filings and 26 Form 4/A filings. Sample: 30 Form 4 filings. Ownership XML parse success: 7/30 (`23.3%`); 23 samples failed due to XML-directory/shape errors captured in the research JSON. Requests: 33 on the first post-fix run; cache hits 6; retries 0; runtime 26.12s. A subsequent cache-only rerun made 0 requests with 49 cache hits.

P/S-only summary from successfully parsed Table I rows: 4 `P` transactions, 8 `S` transactions; 2 buyer issuers, 2 seller issuers, 4 unique issuers, 2 buyer reporting owners, 2 seller reporting owners, 4 unique reporting owners. Price availability and dollar-volume coverage were both `100%` for the 12 retained P/S rows. Purchase dollar volume: `$842,926.84`; sale dollar volume: `$5,904,789.01`. Form 4/A amendments in the sampled filings: `0`.

Estimated 30-day backfill at a 30-filing sample: 1,830 requests (30 daily indexes + 900 filing-directory metadata requests + 900 XML requests), with a conservative rate floor of 1,098 seconds (~18.3 minutes), excluding retries and processing overhead.

Remaining blockers: improve XML-shape coverage beyond `23.3%`; investigate failed filing-directory/XML cases; define amendment supersession and duplicate handling; establish a licensing-safe issuer universe; implement persistent incremental cache/monitoring; and assess dollar-volume usefulness. SEC `P`/`S` remains open-market **or private** purchase/sale activity, not pure open-market activity. Production wiring remains prohibited. No production files changed and no commit/push was performed.

## SEC Form 4 POC — Filing-Shape Discovery Fix and Validation

The prior `23.3%` result was diagnosed filing-by-filing before changing discovery. All 23 failures had cached accession metadata and exactly one XML candidate, but the old resolver rejected generic filenames because it only accepted names containing `ownership` or `xslF345`. The individual audit was:

| Accession | Issuer CIK | Master-index path | Candidate XML | Diagnosis |
|---|---:|---|---|---|
| 000143774926030170 | 1001385 | `edgar/data/1001385/0001437749-26-030170.txt` | `rdgdoc.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000111623326000003 | 1032975 | `edgar/data/1032975/0001116233-26-000003.txt` | `form4-09112026_100950.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000107807526000139 | 1078075 | `edgar/data/1078075/0001078075-26-000139.txt` | `form4.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000115903626000119 | 1159036 | `edgar/data/1159036/0001159036-26-000119.txt` | `wk-form4_1789173314.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000143774926030184 | 1217614 | `edgar/data/1217614/0001437749-26-030184.txt` | `rdgdoc.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000176877326000010 | 1280784 | `edgar/data/1280784/0001768773-26-000010.txt` | `primarydocument.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000114036126036384 | 1379344 | `edgar/data/1379344/0001140361-26-036384.txt` | `form4.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000142681626000005 | 1426816 | `edgar/data/1426816/0001426816-26-000005.txt` | `form4-09112026_040925.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000147559726000241 | 1527541 | `edgar/data/1527541/0001475597-26-000241.txt` | `primary_doc.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000141176526000007 | 1595974 | `edgar/data/1595974/0001411765-26-000007.txt` | `wk-form4_1789157516.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000208640326000008 | 1636422 | `edgar/data/1636422/0002086403-26-000008.txt` | `primarydocument.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000171252526000005 | 1712525 |  `edgar/data/1712525/0001712525-26-000005.txt` | `form4-09112026_040921.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000110465926106986 | 1746109 | `edgar/data/1746109/0001104659-26-106986.txt` | `tm2625285-1_4seq1.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000177839526000007 | 1778395 | `edgar/data/1778395/0001778395-26-000007.txt` | `primarydocument.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000162828026061621 | 1832466 | `edgar/data/1832466/0001628280-26-061621.txt` | `wk-form4_1789173662.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000190183926000004 | 1901839 | `edgar/data/1901839/0001901839-26-000004.txt` | `form4-09112026_040902.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000162828026061589 | 1970265 | `edgar/data/1970265/0001628280-26-061589.txt` | `wk-form4_1789160636.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000209079826000006 | 2090798 | `edgar/data/2090798/0002090798-26-000006.txt` | `wk-form4_1789157359.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000208049826000005 | 2136387 | `edgar/data/2136387/0002080498-26-000005.txt` | `form4-09112026_040915.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000122520826007768 | 7084 | `edgar/data/7084/0001225208-26-007768.txt` | `doc4.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000078901926000199 | 789019 | `edgar/data/789019/0000789019-26-000199.txt` | `form4.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000131020426000027 | 882095 | `edgar/data/882095/0001310204-26-000027.txt` | `wk-form4_1789165843.xml` | fixed-filename filter miss; candidate is valid ownership XML |
| 000202206026000005 | 97134 | `edgar/data/97134/0002022060-26-000005.txt` | `form4-09112026_080953.xml` | fixed-filename filter miss; candidate is valid ownership XML |

The research resolver now inspects the exact filing path, then cached/live accession metadata, bounded relevant nested directories, and every XML candidate; it validates an `ownershipDocument` root/descendant before Table I parsing. The exact 2026-09-11 sample now passes **30/30 (100.0%)**, meeting the research-stage `>=90%` gate. Selected index: `master_20260911.idx`; 895 Form 4 and 26 Form 4/A filings; final cache-only run: 0 requests, 92 cache hits, 0 retries, 0.03s. P/S-only output: 4 purchases and 24 sales, 13 unique issuers/reporting owners, 100% price availability and dollar-volume coverage; sampled amendments: 0.

Because the gate passed, two additional 30-filing business-day validations were run: `master_20260910.idx` (30/30, 100.0%; 1,070 Form 4, 6 Form 4/A) and `master_20260909.idx` (30/30, 100.0%; 1,027 Form 4, 14 Form 4/A). Aggregate additional validation: **60/60 (100.0%)**. These runs used the same cache/retry/rate-limit policy; no production files, generated dashboard JSON, scoring, frontend, or workflows were changed. Form 4/A supersession and duplicate handling remain explicitly unresolved blockers. The configured SEC contact email remained runtime-only and is not present here or in research outputs. No commit or push was performed.

## Publication Note

## SEC Form 4/A Row-Level Reconciliation Study — Research Only

The Form 4/A study was reworked for sections 204–212. It no longer treats an amendment as a whole-accession replacement. The parser now retains `dateOfOriginalSubmission`, uses it as the primary original-date anchor with issuer and reporting-owner CIKs, and falls back to bounded filing-date heuristics only when the field is absent or ambiguous.

### Validation and matching

- Same amendment sample: **26/26 XML parses (100%)** across 2026-09-09, 2026-09-10, and 2026-09-11.
- `dateOfOriginalSubmission` coverage: **26/26 (100%)**.
- Original match confidence: high **16/26 (61.5%)**, medium **4/26 (15.4%)**, low **0/26 (0.0%)**, unmatched **6/26 (23.1%)**.
- Row actions: `replace_row` 7, `add_row` 4, `metadata_only` 17; ambiguous row actions 0.
- Amendment-level classes: `replace_row` 7, `add_row` 3, `metadata_only` 10, `unknown_or_unmatched` 6.
- Exact unchanged original rows are retained in each reconciled research record. Omitted unchanged lines in a 4/A are not treated as removals.

### Auditable reconciliation examples

| Amendment accession | Confidence | Selected original | Action | Original shares @ price | Amended shares @ price |
|---|---|---|---|---:|---:|
| `000086311026000091` | high | `0000863110-26-000088.txt` | replace_row | 2,000 @ 36.11 | 1,876 @ 36.11 |
| `000149315226042326` | high | `0001493152-26-042064.txt` | metadata_only | 31,250 @ 0.80 | 31,250 @ 0.80 |
| `000149315226042324` | high | `0001493152-26-042061.txt` | replace_row | 31,250 @ 0.78 | 31,250 @ 0.80 |
| `000166994326000021` | high | `0001669943-26-000019.txt` | metadata_only | 4,064 @ 85.44 | 4,064 @ 85.44 |
| `000178039626000015` | high | `0001780396-26-000010.txt` | replace_row | 3,747 @ 9.93 | 6,054 @ 9.93 |
| `000178039626000016` | high | `0001780396-26-000012.txt` | replace_row | 1,579 @ 9.73 | 2,551 @ 9.73 |
| `000193872226000015` | high | `0001938722-26-000010.txt` | replace_row | 3,747 @ 9.93 | 6,054 @ 9.93 |
| `000193872226000016` | high | `0001938722-26-000012.txt` | replace_row | 790 @ 9.73 | 1,276 @ 9.73 |
| `000149315226042324` | high | `0001493152-26-042061.txt` | replace_row | 31,250 @ 0.78 | 31,250 @ 0.80 |
| `000149315226042326` | high | `0001493152-26-042064.txt` | metadata_only | 31,250 @ 0.80 | 31,250 @ 0.80 |

The full records retain stable row keys based on issuer/owner, security title, transaction date/code, acquired-disposed flag, and direct/indirect ownership; shares and price are intentionally excluded from identity so corrected values can be matched. Remarks/footnotes are retained as corroborating metadata.

### P/S aggregate impact and duplicate caution

For the research-only reconciled rows, before/after P/S counts were `P 6 / S 6` and `P 10 / S 10`; dollar volume changed from `$5,120,176.12` to `$6,738,185.40`. After reconciliation, the diagnostic P/S rows represented 2 purchase issuers / 2 purchase owners and 3 sale issuers / 3 sale owners. These figures are not production aggregates: repeated amendment records and duplicate-risk rows are intentionally still visible for study.

The study retained 14 repeated row fingerprints and did not delete them. A conservative future policy is: use `dateOfOriginalSubmission` plus issuer/owner anchors; replace only stable-key-matched rows; add only genuinely new rows; leave metadata-only P/S totals unchanged; preserve all omitted original rows; and quarantine unmatched/ambiguous amendments rather than guessing. Whole-accession replacement is explicitly rejected.

Operational stats: 3 requests, 217 cache hits, 0 retries, approximately 2.36 seconds. Research outputs are `research/sec_form4a_study.json` and `research/sec_form4a_study.md`. No production files, generated JSON, scoring, frontend, workflows, or data pipeline were changed. No commit or push was performed.

## SEC Form 4/A Amendment Study — Research Only

The targeted amendment study required by sections 194–202 is complete. It uses the validated filing-shape-driven ownership XML resolver, retains the existing SEC User-Agent privacy safeguard, cache, retries, and <=2 requests/second policy, and does not modify production data or apply supersession.

### Sample and parse validation

| SEC index | Form 4 | Form 4/A | Amendments sampled | XML parsed |
|---|---:|---:|---:|---:|
| 2026-09-11 | 895 | 26 | 10 | 10/10 |
| 2026-09-10 | 1,070 | 6 | 6 | 6/6 |
| 2026-09-09 | 1,027 | 14 | 10 | 10/10 |

Targeted total: **26/26 (100.0%)**, exceeding the 95% research gate. Each record retains issuer CIK, reporting-owner CIKs, period of report, transaction rows, codes, shares, price, acquired/disposed flag, direct/indirect ownership, footnotes/remarks where present, and row fingerprints.

### Original matching and amendment classes

- Candidate original filings examined: 43; candidate original XML parses: 43/43.
- Match confidence: `high` 12, `medium` 10, `unmatched` 4; high-or-medium match rate **22/26 (84.6%)**, above the 80% research criterion.
- Amendment classes: `metadata_or_footnote_only` 6; `transaction_row_added` 1; `transaction_row_removed` 4; `unknown_or_unmatched` 15; `transaction_value_corrected` 0; `ownership_nature_corrected` 0; `reporting_owner_corrected` 0.
- The `unknown_or_unmatched` group is intentionally not forced into a correction class; the study preserves amendment and candidate-original fingerprints for review.

### Duplicate-risk observations

The study found 14 repeated row fingerprints among the sampled amendment rows. Examples include repeated issuer/owner/date/code/share/price/ownership combinations for CIK pairs `1512922/1258622`, `1512922/1302378`, `0102109/1212502`, `1046102/1763701`, `1474627/1869115`, and `1378950/1240508`. No sampled amendment had multiple reporting owners. These are diagnostic examples only: no repeated row was deleted or collapsed.

### Operational results

- Final run: 3 SEC requests, 217 cache hits, 0 retries, approximately 2.53 seconds.
- The contact email was read only at runtime and is not printed, logged, or copied here or into research output.
- Research outputs: `research/sec_form4a_study.json` and `research/sec_form4a_study.md`.

### SUPERSEDED — DO NOT USE: prior whole-accession policy

The earlier bullets in this section that described treating a Form 4/A as an authoritative replacement for an entire original accession are obsolete and rejected. They must not be used. The active research rule is row-level only: preserve unchanged original rows, add only added rows, replace only matched corrected rows, leave metadata-only P/S totals unchanged, and never replace a whole accession.

### Current row-level matching and duplicate audit — sections 214–222

The focused follow-up reprocessed the same 26 amendments and inspected the exact `dateOfOriginalSubmission` master-index dates, issuer candidates, owner CIK sets, periods, row overlap, and cached accession/XML evidence. The five unique accessions represented the original 10 non-high-confidence records (duplicates in the sampled selection):

- Six of the prior unmatched records became **high confidence** after exact-date discovery: `000147793226005514` selected `edgar/data/1474627/0001477932-26-005466.txt`; `000114036126036091` selected `edgar/data/1378950/0001140361-26-034452.txt`; and `000168316826007039` selected `edgar/data/1756180/0001683168-26-002886.txt`.
- The four prior medium records remain **medium**, not forced higher: `000149315226042004` selected `edgar/data/1702924/0001493152-26-041637.txt`, and `000149315226042002` selected `edgar/data/1702924/0001493152-26-041638.txt`. Each has four same-issuer exact-date Form 4 candidates; owner identity narrows the candidate, but the amendment carries no Table I row evidence sufficient for a high-confidence upgrade.

Final confidence across all 26: **high 22/26 (84.6%)**, medium 4/26 (15.4%), low 0, unmatched 0. `dateOfOriginalSubmission` coverage remains 26/26. The high-confidence gate in section 221 is **not met** because 84.6% is below 90%; production remains blocked.

All 14 repeated row fingerprints were classified as `same_accession_duplicate_attachment` at the research-sample level: each repeated fingerprint occurred twice under the same amendment accession and selected original, indicating repeated index/sample/attachment representation rather than two proven economic events. Each should count **once** pending direct attachment-level confirmation. No repeated fingerprint was deleted. No multi-owner representation, cross-filing duplicate, legitimate repeated same-day transaction, or same-amendment distinct duplicate was established in this sample; those remain possible classes requiring broader research.

Reconciled row semantics remain unchanged. P/S diagnostic totals moved from `P=10, S=8` before amendment actions to `P=14, S=12` after row-level additions/replacements; dollar volume moved from `$5,673,914.01` to `$7,291,923.29`. These are research diagnostics and are not production aggregates because duplicate rows remain visible and no production deduplication has been applied.

Exact-date audit evidence, all 10 focused cases, all 14 duplicate classifications, row actions, candidate sets, and fingerprints are in `research/sec_form4a_study.json`. Final operational stats: 3 requests, 324 cache hits, 0 retries, approximately 2.55 seconds. No production files changed and no commit or push was performed.

### Proposed production supersession/dedup policy — not implemented

1. For a high-confidence Form 4/A match, apply only row-level add/replace/metadata actions; never replace the matched original accession as a whole.
2. Exclude unmatched and low-confidence amendments from aggregates and mark them for review rather than guessing.
3. Compare transaction rows using the retained diagnostic fingerprint; do not erase legitimate repeated same-day transactions automatically.
4. Deduplicate exact repeated rows only within a reviewed accession context, and never aggregate an original together with its superseding amendment.
5. Preserve amendment coverage, match confidence, and excluded counts as quality metadata before any future production signal is considered.

Status: **research complete; production remains blocked pending review of unmatched/unknown amendments, broader issuer/date validation, and approval of the supersession policy.** No production files changed, and no commit or push was performed.

The reviewed CAPE remediation is published in `14d9ffd`; the live-source verification and push status above supersede earlier pre-publication wording in this handoff.

## SEC Form 4/A — Accession-Normalized Validation (Authoritative)

This section supersedes older raw-record amendment metrics. The research layer now canonicalizes one amendment record per SEC accession while retaining every master-index row, accession-directory file list, XML candidate, and attachment diagnostic.

### Why duplicate amendment records appeared

The prior 26-record focus sample contained 10 duplicated accession representations. Each duplicate accession appeared twice on the same SEC business-day index under two issuer/owner directory paths, for example `edgar/data/1258622/...042326.txt` and `edgar/data/1512922/...042326.txt`. The accession directory for each had one XML candidate (`ownership.xml`, `doc4a.xml`, `form4a.xml`, `form4.xml`, or `wk-form4a_*.xml`) and no multiple ownership XML documents. This was a duplicate master-index representation of one submission, amplified by sampling each raw master-index row; it was not a second economic event and not a multiple-attachment case. Canonicalization reduces 26 raw records to 16 unique accessions in the focus sample. Repeated row fingerprints are therefore counted once, while attachment diagnostics remain retained.

### Focus sample, raw versus unique

- Raw focus sample: 26 records; unique accessions: 16; duplicate records: 10.
- Raw confidence: high 22/26, medium 4/26, low 0, unmatched 0.
- Unique confidence: high 12/16 (**75.0%**), medium 4/16 (**25.0%**), low 0, unmatched 0.
- `dateOfOriginalSubmission`: 100% coverage.
- The 14 repeated fingerprints were classified as same-accession duplicate attachment/index representations and should count once pending attachment-level review. Duplicate attachment rate: 0 multiple-ownership-XML cases among 10 duplicated accession groups; 100% of duplicated groups had one ownership XML candidate.

### The two unique medium-confidence accessions

| Amendment accession | Table I rows | P rows | S rows | Table II rows | Remarks/footnotes | P/S economic effect |
|---|---:|---:|---:|---:|---|---|
| `000149315226042004` | 0 | 0 | 0 | 0 | none extracted | Cannot change P/S aggregate; quarantine as unresolved/unknown |
| `000149315226042002` | 0 | 0 | 0 | 0 | none extracted | Cannot change P/S aggregate; quarantine as unresolved/unknown |

These amendments are not upgraded to high confidence. Their zero-row XML shape supports P/S quarantine, but because no explicit metadata/footnote change was extracted they remain `unknown` rather than being represented as a proven metadata-only amendment.

### Broader unique-accession validation

Validation covered **56 unique Form 4/A accessions** across five SEC business-day indexes:

| Index date | Form 4/A filings sampled |
|---|---:|
| 2026-09-11 | 13 |
| 2026-09-10 | 3 |
| 2026-09-09 | 7 |
| 2026-09-08 | 16 |
| 2026-09-04 | 17 |

Unique XML parse coverage was **56/56 (100%)**. Unique match confidence: high 37/56 (**66.1%**), medium 18/56 (**32.1%**), low 0, unmatched 1/56 (**1.8%**). `dateOfOriginalSubmission` coverage remained 100%. Economic relevance: P/S Table I 17; non-P/S Table I 34; unknown 5. Five non-high-confidence P/S amendments remain quarantined, so the unresolved P/S-relevant rate is **5/17 (29.4%)**. Metadata/non-P/S unresolved count is 14/56 (**25.0%**). Row-action resolution was 100% for the generated row actions, but this does not override unresolved original matching.

Every unique accession record retains parse status, date/issuer/owner anchors, selected original, confidence, row actions, P/S relevance, and quarantine status. Future production interpretation is conservative: high-confidence amendments may reconcile row-by-row; non-high-confidence zero-P/S amendments remain quarantined as economically irrelevant only where proven; any non-high-confidence P/S amendment remains quarantined and would make the affected rolling period degraded.

Operational stats for the broader run: 129 requests, 1,072 cache hits, 0 retries, approximately 113.5 seconds. No production files, generated JSON, scoring, frontend, workflows, or existing pipeline were changed. No commit or push was performed. Research outputs are `research/sec_form4a_study.json`, `research/sec_form4a_focus.json`, and `research/sec_form4a_study.md`.

### Refined production gate result

**NOT MET.** Ordinary and targeted XML parsing pass the current research thresholds, but unique-accession high-confidence matching is only 66.1%, the focus unique rate is 75.0%, and 5 unique P/S-relevant amendments remain quarantined. The SEC insider work remains research-only.

## CURRENT AUTHORITATIVE SEC RESEARCH STATUS — Rolling 30-Day Simulation

This section supersedes prior SEC status summaries for the rolling-window task. The simulation runner is implemented at `scripts/research_sec_rolling.py`, but the complete XML simulation was not completed in this run because the required full-universe request volume is materially larger than the prior sampled studies. No aggregates are claimed without parsing the complete universe.

### Completed inventory

Window: **2026-08-13 through 2026-09-11**, ending on the latest available SEC filing day used by the research run.

- SEC business days processed: 21
- Form 4 master-index rows: **24,627**
- Form 4/A master-index rows: **512**
- Unique Form 4 accessions: **11,791**
- Unique Form 4/A accessions: **241**
- The inventory completed from cached SEC daily indexes with no production requests or data writes.

The exact index counts and duplicate-row total (**13,107**) are in `research/sec_form4_rolling30.json` with `status: inventory_only`.

### Why the full simulation remains pending

The complete requested pipeline requires ownership-directory metadata and XML retrieval for every unique accession, followed by parsing all Table I rows and matching/quarantine reconciliation. At the enforced 0.6-second minimum interval, this is tens of thousands of SEC requests and several hours of minimum runtime. The initial full attempt was stopped before producing partial aggregates; therefore no raw-original, high-confidence-reconciled, or final quarantine-adjusted 30-day P/S totals are reported here.

The research runner preserves the required A/B/C model, canonical accession state, candidate-original quarantine, P/S-only aggregation, quality fields, cache/retry counters, and request/runtime estimates. It must be allowed to complete end-to-end before any market-level conclusion is drawn. This is an operational research blocker, not evidence about the economic signal.

Production remains blocked. No production dashboard, generated JSON, scoring, frontend, GitHub Actions, or existing data pipeline was modified. No commit or push was performed. `SEC_CONTACT_EMAIL` was not printed or copied into output.

## CURRENT AUTHORITATIVE SEC RESEARCH STATUS — Ingestion Architecture POC

This section supersedes the prior rolling-crawl feasibility note for the ingestion-architecture task. The full 30-day XML universe was intentionally **not** rerun.

### Complete-submission parity result

The research-only runner [research_sec_ingestion.py](C:/Users/Liorkale/Desktop/recession-web/scripts/research_sec_ingestion.py) fetches the exact master-index `.txt` filing path, extracts the local `<DOCUMENT>` / `<TEXT>` ownership XML block, strips the SEC `<XML>` wrapper, validates `ownershipDocument`, and parses it with the existing ownership parser. Accession-directory metadata and separate XML remain the fallback path.

- Form 4 parity sample: **100 unique accessions**
- Form 4/A parity sample: **20 unique accessions**
- Ownership-document discovery: **120/120 (100%)**
- Directory/XML fallback: **0/120 (0%)**
- Field-level parity: **100%**; mismatches: **0**
- Compared issuer CIK, reporting-owner CIKs, period, original-submission date, Table I rows, transaction date/code/shares/price/acquired-disposed/direct-indirect fields, Table II count, and footnotes/remarks.
- POC run statistics: 40 network requests, 440 cache hits, 0 retries; all 120 records had zero parity failures.

The optimized path reduces the theoretical per-accession design from metadata + XML to one complete-submission request: approximately **50% fewer requests** (12,032 instead of 24,064 for the inventoried universe), subject to fallback requests. It must not be used for the full crawl until broader operational review is complete.

### Resumable checkpoint verification

The POC persists accession-keyed state in `research/sec_live_state.json`, including form type, filing date/path, fetch status, parse status, normalized rows, source method, and failure metadata. A restart simulation skipped all **3/3** previously successful test accessions and issued **0** repeat requests. State is research-only and is not connected to production.

### Official SEC 2026 Q2 bulk dataset

The SEC official [Insider Transactions Data Sets page](https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets) lists **2026 Q2 345** at approximately **10.97 MB** and states coverage through June 2026, quarterly updates, and as-filed flattened XML-derived data. The official [data documentation](https://www.sec.gov/files/insider_transactions_readme.pdf) defines eight tab-delimited UTF-8 tables:

- `SUBMISSION`: primary key `ACCESSION_NUMBER`; filing date, period, original-submission date, document type, issuer, remarks and filing flags.
- `REPORTINGOWNER`: `ACCESSION_NUMBER + RPTOWNERCIK`.
- `NONDERIV_TRANS`: Table I rows keyed by `ACCESSION_NUMBER + NONDERIV_TRANS_SK`, including transaction date/code, shares, price, acquired/disposed, ownership and footnote IDs.
- `NONDERIV_HOLDING`: Table I holdings.
- `DERIV_TRANS` and `DERIV_HOLDING`: Table II transactions/holdings.
- `FOOTNOTES`: `ACCESSION_NUMBER + FOOTNOTE_ID`.
- `OWNER_SIGNATURE`: `ACCESSION_NUMBER + OWNERSIGNATURENAME`.

The Q2 ZIP was not downloaded in this task. The bulk data is suitable as the historical baseline through June 2026, but not as the current September 2026 source.

### Proposed hybrid architecture

Use the quarterly bulk dataset for historical state and backtesting through the latest completed quarter. Use complete-submission EDGAR ingestion for the current-quarter delta, keyed by canonical accession and checkpointed locally. Reconcile Form 4/A rows against local Form 4 state first; use SEC directory/XML fallback only when complete-submission extraction fails. At the next quarterly release, compare the bulk compaction checkpoint against accumulated live state before replacement. No sentiment score or bullish/bearish threshold is defined.

No production files, dashboard JSON, scoring, frontend, workflows, or existing pipeline changed. No commit or push was performed. Research outputs are `research/sec_submission_parity.json`, `research/sec_live_state.json`, and `research/sec_submission_parity.json`'s documented bulk schema fields.

## CURRENT AUTHORITATIVE SEC RESEARCH STATUS — Full 30-Day Run Checkpoint

The complete-window runner required by sections 258–267 is implemented at [research_sec_full.py](C:/Users/Liorkale/Desktop/recession-web/scripts/research_sec_full.py). It uses the inventoried 2026-08-13 through 2026-09-11 universe, canonicalizes by `(form, accession)`, retrieves complete-submission `.txt` first, persists accession state after deterministic 300-accession batches, and applies the existing row-level/quarantine policy only at finalization.

Execution reached a clean checkpoint boundary:

- Completed: **300 / 12,032** unique accessions
- Remaining: **11,732**
- Batch size: 300
- Batch requests: 195; cache hits: 105; retries: 0; HTTP 429s: 0
- State file: `research/sec_full_state.json` (~646,655 bytes)
- Progress file: `research/sec_full_progress.json`

The full run was stopped after this completed batch because the enforced 0.6-second minimum request interval makes the remaining complete-submission crawl a multi-hour operation. No final A/B/C market views are reported from partial data. In particular, no partial P/S ratio, quarantine impact, or production-feasibility conclusion should be inferred from this checkpoint. The runner can resume by rerunning the same command; completed accessions are skipped and successful fetches are not refetched.

Production remains blocked pending completion and review of all 12,032 accessions. No production dashboard, generated JSON, scoring, frontend, workflows, or existing pipeline changed. No commit or push was performed.

## CURRENT AUTHORITATIVE SEC RESEARCH STATUS — Resume Checkpoint Update

The full-window run resumed from the prior 300-accession checkpoint without restarting or deleting cache/state. One additional deterministic 300-accession batch completed and flushed successfully:

- Target window: 2026-08-13 through 2026-09-11
- Target unique accessions: **12,032**
- Completed: **600**
- Remaining: **11,432**
- Completed accession keys: unique; completed + remaining = **12,032**
- Successful parsed accessions: **599**
- Failed accessions: **1** (preserved with failure metadata; not fabricated)
- Complete-submission successes: **599**
- Directory/XML fallback successes: **0**
- Latest batch operational counters: 291 requests, 8 cache hits, 0 retries, 0 HTTP 429s
- State file: `research/sec_full_state.json`, approximately **1,306,240 bytes**
- Progress file: `research/sec_full_progress.json`

A subsequent resume attempt did not reach its next 300-accession flush within the safe execution window and was stopped before checkpoint mutation. The saved 600-accession checkpoint remains intact, and no previously successful accession regressed. No partial P/S aggregates, ratios, quarantine impact, sentiment, or production-feasibility conclusion are reported. The complete A/B/C reconciliation remains deferred until all 12,032 accessions finish.

## HISTORICAL / SUPERSEDED SEC RESEARCH STATUS — 100-Accession Resume Checkpoint

Sections 277–283 supersede the prior 300-batch checkpoint details. The research runner now enforces deterministic **100-accession** checkpoint batches and resumed from the saved 600-accession state without restarting or refetching successful accessions.

- Fixed target universe: **12,032** unique accessions
- Window: **2026-08-13 through 2026-09-11**
- Completed: **1,100**
- Remaining: **10,932**
- Successful parses: **1,097**
- Preserved failures: **3** (0.33%, below the 1% operational diagnosis threshold)
- Complete-submission successes: **1,097**
- Fallback successes: **0**
- Latest completed batch: 100 accessions
- Latest-run counters: 98 requests, 2 cache hits, 0 retries, 0 HTTP 429s
- State size: approximately **2,361,723 bytes**
- Latest completed batch: 100 accessions
- Latest-run counters: 51 requests, 47 cache hits, 0 retries, 0 HTTP 429s
- State size: approximately **1,986,324 bytes**

Checkpoint integrity passed before and after the run: target remained 12,032, completed keys remained unique, completed + remaining equals 12,032, and no prior successful accession regressed. A subsequent batch did not reach its next flush within the safe execution window and was stopped before state mutation. No partial P/S aggregates, buyer/seller ratios, quarantine impact, sentiment, or production-feasibility conclusion is reported. The final A/B/C reconciliation remains deferred until all accessions complete.

## CURRENT AUTHORITATIVE SEC RESEARCH STATUS — DEFERRED

Per PROJECT_INSTRUCTIONS sections 293–296, the SEC insider full backfill is **DEFERRED** and is no longer the active project priority. No further accessions will be processed unless SEC insider research is explicitly reactivated.

Preserved local checkpoint:

- Fixed universe: 12,032 accessions for 2026-08-13 through 2026-09-11
- Completed: **1,100**
- Remaining: **10,932**
- Successful parses: **1,097**
- Preserved failures: **3**
- Complete-submission successes: **1,097**
- Fallback successes: **0**
- State: `research/sec_full_state.json`
- Progress: `research/sec_full_progress.json`
- Cache: `research/.sec_cache/`
- Latest completed batch: 100 accessions
- Latest-run counters: 98 requests, 2 cache hits, 0 retries, 0 HTTP 429s
- State size: approximately **2,361,723 bytes**

The state and cache were preserved and not deleted by this priority reset. SEC insider data remains research-only and is not connected to the dashboard, scoring, generated production JSON, frontend, workflows, or production data pipeline.

Next project priority: return to the core US recession/cycle objective, especially labor deterioration, claims acceleration, JOLTS/labor-demand review, consumer deterioration, rates/credit stress confirmation, and robustness of the existing recession-risk score. No automatic scoring changes are implied by this priority reset.

## Labor Market v2 — Validation (sections 298–308)

- Scope: labor derivations and presentation only; SEC insider full backfill remains deferred and no SEC state/cache was resumed or changed.
- `.gitignore`: PASS for `.env`, `research/.sec_cache/`, `research/_sec_cache/`, `research/sec_live_state.json`, `research/sec_live_failures.json`, `research/sec_live_progress.json`, `research/sec_full_state.json`, and `research/sec_full_progress.json`; the whole `research/` directory is not ignored.
- Payrolls: PASS — latest monthly change, 3-month average monthly change, and 12-month average monthly change are generated from PAYEMS.
- Initial Claims: PASS — canonical ICSA derivation exposes latest claims `206,000`, 4-week average `206,000`, 4-week average 13 weeks ago `219,250`, and 13-week change `-6.0%`. Current Stress consumes the same derived object; its claims signal matches these values exactly.
- JOLTS: PASS — Hires and Quits expose latest, 3-month average, 12-month average, and descriptive trend without adding score components.
- Unemployment/Sahm and wages: PASS — unemployment 3-month average and 12-month change, Sahm threshold reference, wage latest YoY, 3-month average YoY, and 12-month growth-rate change are displayed without scoring changes.
- Score invariant: PASS — Cycle / Recession remains `10 / 28`, normalized risk `36 / 100`; no thresholds, denominator, or scored-indicator count changed.
- Frontend: PASS — `npm run build` completed successfully (`tsc -b` and Vite production build).
- Pipeline: PASS — real-key Python pipeline completed and synchronized `data/current.json`, `data/history.json`, and frontend data.
- `.env`: PASS — ignored by Git and not staged. No commit or push was performed.

## CURRENT AUTHORITATIVE LABOR RESEARCH STATUS

### Labor Market v2 publication

- Commit: `0a62b383b7ba666dd5dd73e2e358a599b557ad1d`
- Message: `Improve labor market trend signals`
- Push: PASS — pushed to `origin/main`.
- Published files: `.gitignore`, `CHATGPT_HANDOFF.md`, `data/current.json`, `frontend/src/components/IndicatorCard.tsx`, `frontend/src/data/current.json`, `scripts/build_dashboard_data.py`, `scripts/current_stress.py`, `scripts/derived_metrics.py`.
- Final checks: real-key pipeline PASS; frontend build PASS; generated JSON synchronized; score `10 / 28`; normalized risk `36 / 100`; no scoring, threshold, denominator, data-source, workflow, or infrastructure changes.

### Labor Scoring Robustness Study — research only

- FRED `USREC` is an evaluation label only and never enters production scoring.
- Coverage: PAYEMS 1939–2026, ICSA 1967–2026, JOLTS Hires/Quits 2000–2026, UNRATE 1948–2026, SAHMREALTIME 1959–2026, USREC 1854–2026.
- Canonical current metrics: payroll latest/3M/12M `+162K / +71.3K / +50.3K`; claims latest/4W/prior-4W/13W change `206,000 / 206,000 / 219,250 / -6.04%`; JOLTS Hires `3.2 / 3.3 / 3.3`; Quits `1.9 / 2.0 / 2.0`.
- JOLTS Hires/Quits correlation: `0.746` overall, `0.967` in recession months, `0.719` outside recession months.
- Same-month descriptive correlations with USREC: PAYEMS `-0.108`, ICSA `0.265`, JOLTS Hires `-0.184`, JOLTS Quits `-0.153`, UNRATE `0.148`, SAHM `0.306`.
- Recommendation: retain production scoring unchanged; evaluate payroll smoothing and claims acceleration as context candidates; treat Hires/Quits as overlapping evidence; treat Sahm as confirmation/context pending further timing analysis.
- Research-only outputs: `scripts/research_labor_robustness.py`, `research/labor_scoring_robustness.json`, `research/labor_scoring_robustness.md`.
- No scoring implementation was started. SEC insider research remains DEFERRED / historical and must not resume.

## CURRENT AUTHORITATIVE LABOR TIMING RESEARCH STATUS

Research-only study completed under PROJECT_INSTRUCTIONS sections 322–334. No production scoring, thresholds, denominator, frontend semantics, generated production JSON, workflows, infrastructure, or data sources were changed. No commit or push was performed for this study.

- Evaluation label: FRED `USREC` only; never a production feature.
- Event framework: recession episodes evaluated at `t-12`, `t-6`, `t-3`, `t`, and `t+3`.
- Event-window medians:
  - Payroll latest change: `+228K / +93K / +108K / -99K / -155K`.
  - Payroll 3M average: `+162K / +119.3K / +91K / -12.7K / -131.3K`.
  - Payroll 12M average: `+170.4K / +151.4K / +152.1K / +77.1K / +16.1K`.
  - Payroll 3M-minus-12M momentum: `+16.9K / +2.1K / -28.9K / -89.8K / -149.8K`.
  - Claims 4W average: `295,125 / 307,125 / 334,125 / 390,500 / 422,375`.
  - Claims 13W acceleration: `-1.5% / +5.0% / +4.0% / +12.4% / +11.7%`.
  - Unemployment: `4.6% / 4.3% / 4.5% / 4.65% / 5.15%`.
  - Sahm: `0.02 / 0.07 / 0.13 / 0.30 / 0.53`.
- Episode consistency using simple descriptive events: payroll latest negative before start `28.6%`; payroll momentum negative `37.1%`; claims acceleration positive `22.9%`; unemployment fixed reference rise `17.1%`; Sahm `0.50` confirmation `8.6%`. These are not optimized production thresholds.
- False-warning behavior: negative payroll months outside USREC `116/919 (12.6%)`; positive claims acceleration months `241/628 (38.4%)`; Sahm ≥0.50 outside USREC `106/705 (15.0%)`.
- JOLTS overlap: Hires/Quits correlation `0.746`; 3-month lead correlations are `0.771` for Hires leading Quits and `0.690` for Quits leading Hires. Neither is established as distinct enough to change production weighting.

| Signal | Role | Leading? | Redundant? | Recommended future status |
|---|---|---|---|---|
| Payroll latest | Early but noisy | Limited; 28.6% prior-event consistency | Partly overlaps smoothing | Keep scored unchanged; smoothing as context |
| Payroll 3M/12M/momentum | Trend context | Momentum earlier than level, 37.1% consistency | High overlap by construction | Needs more research before replacement |
| Claims 4W level | Labor stress level | Limited at fixed 75th-percentile reference | Related to acceleration | Keep current scored level |
| Claims 13W acceleration | Change/early-warning context | 22.9% prior-event consistency | Complements level | Keep as context/confirmation |
| JOLTS Hires | Labor demand | No reliable early signal under fixed reference | High overlap with Quits | Keep scored pending further study |
| JOLTS Quits | Worker confidence | Limited under fixed reference | High overlap with Hires | Needs more research; possible context-only |
| Unemployment | Slow deterioration | Limited lead behavior | Overlaps Sahm | Keep scored unchanged |
| Sahm Rule | Recession confirmation | Mostly confirmation, not leading | Overlaps unemployment | Confirmation/context candidate |

Coverage limitations: JOLTS begins in 2000; claims begins in 1967; older labor-force regimes are structurally different; raw payroll changes are not comparable across decades without normalization. Research outputs are `scripts/research_labor_timing.py`, `research/labor_timing_incremental.json`, and `research/labor_timing_incremental.md`.

## CURRENT AUTHORITATIVE BROAD CYCLE RESEARCH STATUS

Research-only Broad Cycle Confirmation Study completed under PROJECT_INSTRUCTIONS sections 339–349. No production scoring, thresholds, denominator, frontend, generated production JSON, workflows, infrastructure, data sources, or SEC state were changed. No commit or push was performed.

- Series: PAYEMS, W875RX1, INDPRO, CMRMTSPL; PCEC96 was fetched only as secondary context and excluded from the 0–4 breadth measure. FRED `USREC` was used only as a historical evaluation label.
- Current latest metrics: PAYEMS (2026-08) `+0.135%` 3M / `+0.381%` 12M, improving; W875RX1 (2026-07) `+0.561%` / `-0.379%`, flat/mixed; INDPRO (2026-07) `+0.462%` / `+1.079%`, improving; CMRMTSPL (2026-06) `+0.062%` / `+2.189%`, improving.
- Four-series breadth uses transparent descriptive rules: index series deteriorate only when both 3M and 12M growth are negative; PAYEMS also requires a negative latest monthly change. Current common date is 2026-06: `1/4` deteriorating; research conclusion: **Broad activity is slowing but not contracting**.
- Breadth history: `3-of-4` occurred in 53 recession months and 5 non-recession months; `4-of-4` occurred in 27 recession months and 1 non-recession month. This is descriptive evidence only, not an NBER score or recession probability.
- Coverage: PAYEMS 1939–2026, W875RX1 1959–2026, INDPRO 1919–2026, CMRMTSPL 1967–2026, PCEC96 2007–2026. CMRMTSPL is the lagging common-date constraint.
- CMRMTSPL source safeguard: FRED identifies it as a BEA-derived/spliced real manufacturing and trade sales series. It remains research-only pending explicit redistribution/licensing review; no production publication is recommended yet.

Decision: keep all current production scoring unchanged. Research outputs: `scripts/research_broad_cycle.py`, `research/broad_cycle_confirmation.json`, and `research/broad_cycle_confirmation.md`.

## CURRENT AUTHORITATIVE CONSUMER PRESSURE RESEARCH STATUS

Research-only Consumer Pressure & Household Resilience Study completed under PROJECT_INSTRUCTIONS sections 355–367. No production scoring, thresholds, denominator, frontend, generated JSON, workflows, infrastructure, data sources, or SEC state were changed. No commit or push was performed.

- Approved series: PCEC96, DSPIC96, PSAVERT, TDSP, DRCCLACBS; W875RX1 was secondary income-quality context only. USREC was an evaluation label only.
- Current state: PCEC96 (2026-07) 3M `+0.82%`, 12M `+2.14%`, resilient; DSPIC96 3M `+0.92%`, 12M `+0.45%`, resilient; PSAVERT `3.0%`, 12M change `-33.3%`, cushion pressured; TDSP (2026-Q1) `11.16`, 25th historical percentile; DRCCLACBS (2026-Q2) `2.85%`, 31.2nd percentile and down `6.25%` YoY.
- Exact divergence formula: `consumer_cashflow_gap = PCEC96 6M annualized growth - DSPIC96 6M annualized growth`, with annualized six-month growth equal to `2 × six-month percent change`. Latest gap: `+3.17 pp`; consumption is outrunning real disposable income.
- Consumer breadth is descriptive only: spending resilient, income resilient, saving-rate cushion pressured, debt/delinquency resilient; `1/4` pressured blocks on the latest common monthly date `2026-07`. Research conclusion: **Consumer is losing momentum**.
- Event study: spending pressure was mostly coincident (`50.0%` pressured at t=0, `0.0%` at t-3); saving-rate pressure was visible at t-3 (`100.0%` episode consistency under the descriptive rule); debt/delinquency pressure was mixed and frequency-limited (`50.0%` at t-6/t-3/t=0); income pressure was not consistently leading. False-warning counts across 215 non-recession common months: spending 2, income 15, saving cushion 98, debt/delinquency 33.
- Overlap review: W875RX1 must not be double-counted with DSPIC96; credit-card delinquency remains distinct from mortgage delinquency; TDSP is household debt burden and does not duplicate Current Stress market signals; no consumer measure is added to production.
- Coverage/caveats: monthly PCEC96/DSPIC96/PSAVERT and quarterly TDSP/DRCCLACBS; quarterly observations were not interpolated and event comparisons use as-of observations; FRED history is revised, not real-time vintage data; ratio levels are regime-dependent.

Decision: keep all measures research-only or context candidates pending separate review. Outputs: `scripts/research_consumer_pressure.py`, `research/consumer_pressure.json`, `research/consumer_pressure.md`.

## CURRENT AUTHORITATIVE CORPORATE PRESSURE RESEARCH STATUS

Research-only Corporate Profit & Credit Transmission Study completed under PROJECT_INSTRUCTIONS sections 372–385. No production scoring, thresholds, denominator, frontend, generated JSON, workflows, infrastructure, data sources, or SEC state were changed. No commit or push was performed.

- Current state: CPATAX (2026-Q2) `3,921.445`, QoQ `+8.22%`, YoY `+20.31%`, 100th historical percentile, profit/GDP `12.07%`; DRTSCILM (2026-Q3) `0.0%`, 46.9th percentile, 4Q average `4.975`; BUSLOANS (2026-08) 3M `+1.96%`, 12M `+9.80%`, momentum `-7.84 pp`; ISRATIO (2026-06) `1.30`, 24.5th percentile, 12M change `-6.47%`.
- Corporate breadth is descriptive only: profits resilient, lending standards pressured, C&I loan growth resilient, inventory/sales resilient; `1/4` pressured blocks at the latest common date `2026-06`. Research conclusion: **Corporate momentum is slowing**.
- Event medians: profit YoY was positive through t-3 and negative at t=0; lending standards rose from `2.8` at t-12 to `36.8` at t-3 and `39.4` at t=0; loan growth remained positive around recession starts; inventory ratios were elevated around t-3/t=0. This supports credit tightening as the clearest transmission signal, but not a production trigger.
- Episode consistency under the descriptive block rules was low across the full historical episode set: at t-3 profits `5.7%`, lending standards `8.6%`, loan growth `0%`, inventories `5.7%`. False-warning counts across 386 non-recession tested months: profits 76, lending standards 165, loan growth 112, inventories 139.
- Overlap review: DRTSCILM measures bank lending standards, distinct from NFCICREDIT/STLFSI4 financial stress; BUSLOANS measures credit quantity and can reflect demand or stress borrowing; CPATAX is corporate fundamentals, distinct from INDPRO but related; ISRATIO is operating-cycle pressure; Margin Debt/GDP is market leverage; Current Stress and Yield Curve remain separate confirmation engines.
- Revised-data caveat: CPATAX and DRTSCILM are quarterly and revised; event values use the latest observed as-of quarter without interpolation. This is not a real-time vintage backtest.

Decision: keep all four corporate measures research-only/context candidates pending further review. Outputs: `scripts/research_corporate_pressure.py`, `research/corporate_pressure.json`, `research/corporate_pressure.md`.

## CURRENT AUTHORITATIVE SCORE ARCHITECTURE AUDIT STATUS

Research-only audit completed under PROJECT_INSTRUCTIONS sections 390–402. No production scoring, thresholds, denominator, scored-indicator count, frontend, generated JSON, workflows, infrastructure, data sources, or SEC state were changed. No commit or push was performed.

- Authoritative production baseline from the actual scorer: **14 scored indicators, 10 / 28 points, normalized risk 36 / 100, regime Slowdown**.
- Domain denominator shares: Labor `12/28 (42.9%)`, Business `6/28 (21.4%)`, Housing `6/28 (21.4%)`, Rates `2/28 (7.1%)`, Mortgage/Household Credit `2/28 (7.1%)`. Labor currently contributes `4/10` points.
- Labor redundancy: existing research found Hires/Quits correlation `0.746` overall and `0.967` during recession months, supporting duplicate-vote concern. Sahm crossed `0.50` before only `8.6%` of episodes and is primarily confirmation-like despite equal cycle-score treatment.
- Threshold audit: payrolls/claims/ISM/yield curve are reasonable-but-provisional; Hires, Quits, wages, housing, mortgage delinquency and similar level rules are weak/heuristic; LEI is manual/insufficiently testable; Sahm is strongly supported as confirmation but its equal cycle weight is questionable.
- Thought experiments: A current `10/28`; B collapse Hires/Quits to one vote and treat Sahm as confirmation `9/24` (38/100, non-production); C remove Sahm from cycle denominator while retaining other votes `10/26` (38/100, non-production). No historical composite was fabricated because manual LEI/ISM history limits full reconstruction.
- Evidence-chain review covers Labor, Housing, Yield Curve/Rates, Broad Activity, Consumer, Corporate/Credit, Market Fragility, Current Stress, Valuation and Positioning, distinguishing score drivers, context, confirmation and vulnerability.
- Ranked shortlist: (1) separate Sahm as confirmation/context, (2) further Hires/Quits de-duplication study, (3) add broader activity/consumer/credit only as context first. All require separate approval; no implementation is recommended in this task.
- Research outputs: `scripts/research_score_architecture.py`, `research/score_architecture_audit.json`, `research/score_architecture_audit.md`.

## HISTORICAL / SUPERSEDED CYCLE SCORE V2 DESIGN STATUS

Research/design-only Cycle Score v2 decision completed under PROJECT_INSTRUCTIONS sections 407–417. No production scoring, thresholds, denominator, scored-indicator count, generated JSON, frontend, workflows, infrastructure, data sources, or SEC state were changed. No commit or push was performed.

- Exactly one recommendation: keep **JOLTS Hires scored**, move **JOLTS Quits to context-only**, and remove **Sahm from Cycle scoring** while retaining Sahm visibly in confirmation/Current Stress.
- Candidate v2: **12 scored indicators**, denominator **24**, current raw score **9 / 24**, normalized risk **38 / 100**, regime **Slowdown**. Labor share becomes **8 / 24 = 33.3%**, versus v1 `12 / 28 = 42.9%`.
- Points removed: Sahm `0` current points and `2` denominator points; JOLTS Quits `1` current point and `2` denominator points. Hires remains the sole scored labor-demand vote.
- Selection evidence: Hires is the more direct labor-demand measure; Quits is more worker-confidence/confirmation-like. Existing Hires/Quits correlation is `0.746` overall and `0.967` in recession months. Both thresholds remain weak/heuristic and unchanged.
- Current qualitative regime remains Slowdown; the structural change is intended to improve interpretability without an arbitrary large regime jump. Primary downside: Quits may contain distinct information and the smaller denominator increases remaining-vote influence.
- Historical limitation: no full v1/v2 composite backtest was fabricated because manual/missing LEI/ISM history prevents reconstruction. Existing timing evidence and current counterfactuals were reused.
- Future UI/migration plan is design-only: retain Sahm and both JOLTS cards, add clear scored/context role labels, preserve old history, optionally version new snapshots with `score_model_version: 2`, and keep Actions/static deployment unchanged.
- Outputs: `scripts/research_cycle_score_v2_design.py`, `research/cycle_score_v2_design.json`, `research/cycle_score_v2_design.md`.

## HISTORICAL / SUPERSEDED CYCLE SCORE V2 IMPLEMENTATION STATUS

- Exact structural diff: JOLTS Quits and Sahm now have `scored:false`, `score:null`, `risk_score:null`; both remain visible. JOLTS Hires remains scored with its existing threshold function unchanged. Current Stress continues consuming Sahm unchanged.
- v1 → v2: `14 / 28`, `10`, `36 / 100`, Slowdown → `12 / 24`, `9`, `38 / 100`, Slowdown. Labor denominator share: `42.9%` → `33.3%`.
- Additive metadata: current payload includes `score_model_version: 2`.
- History safety: `update_history` preserves an existing same-date snapshot unchanged; the existing unversioned `2026-09-12` snapshot remains v1 and was not rescored or rewritten. New dates can receive version 2. This is the smallest safe migration; mixed-version history remains explicit/documented.
- Current Stress: Sahm Confirmation remains present and enabled; no Current Stress thresholds or logic changed.
- Pipeline and validation: real-key pipeline PASS; visible indicator count unchanged; scored count 12; denominator 24; raw score 9; normalized risk 38; regime Slowdown; generated-data synchronization PASS; frontend production build PASS; threshold/source/workflow/infrastructure/SEC-state checks PASS.
- Files changed: `scripts/build_dashboard_data.py`, `frontend/src/components/IndicatorCard.tsx`, `README.md`, `CHATGPT_HANDOFF.md`, `data/current.json`, `frontend/src/data/current.json`, plus history handling preserved existing snapshots. No commit or push.
- Status: **NOT COMMITTED / NOT PUSHED**. Awaiting ChatGPT review before publication.

## HISTORICAL / SUPERSEDED CYCLE SCORE V2 IMPLEMENTATION STATUS

- Implementation status: local implementation complete; **NOT COMMITTED / NOT PUSHED** pending review.
- Exact scoring diff: `sahm-rule` and `jolts-quits` are forced context-only in the production build path (`scored:false`, `score:null`, `risk_score:null`). `jolts-hires` remains scored through the unchanged `score_jolts_hires` threshold function. Sahm remains visible and continues through the unchanged Current Stress confirmation path.
- v1 → v2: `14` scored / `10 / 28` / `36 / 100` / Slowdown → `12` scored / `9 / 24` / `38 / 100` / Slowdown. Labor denominator share: `42.9%` → `8 / 24 = 33.3%`.
- Visible indicator count: unchanged at `24`. Removed current contributions: Sahm `0` points and `2` denominator points; Quits `1` point and `2` denominator points.
- Model metadata: current payload has `score_model_version: 2`.
- History behavior: the existing unversioned `2026-09-12` v1 snapshot remains byte-for-byte preserved; the new `2026-09-13` snapshot carries `score_model_version: 2`. No old snapshot was rescored.
- Current Stress verification: `Calm / No Break`, `0 / 6` active confirmations; Sahm Confirmation remains present. No Current Stress thresholds or logic changed.
- Validation: real-key pipeline PASS; JSON fields PASS; root/frontend current and history files synchronized; frontend `npm run build` PASS; Hires threshold unchanged; no scoring threshold/source/workflow/infrastructure changes; `.env` ignored and unstaged; SEC state untouched.
- Files changed: `scripts/build_dashboard_data.py`, `frontend/src/components/IndicatorCard.tsx`, `README.md`, `data/current.json`, `data/history.json`, `frontend/src/data/current.json`, `frontend/src/data/history.json`, `CHATGPT_HANDOFF.md`.
- Commit status: **NOT COMMITTED**. Push status: **NOT PUSHED**.

## CYCLE SCORE V2 — PUBLISHED STATUS

- Commit: `eaf0a46844e7a120be46332d4ce7d0c798430d72`
- Message: `Introduce Cycle Score v2`
- Push: PASS — verified at `origin/main`.
- Final v2 baseline: 24 visible indicators; 12 scored; `9 / 24`; normalized risk `38 / 100`; regime `Slowdown`; Labor denominator share `8 / 24 = 33.3%`.
- Role changes: JOLTS Hires remains scored with unchanged threshold logic; JOLTS Quits is visible context-only; Sahm is visible confirmation/context-only for Cycle scoring and remains in Current Stress.
- History: unversioned `2026-09-12` v1 snapshot preserved unchanged; new `2026-09-13` v2 snapshot carries `score_model_version: 2`; no old snapshot was rescored.
- Current Stress: unchanged `Calm / No Break`, `0 / 6`; Sahm Confirmation remains present.
- Verification: real-key pipeline PASS; root/frontend current and history JSON synchronized; frontend production build PASS; `.env` and SEC state/cache ignored and unstaged; no threshold, source, workflow, infrastructure, or SEC changes.
- Published files: `scripts/build_dashboard_data.py`, `frontend/src/components/IndicatorCard.tsx`, `README.md`, `data/current.json`, `data/history.json`, `frontend/src/data/current.json`, `frontend/src/data/history.json`, `CHATGPT_HANDOFF.md`.
- Next phase: **Score v2 Monitoring & Stability**. No scoring redesign begins here.

Older duplicate v2 design/implementation headings in this handoff are historical audit records and are superseded by this published status. The former Historical Suggested Prompt is archived below.

## HISTORICAL / SUPERSEDED SCORE V2 MONITORING — PRE-FIX

This pre-publication monitoring record is retained for audit history. Its stale same-date conclusions are superseded by the published fix below.

- Fix files: `scripts/build_dashboard_data.py`, `README.md`, `CHATGPT_HANDOFF.md`, `data/current.json`, `frontend/src/data/current.json`. No frontend code was changed.
- Tests A–E: PASS — new-date v2 append; same-date same-version identical rerun; same-date same-version changed payload replacement without row-count growth; same-date v1/v2 conflict with byte-preserved v1 and warning; next-date append with chronological order and older rows unchanged.
- Live pipeline after fix: PASS; actual current state remains `9 / 24`, `38 / 100`, `Slowdown`. The generated data diff is limited to the legitimate `generated_at` refresh, with model/role/score fields unchanged.

- Real-key pipeline: PASS. Current payload: `score_model_version: 2`, 24 visible indicators, 12 scored, denominator `24`, raw score `9 / 24`, normalized risk `38 / 100`, regime `Slowdown`.
- Role invariants: PASS — JOLTS Hires scored; JOLTS Quits context-only with null score fields; Sahm context/confirmation-only with null Cycle score fields.
- Current Stress: PASS — `Calm / No Break`, `0 / 6`; six signals remain and Sahm Confirmation remains present.
- Historical fixture result: same-date changed v2 data stayed stale under the pre-fix policy. This is superseded; the approved fix now replaces same-version rows atomically.
- Historical design issue: same-date divergence was confirmed before implementation and is now resolved by the published rule below.
- Normalization/regime invariants: PASS — `round(total_score / max_possible_score * 100)` and existing regime bands remain unchanged.
- Frontend clarity: PASS — Hires is labeled `Cycle score · Warning`, Quits `Context`, Sahm `Confirmation · Context`; denominator copy is 24; no production-facing 14/28 text remains.
- Synchronization/build: PASS — root/frontend current and history JSON synchronized; frontend production build passed.
- `.env` and SEC state/cache: PASS — ignored and untouched. No scoring redesign or production logic change was made.
- Historical verdict: **STABLE WITH DOCUMENTATION ISSUE** — superseded by the published fix.
- Next phase: **Score v2 Monitoring & Stability**. No commit or push was performed for this monitoring task.

## ARCHIVED HISTORICAL SUGGESTED PROMPT
Here is the latest `CHATGPT_HANDOFF.md` from Codex. The Market Fragility / Stress expansion is implemented and verified locally but intentionally not committed or pushed. Review the live values, curve formulas, FINRA parser, and unchanged root score.
> **SEC research status — authoritative as of latest review:** Earlier Form 4/A conclusions below are historical and superseded where they use raw duplicate sample records or whole-accession language. The current accession-normalized status is the final SEC section 224–232 section near the end of this file. Production remains blocked.
