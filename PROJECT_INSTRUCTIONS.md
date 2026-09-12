# PROJECT_INSTRUCTIONS.md
# US Recession Risk Dashboard — Project Instructions

## 1. Goal

Build a modern, responsive web application that turns a static recession-risk infographic into a live, automatically updating macro dashboard.

The first version must run locally on Windows and use only free/open-source components.

The site should eventually be deployable for free on Cloudflare Pages.

The dashboard should:
- Show a large recession-risk gauge at the top.
- Calculate a deterministic recession-risk score from macro indicators.
- Display indicator cards grouped by category.
- Show current values, score per indicator, and a short explanation.
- Store historical score data so we can chart how risk changes over time.
- Pull public macroeconomic data automatically where possible.
- Keep the scoring logic separate from the UI.
- Avoid using an LLM to determine scores.
- Later, optionally use OpenAI only for a short natural-language interpretation of already calculated data.

The project is coordinated with ChatGPT outside the IDE. This file is the source of truth for architecture and project rules.

---

## 2. Mandatory operating rules

These rules are mandatory.

1. Keep the code simple and readable.
2. Use TypeScript for the frontend.
3. Use Python for data collection and score calculation.
4. Do not place API keys in frontend code.
5. Do not commit API keys to Git.
6. Use `.env` only for local secrets.
7. Prepare the project so secrets can later be stored in GitHub Actions secrets.
8. The scoring engine must be deterministic and rule-based.
9. The LLM must never decide whether an indicator is healthy, warning, or recessionary.
10. Every indicator must include:
   - id
   - name
   - category
   - latest value
   - display value
   - unit
   - score
   - scored / context-only flag
   - explanation
   - source
   - timestamp / observation date
11. All UI components should read from JSON data instead of hardcoded values where practical.
12. Keep a clear separation between:
   - data collection
   - normalization
   - scoring
   - generated JSON
   - frontend presentation
13. Do not over-engineer the project.
14. Prefer static hosting and scheduled data generation over a permanent backend server.
15. The app should keep working if a live source temporarily fails by retaining previous valid data when possible.
16. Do not introduce paid infrastructure services unless explicitly requested.
17. Do not change scoring thresholds silently.
18. Do not start later phases unless explicitly requested.
19. For every major task, Codex must read this file first before making changes.
20. After every meaningful task, Codex must update `CHATGPT_HANDOFF.md`.

---

## 3. Technology stack

### Frontend
- React
- Vite
- TypeScript
- Plain CSS / CSS Modules
- Recharts for charts

### Data / Automation
- Python 3.12+
- requests
- pandas
- python-dotenv

### Source Control / Automation
- Git
- GitHub
- GitHub Actions

### Hosting
- Cloudflare Pages

### Data sources
Prefer official/public sources:
- FRED
- BLS
- U.S. Treasury
- Federal Reserve
- other official agencies when required

For ISM / Conference Board / other sources:
- use official public data only if retrieval is reliable and allowed
- otherwise keep as manual/sample data
- do not scrape random websites when an official source exists

---

## 4. Architecture

Target architecture:

```text
Official macro data / sample data
            ↓
      Python collectors
            ↓
       Normalization
            ↓
   Deterministic scoring
            ↓
 current.json + history.json
            ↓
   React/Vite dashboard
            ↓
   Cloudflare Pages
```

Later, optional LLM flow:

```text
Scored macro data
      ↓
OpenAI summary generation
      ↓
summary saved into JSON
      ↓
static site
```

OpenAI must never be in the scoring path.

---

## 5. Project structure

```text
recession-dashboard/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RecessionGauge.tsx
│   │   │   ├── IndicatorCard.tsx
│   │   │   ├── IndicatorGrid.tsx
│   │   │   ├── CategoryPanel.tsx
│   │   │   ├── SummaryPanel.tsx
│   │   │   └── ScoreLegend.tsx
│   │   │
│   │   ├── data/
│   │   │   ├── current.json
│   │   │   └── history.json
│   │   │
│   │   ├── types/
│   │   │   └── dashboard.ts
│   │   │
│   │   ├── styles/
│   │   │   └── dashboard.css
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── public/
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── scripts/
│   ├── config.py
│   ├── fetch_fred.py
│   ├── fetch_bls.py
│   ├── calculate_scores.py
│   ├── build_dashboard_data.py
│   └── utils.py
│
├── data/
│   ├── current.json
│   ├── history.json
│   └── sample_raw.json
│
├── .github/
│   └── workflows/
│       └── update-data.yml
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── PROJECT_INSTRUCTIONS.md
└── CHATGPT_HANDOFF.md
```

---

## 6. Indicator model

The dashboard now supports two types of indicators:

### Scored indicators
These affect the recession-risk score.

### Context indicators
These are displayed and analyzed, but do not affect the main score.

Every indicator must have a field such as:

```json
"scored": true
```

or:

```json
"scored": false
```

This distinction must be explicit in generated JSON.

---

## 7. Initial macro indicators

### Labor

