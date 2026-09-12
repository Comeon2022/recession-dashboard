# ChatGPT Project Handoff

## Project
US Recession Risk Dashboard

## Current Phase
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

## Publication Note

The reviewed CAPE remediation is published in `14d9ffd`; the live-source verification and push status above supersede earlier pre-publication wording in this handoff.

## Suggested Prompt for ChatGPT
Here is the latest `CHATGPT_HANDOFF.md` from Codex. The Market Fragility / Stress expansion is implemented and verified locally but intentionally not committed or pushed. Review the live values, curve formulas, FINRA parser, and unchanged root score.
