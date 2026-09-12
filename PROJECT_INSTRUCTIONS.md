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