1. Payrolls
2. Unemployment / Sahm Rule
3. Initial Claims
4. JOLTS Hires
5. JOLTS Quits
6. Wage Growth

### Business

7. ISM Employment
8. ISM Activity / Orders
9. LEI

### Rates

10. Yield Curve 2s10s

The original Phase 1 / Phase 2 dashboard used these 10 indicators.

---

## 8. Housing and Mortgage expansion

Add two additional categories:

### Housing

#### Scored
1. Housing Starts
2. Building Permits
3. New Home Sales

#### Context-only
4. Months Supply
5. Case-Shiller Home Prices

### Mortgage / Household Credit

#### Scored
6. Mortgage Delinquency Rate

#### Context-only
7. 30Y Mortgage Rate
8. Mortgage Debt Service Ratio

Important:
- do not allow highly correlated housing indicators to over-dominate the overall score
- do not score every available housing series just because it exists
- context indicators should remain visible but should not inflate the recession score

The housing and mortgage categories should eventually have their own category-level status / score.

---

## 9. Why some housing indicators are context-only

Do not use a simplistic rule such as:

```text
Mortgage rate > X% = recession
```

A high mortgage rate alone is not sufficient evidence of recession.

Context indicators such as:
- 30Y Mortgage Rate
- Case-Shiller Home Prices
- Months Supply
- Mortgage Debt Service Ratio

should help explain:
- affordability
- financing stress
- housing-market cooling
- household pressure

but should not automatically add recession points unless a validated scoring rule is explicitly approved.

---

## 10. Future affordability metric

Prepare the architecture so we can later add:

```text
Housing Affordability Stress
```

Potential inputs:
- mortgage rate
- median home price
- median household income

This metric is NOT yet part of the official scoring engine.

Do not implement or score it without a separate task.

---

## 11. Scoring system

For individual scored indicators:

- `0 = Healthy`
- `1 = Warning`
- `2 = Recessionary`

All score functions live in Python.

Example:

```python
def score_initial_claims(value: float) -> int:
    if value < 220_000:
        return 0
    elif value < 250_000:
        return 1
    return 2
```

Example:

```python
def score_sahm(value: float) -> int:
    if value < 0.25:
        return 0
    elif value < 0.50:
        return 1
    return 2
```

Thresholds must:
- be explicit
- be commented
- be reviewable
- be marked provisional when not finalized

Never hide uncertainty.

---

## 12. Main risk score normalization

The project originally used a raw score such as:

```text
7 / 20
```

As the project grows, the primary dashboard score should migrate to a normalized 0–100 scale.

Formula:

```python
risk_score = round(
    total_score / max_possible_score * 100
)
```

Store BOTH:
- raw total score
- max possible score
- normalized risk score

Example:

```json
{
  "total_score": 11,
  "max_score": 28,
  "risk_score": 39
}
```

The gauge should eventually use the normalized `risk_score`.

Do not delete the raw score because it is useful for transparency and debugging.

---

## 13. Risk regime mapping

First-pass normalized mapping:

```text
0–25   = Healthy
26–50  = Slowdown
51–70  = Elevated Risk
71–100 = Recessionary
```

Store this mapping in code.

Example:

```python
def get_regime_from_risk_score(risk_score: int) -> str:
    if risk_score <= 25:
        return "Healthy"
    elif risk_score <= 50:
        return "Slowdown"
    elif risk_score <= 70:
        return "Elevated Risk"
    return "Recessionary"
```

This mapping is provisional and may be refined after historical backtesting.

Do not change it silently.

---

## 14. Category-level scores

The architecture should support category-level summaries.

Example:

```text
Labor
Business
Rates
Housing
Mortgage Stress
```

Each category may eventually expose:
- raw score
- max score
- normalized category risk
- regime / label

Example:

```json
{
  "name": "Housing",
  "score": 4,
  "max_score": 6,
  "risk_score": 67,
  "regime": "Elevated Risk"
}
```

Only scored indicators count toward category scores.

Context indicators do not.

---

## 15. JSON schema

`data/current.json` should evolve toward:

```json
{
  "generated_at": "2026-09-12T09:00:00Z",
  "country": "United States",
  "total_score": 11,
  "max_score": 28,
  "risk_score": 39,
  "regime": "Slowdown",
  "summary": "Labor-market weakness is visible, but the economy is not yet in a full recession regime.",
  "categories": [
    {
      "id": "labor",
      "name": "Labor",
      "score": 7,
      "max_score": 12,
      "risk_score": 58
    }
  ],
  "indicators": [
    {
      "id": "payrolls",
      "name": "Payrolls",
      "category": "Labor",
      "value": 162000,
      "display_value": "August +162K | 12M avg +31K",
      "unit": "jobs",
      "score": 1,
      "scored": true,
      "explanation": "Weak beneath the headline number",
      "source": "BLS",
      "observation_date": "2026-08-01"
    }
  ]
}
```

Context-only indicator example:

```json
{
  "id": "mortgage_rate_30y",
  "name": "30Y Mortgage Rate",
  "category": "Mortgage",
  "value": 6.5,
  "display_value": "6.5%",
  "unit": "percent",
  "score": null,
  "scored": false,
  "explanation": "Financing-cost context",
  "source": "FRED",
  "observation_date": "2026-09-01"
}
```

---

## 16. History file

`data/history.json` should contain:

```json
{
  "date": "2026-09-12",
  "total_score": 11,
  "max_score": 28,
  "risk_score": 39,
  "regime": "Slowdown"
}
```

Rules:
- one record per date
- replace same-date entry
- sort by date
- keep normalized risk score for historical comparison even if total number of indicators changes

This is an important reason for using 0–100 normalization.

---

## 17. Frontend visual direction

Use a visual style inspired by clean Google Cloud architecture diagrams.

### Main direction
- light gray / white background
- dark navy typography
- Google-style blue as primary accent
- green for healthy
- yellow for warning
- red for recessionary
- rounded white cards
- thin gray borders
- subtle shadows
- clean vector icons
- responsive layout

### Gauge
Top of dashboard:
- large semicircular gauge
- green left
- yellow middle
- red right
- needle uses normalized risk score
- smooth page-load animation
- raw score can be shown underneath
- regime clearly displayed

Gauge labels:
- Healthy
- Slowdown
- Recession

### Indicator cards
Each card:
- icon
- indicator title
- current display value
- short explanation
- source
- observation date
- score badge if scored
- `Context` badge if context-only

Desktop:
- two-column layout

Mobile:
- one-column layout

---

## 18. Hebrew support

The UI must remain easy to localize.

Support:
- English
- Hebrew

Do not hardcode layouts that break RTL.

Use:

```css
direction: rtl;
```

where appropriate.

Example Hebrew labels:

```text
מדד קרבה למיתון
ציון סיכון
מצב נוכחי
בריא
האטה
סיכון מוגבר
מיתון
דיור
שוק המשכנתאות
תמונה כוללת
```

---

## 19. Completed phase — Phase 1

Phase 1:
- React + Vite + TypeScript frontend
- gauge
- summary
- legend
- 10 indicator cards
- sample JSON
- responsive layout

Phase 1 was completed and verified.

Do not rebuild it from scratch.

---

## 20. Completed phase — Phase 2

Phase 2:
- Python sample scoring engine
- deterministic scoring
- `sample_raw.json`
- generated `current.json`
- generated `history.json`
- frontend synchronization
- build verification

Phase 2 was completed and verified.

Do not replace the scoring pipeline with frontend logic.

---

## 21. Phase 2.5 — Housing / Mortgage schema expansion

Before Phase 3 live APIs, extend the existing schema and frontend support for:
- Housing category
- Mortgage / Household Credit category
- scored vs context-only indicators
- category-level scoring support
- raw + normalized 0–100 score fields

Use sample/manual values only during this phase.

Do not connect FRED/BLS yet unless explicitly requested in the task.

Success criteria:
- existing 10 indicators still work
- new housing/mortgage indicators render
- scored/context distinction works
- raw score and normalized score both exist
- history supports normalized score
- Python pipeline succeeds
- frontend build succeeds
- `CHATGPT_HANDOFF.md` updated

---

## 22. Phase 3 — FRED integration

After schema expansion is stable:

Add FRED integration.

Environment variable:

```text
FRED_API_KEY=
```

Add to `.env.example`.

Do not commit `.env`.

Implement:

```python
def fetch_fred_series(series_id: str, api_key: str):
    ...
```

Requirements:
- request latest observations
- timeout handling
- readable errors
- normalize response
- keep previous valid value if fetch fails
- do not blank dashboard on source failure

FRED should be used for any reliable series available there.

Examples likely to be sourced from FRED:
- unemployment
- Sahm Rule
- initial claims
- payroll-related series
- wage growth series
- Treasury yields
- yield curve
- housing starts
- building permits
- new home sales
- months supply
- Case-Shiller
- 30Y mortgage rate
- selected household/mortgage stress series

Exact series IDs must be reviewed before finalizing.

---

## 23. Phase 4 — BLS direct integration

Use BLS direct API only where it is more appropriate/reliable than FRED.

Implement:

```python
def fetch_bls_series(series_ids: list[str]):
    ...
```

Normalize all external data into the same internal structure before scoring.

---

## 24. Data-source policy

Every indicator must visibly expose its source.

Examples:
- BLS
- FRED
- Federal Reserve
- U.S. Treasury
- Manual

Never silently mix sources.

If live data is unavailable:
- preserve previous valid data when possible
- mark data status
- show a warning

---

## 25. Error handling

Python should:
- catch HTTP failures
- log failed series
- retain previous valid values if possible
- produce `data_status`
- include warnings

Example:

```json
{
  "data_status": "partial",
  "warnings": [
    "ISM Services unavailable; previous value retained."
  ]
}
```

Frontend:
- show a small warning banner if `data_status != "ok"`

---

## 26. Git setup

`.gitignore` should include:

```text
node_modules/
dist/
.env
.venv/
__pycache__/
*.pyc
.vscode/
```

Do not ignore:
- `.env.example`
- generated sample JSON
- GitHub workflow files
- `PROJECT_INSTRUCTIONS.md`
- `CHATGPT_HANDOFF.md`

---

## 27. Python virtual environment

From project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Initial requirements:

```text
requests
pandas
python-dotenv
```

---

## 28. Frontend commands

From project root:

```powershell
cd frontend
npm install
npm run build
npm run dev
```

Do not add large UI frameworks unless explicitly approved.

Avoid by default:
- Material UI
- Bootstrap
- Tailwind

---

## 29. README requirements

README should explain:

1. Project purpose
2. Architecture
3. Requirements
4. Local setup
5. Data rebuild
6. Environment variables
7. Scoring model
8. Category model
9. Scored vs context indicators
10. Deployment plan

---

## 30. GitHub Actions — future phase

Future workflow:

`.github/workflows/update-data.yml`

Expected behavior:
- scheduled run
- Python data update
- generated JSON changes
- commit/push
- Cloudflare Pages redeploy

Initial target:

```yaml
schedule:
  - cron: "0 6 * * *"
```

One daily update is sufficient initially.

Do not enable automation before live data pipeline is stable.

---

## 31. Cloudflare Pages — future deployment

Target:
Cloudflare Pages

Build settings:

```text
Root directory: frontend
Build command: npm run build
Output directory: dist
```

Production site should remain static.

No permanent Node server should be required.

---

## 32. OpenAI / LLM policy

Do not add OpenAI integration until explicitly requested.

When later added:
- LLM summarizes already-scored data
- LLM never changes score
- LLM never changes thresholds
- API key never goes into frontend
- OpenAI call happens in Python or GitHub Action
- generated summary saved into JSON
- do not call OpenAI on every page load

ChatGPT subscription and OpenAI API are separate; the project must assume API billing is separate if/when enabled.

---

## 33. Codex task protocol

This project is built in VS Code using the official OpenAI Codex extension.

For every MAJOR task:

1. Read `PROJECT_INSTRUCTIONS.md` first.
2. Treat it as the project source of truth.
3. Execute only the requested task.
4. Do not start future phases.
5. Do not change unrelated architecture.
6. Do not silently change scoring thresholds.
7. Do not add unnecessary dependencies.
8. Keep Windows PowerShell compatibility.
9. Run appropriate verification.
10. Update `CHATGPT_HANDOFF.md` before reporting completion.

For tiny cosmetic changes, reading the full file is optional, but all architectural/project rules still apply.

---

## 34. CHATGPT_HANDOFF.md

After every meaningful work session, Codex must create or update:

```text
CHATGPT_HANDOFF.md
```

It must never contain:
- API keys
- tokens
- passwords
- `.env` secret values

Required structure:

```markdown
# ChatGPT Project Handoff

## Project
US Recession Risk Dashboard

## Current Phase
...

## Status
Completed / In Progress / Blocked

## What Was Done
- ...

## Files Created or Changed
- ...

## Current Architecture
...

## Current Data / Score State
- Total score: ...
- Max score: ...
- Normalized risk score: ...
- Regime: ...
- Indicators implemented: ...
- Live indicators: ...
- Manual/sample indicators: ...

## Commands to Run Locally

```powershell
...
```

## Verification Performed
- Python pipeline: PASS / FAIL
- npm build: PASS / FAIL
- dev server: PASS / NOT TESTED

## Issues / Warnings
- ...

## Important Decisions
- ...

## Next Recommended Step
One exact next step.

## Suggested Prompt for ChatGPT
A short prompt the user can paste to ChatGPT with this file.
```

Update the handoff:
- after completing a phase
- after major refactor
- after new source integration
- after scoring changes
- after important bug fix
- after a failed task needing outside guidance
- before telling the user a meaningful task is complete

Keep only the latest state in the main handoff file.

---

## 35. Current next task

The next intended task is Phase 2.5:

> Read `PROJECT_INSTRUCTIONS.md` first and follow it as the source of truth. Extend the data model and frontend to support Housing and Mortgage / Household Credit categories. Add Housing Starts, Building Permits, New Home Sales, Months Supply, Case-Shiller Home Prices, 30Y Mortgage Rate, Mortgage Delinquency Rate, and Mortgage Debt Service Ratio. Only Housing Starts, Building Permits, New Home Sales, and Mortgage Delinquency should affect the recession score initially; the others are context-only. Add category-level score support and migrate the main dashboard model to include both raw score and normalized 0–100 risk score. Keep all new indicators on sample/manual data for now. Do not connect FRED, BLS, OpenAI, or external APIs yet. Preserve existing behavior, run the Python pipeline, run `npm run build`, and update `CHATGPT_HANDOFF.md`.

---

## 36. Project philosophy

This is not a prediction engine.

It is a transparent macro monitoring dashboard.

The user should always be able to see:
- the raw indicator value
- whether the indicator is scored or context-only
- the score
- the source
- the threshold logic
- the observation date
- the historical direction

The system should favor:
- transparency
- reproducibility
- simplicity
- traceability
- official data
- deterministic logic

over complexity.


---

## 37. Phase sequencing correction after Phase 3 handoff review

A later Codex run completed part of Phase 3 before the planned Phase 2.5 Housing / Mortgage schema expansion.

Current repository state reported by Codex:
- Phase 1 complete
- Phase 2 complete
- partial Phase 3 FRED integration complete for the original 10-indicator model
- Housing / Mortgage schema expansion has NOT yet been completed
- BLS direct integration has NOT started
- OpenAI integration has NOT started

Do not discard the completed FRED client. Instead, the next task must reconcile the project with the intended architecture:
1. audit/correct current FRED mappings
2. complete Housing / Mortgage schema expansion
3. preserve the existing FRED client and fallback behavior
4. then extend FRED to the new eligible indicators

---

## 38. FRED mapping audit decisions

The following FRED mappings are approved or preferred:

### Existing / approved
- Unemployment Rate: `UNRATE`
- Sahm Rule Recession Indicator: `SAHMREALTIME`
- Initial Claims: `ICSA`
- Average Hourly Earnings: `CES0500000003`, with YoY growth calculated in Python
- 10Y minus 2Y Treasury spread: `T10Y2Y`

### Payrolls should become FRED-live
Use:
- `PAYEMS` — All Employees, Total Nonfarm

Payroll growth should be derived from monthly differences in `PAYEMS`.
The dashboard may show:
- latest monthly change
- optional rolling 3-month / 12-month average

Do not leave Payrolls manual if `PAYEMS` is available and reliable.

### JOLTS Hires should become FRED-live
Use:
- `JTSHIR` — Hires: Total Nonfarm, Rate, Seasonally Adjusted

### JOLTS Quits should become FRED-live
Use:
- `JTSQUR` — Quits: Total Nonfarm, Rate, Seasonally Adjusted

These series are available on FRED and should not remain manual-only.

### LEI correction
Do NOT use `USSLIND` as the current Conference Board LEI.

`USSLIND` is the Philadelphia Fed's historical "Leading Index for the United States" and the available FRED series is stale / not a valid current replacement for the Conference Board LEI.

Until a reliable current official/public source for the intended LEI is integrated:
- keep the dashboard's LEI indicator as manual/sample
- clearly mark its source as Manual / Conference Board data input if entered manually
- do not silently substitute another leading index
- do not calculate 12-month growth from `USSLIND` for the LEI card

A different leading indicator such as CFNAI may be added later as a separate indicator, but must not be renamed "LEI".

---

## 39. Revised current live/manual split for original indicators

Preferred FRED-live capable indicators:

1. Payrolls — `PAYEMS`, monthly difference calculated in Python
2. Unemployment / Sahm Rule — `UNRATE` + `SAHMREALTIME`
3. Initial Claims — `ICSA`
4. JOLTS Hires — `JTSHIR`
5. JOLTS Quits — `JTSQUR`
6. Wage Growth — `CES0500000003`, YoY calculation
7. Yield Curve 2s10s — `T10Y2Y`

Remain manual/sample for now:
8. ISM Employment
9. ISM Activity / Orders
10. LEI

Do not add BLS direct integration merely to fetch a series already available cleanly via FRED.

---

## 40. Next required Codex task after Phase 3 review

The next major task should NOT be Phase 4 BLS yet.

Use this task:

> Read `PROJECT_INSTRUCTIONS.md` first and treat it as the source of truth. Reconcile the current partial Phase 3 implementation with the updated architecture. First audit and correct the FRED mappings: add live Payrolls from `PAYEMS`, add live JOLTS Hires from `JTSHIR`, add live JOLTS Quits from `JTSQUR`, keep `UNRATE` + `SAHMREALTIME`, `ICSA`, `CES0500000003`, and `T10Y2Y`, and remove `USSLIND` as the live source for the dashboard LEI. LEI must return to manual/sample mode until a valid current source is approved. Then complete the planned Housing and Mortgage / Household Credit schema expansion from Phase 2.5: add Housing Starts, Building Permits, New Home Sales, Months Supply, Case-Shiller Home Prices, 30Y Mortgage Rate, Mortgage Delinquency Rate, and Mortgage Debt Service Ratio. Only Housing Starts, Building Permits, New Home Sales, and Mortgage Delinquency affect the main risk score initially; the others are context-only. Add scored/context flags, category-level score support, and raw plus normalized 0–100 risk score fields. Preserve existing fallback/error handling. For this task, use sample/manual values for the new Housing/Mortgage indicators unless the existing FRED client can be extended cleanly without changing the scoring design; if live mappings are added, document each exact series ID. Do not add BLS direct integration or OpenAI. Run the Python pipeline, validate generated JSON, run `npm run build`, and update `CHATGPT_HANDOFF.md`.



---

## 41. Current repository state after reconciliation

Latest verified state:

- Phase 1 complete
- Phase 2 complete
- Phase 2.5 Housing / Mortgage schema expansion complete
- Phase 3 FRED reconciliation complete for the approved original indicators
- BLS direct integration not started
- OpenAI integration not started

Current model:
- 18 indicators total
- 14 scored indicators
- 4 context-only indicators
- 5 categories
- raw score retained
- normalized 0–100 risk score retained
- category-level scores supported
- context indicators do not inflate the main score

Current sample/fallback state:
- raw score: 11 / 28
- normalized risk score: 39 / 100
- regime: Slowdown

Approved FRED-capable mappings currently implemented:
- Payrolls — `PAYEMS`, monthly difference
- Unemployment — `UNRATE`
- Sahm Rule — `SAHMREALTIME`
- Initial Claims — `ICSA`
- JOLTS Hires — `JTSHIR`
- JOLTS Quits — `JTSQUR`
- Wage Growth — `CES0500000003`, 12-month growth
- Yield Curve 2s10s — `T10Y2Y`

Manual/sample for now:
- LEI
- ISM Employment
- ISM Activity / Orders
- Housing Starts
- Building Permits
- New Home Sales
- Months Supply
- Case-Shiller Home Prices
- 30Y Mortgage Rate
- Mortgage Delinquency Rate
- Mortgage Debt Service Ratio

The fallback path and frontend build have been verified. Successful live FRED responses have not yet been validated with a real API key.

---

## 42. Next required task — validate live FRED before adding more sources

Before adding Housing/Mortgage live mappings or BLS integration:

1. Configure a valid local `FRED_API_KEY`.
2. Run the existing pipeline.
3. Verify all approved live series return sensible current observations.
4. Confirm transformations:
   - PAYEMS monthly difference
   - CES0500000003 YoY growth
5. Confirm observation dates are current and not stale.
6. Confirm fallback values are not being used silently when live data succeeds.
7. Confirm generated JSON source labels correctly distinguish FRED vs Manual.
8. Confirm normalized total/category scores remain internally consistent.
9. Run `npm run build`.
10. Update `CHATGPT_HANDOFF.md`.

Do not add BLS direct integration yet.

Do not add OpenAI yet.

Do not add live Housing/Mortgage mappings until the existing live FRED path is validated with a real key.

Recommended Codex task:

> Read `PROJECT_INSTRUCTIONS.md` first and treat it as the source of truth. Validate the existing Phase 3 FRED integration using the locally configured `FRED_API_KEY`. Do not add new indicators, new data sources, BLS, or OpenAI. Run the Python pipeline with the real key and verify each approved FRED-backed indicator: `PAYEMS`, `UNRATE`, `SAHMREALTIME`, `ICSA`, `JTSHIR`, `JTSQUR`, `CES0500000003`, and `T10Y2Y`. Check that observation dates are current, transformations are correct, live values replace sample fallback values, sources are labeled correctly, and scores remain consistent. Then run `npm run build` and update `CHATGPT_HANDOFF.md` with a table of each live series, latest observation date, normalized value used by the dashboard, and PASS/FAIL status. Do not start any later phase.


---

## 43. Phase 3 live validation completed

The real-key FRED validation has now been completed successfully.

Verified live FRED series:
- `PAYEMS` — Payrolls monthly difference
- `UNRATE` — Unemployment
- `SAHMREALTIME` — Sahm Rule
- `ICSA` — Initial Claims
- `JTSHIR` — JOLTS Hires
- `JTSQUR` — JOLTS Quits
- `CES0500000003` — Wage Growth, 12-month growth
- `T10Y2Y` — Yield Curve 2s10s

Verified current repository state:
- 18 indicators
- 14 scored
- 4 context-only
- 7 live dashboard indicators backed by 8 FRED series
- 11 manual/sample indicators
- raw score: 11 / 28
- normalized risk score: 39 / 100
- regime: Slowdown
- `data_status: ok`
- frontend build passes

The FRED key is local-only and must remain excluded from Git.

---

## 44. Approved Housing / Mortgage FRED mappings

The next approved live-data expansion is Housing and Mortgage / Household Credit.

### Housing — scored

#### Housing Starts
Use:
- `HOUST`
- New Privately-Owned Housing Units Started: Total Units
- Monthly
- Thousands of Units, Seasonally Adjusted Annual Rate

Normalize into the same unit expected by the existing scoring function.
If the scoring function expects absolute units, multiply FRED thousands by 1,000.
Do not silently change scoring thresholds.

#### Building Permits
Use:
- `PERMIT`
- New Privately-Owned Housing Units Authorized in Permit-Issuing Places: Total Units
- Monthly
- Thousands of Units, Seasonally Adjusted Annual Rate

Normalize to the same unit convention used by the scoring function.

#### New Home Sales
Use:
- `HSN1F`
- New One Family Houses Sold: United States
- Monthly
- Thousands, Seasonally Adjusted Annual Rate

Normalize into the same unit expected by the existing scoring function.

### Housing — context-only

#### Months Supply
Use:
- `MSACSR`
- Monthly Supply of New Houses in the United States
- Monthly
- Months' Supply, Seasonally Adjusted

This remains context-only.

#### Home Prices
Do NOT use Case-Shiller `CSUSHPINSA` in the public dashboard by default.

Reason:
- FRED marks this S&P-sourced series as copyrighted / pre-approval required
- this project is intended to be a public, free website

Preferred public-domain replacement:
- `USSTHPI`
- All-Transactions House Price Index for the United States
- Source: Federal Housing Finance Agency
- Quarterly
- Public Domain: Citation Requested

Use `USSTHPI` as the default Home Prices context indicator unless separately approved otherwise.

Update the UI label from:
`Case-Shiller Home Prices`

to:
`FHFA Home Price Index`

or:
`U.S. Home Prices (FHFA)`

Update source and description accordingly.

### Mortgage / Household Credit — scored

#### Mortgage Delinquency Rate
Use:
- `DRSFRMACBS`
- Delinquency Rate on Single-Family Residential Mortgages, Booked in Domestic Offices, All Commercial Banks
- Quarterly
- Percent, Seasonally Adjusted
- Source: Board of Governors of the Federal Reserve System

This is a scored indicator.

Do not treat the slower quarterly publication cadence as a data error merely because the observation date is older than monthly indicators.
Recency validation must be frequency-aware.

### Mortgage / Household Credit — context-only

#### 30Y Mortgage Rate
Use:
- `MORTGAGE30US`
- 30-Year Fixed Rate Mortgage Average in the United States
- Weekly
- Percent

Context-only.

#### Mortgage Debt Service Ratio
Use:
- `MDSP`
- Mortgage Debt Service Payments as a Percent of Disposable Personal Income
- Quarterly
- Percent, Seasonally Adjusted

Context-only.

---

## 45. Frequency-aware recency validation

Recency checks must account for release frequency.

Do not use one universal stale-data threshold.

Suggested first-pass validation windows:
- Daily / weekly series: warn if materially beyond expected weekly release cadence
- Monthly series: allow normal publication lags of roughly 1–3 months depending on the series
- Quarterly series: allow normal quarterly publication lag; do not classify as stale solely because it is several months old

The code should preserve:
- observation date
- frequency where practical
- source

Do not silently reject a valid quarterly mortgage series because a weekly indicator is newer.

---

## 46. Next required task — live Housing / Mortgage integration

The next task should extend the already validated FRED pipeline to the approved Housing / Mortgage mappings.

Recommended Codex task:

> Read `PROJECT_INSTRUCTIONS.md` first and treat it as the source of truth. Extend the existing validated FRED integration to the approved Housing and Mortgage / Household Credit indicators only. Add live mappings for `HOUST` (Housing Starts), `PERMIT` (Building Permits), `HSN1F` (New Home Sales), `MSACSR` (Months Supply), `USSTHPI` (FHFA Home Price Index context indicator replacing the planned Case-Shiller public-dashboard indicator), `MORTGAGE30US` (30Y Mortgage Rate), `DRSFRMACBS` (Mortgage Delinquency Rate), and `MDSP` (Mortgage Debt Service Ratio). Preserve the existing scored/context-only rules: Housing Starts, Building Permits, New Home Sales, and Mortgage Delinquency affect the score; Months Supply, FHFA Home Price Index, 30Y Mortgage Rate, and Mortgage Debt Service Ratio are context-only. Normalize FRED units into the existing schema/scoring units without changing thresholds. Make recency validation frequency-aware so quarterly series are not falsely rejected as stale. Keep all existing fallback/error handling and the validated original FRED integrations unchanged. Do not add BLS direct integration or OpenAI. Run the real-key Python pipeline, validate every new live series and observation date, verify category/root scores, run `npm run build`, and update `CHATGPT_HANDOFF.md` with a live-series validation table and exact series IDs.


---

## 47. Housing / Mortgage live integration completed

The approved Housing and Mortgage / Household Credit FRED expansion has now been completed and verified with a real local FRED API key.

Current verified repository state:
- 18 indicators total
- 14 scored indicators
- 4 context-only indicators
- 15 live FRED-backed dashboard indicators
- 3 manual/sample indicators
- raw score: 10 / 28
- normalized risk score: 36 / 100
- regime: Slowdown
- `data_status: ok`
- frontend production build passes

Verified Housing / Mortgage live mappings:
- `HOUST` — Housing Starts — scored
- `PERMIT` — Building Permits — scored
- `HSN1F` — New Home Sales — scored
- `MSACSR` — Months Supply — context-only
- `USSTHPI` — FHFA Home Price Index — context-only
- `MORTGAGE30US` — 30Y Mortgage Rate — context-only
- `DRSFRMACBS` — Mortgage Delinquency Rate — scored
- `MDSP` — Mortgage Debt Service Ratio — context-only

Frequency-aware recency validation is active:
- daily: 14 days
- weekly: 45 days
- monthly: 120 days
- quarterly: 450 days

Current category scores:
- Labor: 4 / 12, normalized risk 33
- Business: 2 / 6, normalized risk 33
- Rates: 1 / 2, normalized risk 50
- Housing: 3 / 6, normalized risk 50
- Mortgage / Household Credit: 0 / 2, normalized risk 0

The three remaining manual/sample indicators are:
- ISM Employment
- ISM Activity / Orders
- LEI

Do not force unofficial or licensing-problematic live replacements for these three indicators.

---

## 48. Next priority — automate updates and deploy the public site

The core live-data pipeline is now sufficiently mature to automate and deploy before adding more data sources.

Priority order:
1. GitHub Actions scheduled data refresh
2. automatic commit of generated JSON only when data changes
3. Cloudflare Pages deployment
4. custom domain later if desired
5. only after deployment is stable, consider additional sources or OpenAI summaries

Do NOT add BLS direct integration or OpenAI before the automated deployment path is stable unless explicitly requested.

---

## 49. GitHub Actions requirements

Create:

```text
.github/workflows/update-data.yml
```

The workflow should:

1. Run on:
   - `workflow_dispatch`
   - scheduled cron
2. Checkout repository
3. Set up Python
4. Install Python dependencies
5. Load `FRED_API_KEY` from GitHub Actions Secrets
6. Run:

```powershell
python scripts/build_dashboard_data.py
```

7. Verify generated JSON exists and is valid
8. Optionally run frontend build as a validation step
9. Commit and push only if tracked generated files changed
10. Never expose the FRED key in logs

Recommended scheduled cadence:

```yaml
schedule:
  - cron: "0 14 * * 1-5"
```

Meaning:
- once per weekday
- 14:00 UTC
- chosen to catch most U.S. morning macro releases after publication / FRED ingestion

A manual `workflow_dispatch` trigger must also exist so updates can be run on demand.

If future experience shows FRED ingestion occurs later for specific releases, the schedule may be adjusted without changing architecture.

---

## 50. GitHub Actions secret

The repository must use:

```text
FRED_API_KEY
```

as a GitHub Actions repository secret.

Never commit the key.

Never place the key in:
- frontend code
- JSON output
- README
- `PROJECT_INSTRUCTIONS.md`
- `CHATGPT_HANDOFF.md`
- workflow logs

Local `.env` remains for local development only.

---

## 51. Generated files to commit from automation

The workflow may commit updates to:

```text
data/current.json
data/history.json
frontend/src/data/current.json
frontend/src/data/history.json
```

Do not commit:
- `.env`
- virtual environments
- `node_modules`
- temporary logs

Commit only when content changed.

Suggested automated commit message:

```text
chore(data): refresh macro dashboard
```

---

## 52. Cloudflare Pages deployment

Target:
Cloudflare Pages

Repository:
GitHub `recession-dashboard`

Build configuration:

```text
Root directory: frontend
Build command: npm run build
Output directory: dist
```

Cloudflare Pages should redeploy automatically whenever GitHub receives a commit that changes the generated dashboard data or frontend code.

No permanent backend server is required.

The production site must remain a static deployment.

---

## 53. FRED attribution requirement

Before public deployment, add a small footer / About attribution indicating that the site uses FRED data.

The attribution should clearly state that:
- data is obtained through the FRED API / Federal Reserve Bank of St. Louis data service
- the dashboard is not affiliated with, endorsed by, or sponsored by the Federal Reserve Bank of St. Louis

Also preserve per-indicator source labels already present in the dashboard.

Do not claim all FRED-hosted series are owned by FRED; individual indicator sources should remain visible where known.

---

## 54. Deployment validation checklist

Before calling the automated deployment complete, verify:

### GitHub Actions
- manual workflow run succeeds
- scheduled workflow syntax validates
- `FRED_API_KEY` is read from GitHub Secret
- no secret appears in logs
- Python pipeline succeeds
- generated JSON validates
- no commit is created when data is unchanged
- commit/push succeeds when data changes

### Frontend
- `npm run build` succeeds in CI
- normalized gauge renders from generated live data
- all 18 indicators render
- context badges render
- warning banner behavior remains correct
- sources and observation dates remain visible

### Cloudflare Pages
- GitHub repository connected
- build succeeds
- site receives a `.pages.dev` URL
- HTTPS works
- latest committed live JSON is visible on the deployed site
- new data commit triggers a new deployment

---

## 55. Next required Codex task — GitHub Actions automation only

Recommended Codex task:

> Read `PROJECT_INSTRUCTIONS.md` first and treat it as the source of truth. Implement the next deployment-preparation step only: create and validate `.github/workflows/update-data.yml` for automated FRED data refresh. The workflow must support both `workflow_dispatch` and a weekday schedule at 14:00 UTC, use the repository secret `FRED_API_KEY`, run the existing Python pipeline, validate the generated JSON, run the frontend production build, and commit/push only the generated data files when they actually change. Do not add Cloudflare-specific files yet, do not add BLS, do not add OpenAI, do not change scoring thresholds, and do not add or remove indicators. Never expose the API key. Update README with the GitHub Actions secret/setup instructions, run any local syntax/static checks possible, and update `CHATGPT_HANDOFF.md` when finished. Clearly state that the workflow cannot be fully live-tested until the user adds the GitHub repository secret and manually runs it from GitHub Actions.
