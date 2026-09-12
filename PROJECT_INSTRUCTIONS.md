# PROJECT_INSTRUCTIONS.md
# US Recession Risk Dashboard — Project Instructions

## 1. Goal

Build a modern, responsive web application that turns a static recession-risk infographic into a live, automatically updating macro dashboard.

The first version must run locally on Windows and use only free/open-source components.

The site should eventually be deployable for free on Cloudflare Pages.

The dashboard should:
- Show a large recession-risk gauge at the top.
- Calculate a deterministic recession-risk score from 10 indicators.
- Display 10 indicator cards.
- Show current values, score per indicator, and a short explanation.
- Store a small historical series so we can later chart how the total score changes over time.
- Pull public macroeconomic data automatically where possible.
- Keep the scoring logic separate from the UI.
- Avoid using an LLM to determine scores.
- Later, optionally use OpenAI only for a short natural-language interpretation of already calculated data.

---

## 2. Important development rules

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
   - unit
   - score
   - explanation
   - source
   - timestamp / observation date
11. All UI components should read from JSON data instead of hardcoded values where practical.
12. Keep a clear separation between:
   - data collection
   - scoring
   - generated JSON
   - frontend presentation
13. Do not over-engineer the project.
14. Prefer static hosting and scheduled data generation over a permanent backend server.
15. The initial version should work even if no external API keys are configured, by using local sample data.

---

## 3. Technology stack

### Frontend
- React
- Vite
- TypeScript
- CSS Modules or plain CSS
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
Prefer:
- FRED
- BLS
- U.S. Treasury
- Federal Reserve
- Conference Board only if legally/publicly accessible without scraping restrictions
- ISM only if public official data can be retrieved reliably

If a series is not freely available from an official API, keep it as a manual/simulated data source in the first version and clearly mark it.

---

## 4. Initial project structure

Create this structure:

```text
recession-dashboard/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RecessionGauge.tsx
│   │   │   ├── IndicatorCard.tsx
│   │   │   ├── IndicatorGrid.tsx
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
└── PROJECT_INSTRUCTIONS.md
```

---

## 5. Initial indicators

Use exactly these 10 indicators in version 1.

### 1. Payrolls
Display name:
`Payrolls`

Initial sample:
`162K+ in August, 12-month average: 31K+`

Initial score:
`1`

Initial explanation:
`Weak beneath the headline number`

### 2. Unemployment / Sahm Rule
Display name:
`Unemployment / Sahm Rule`

Initial sample:
`Unemployment 4.1% | Sahm = -0.07`

Initial score:
`0`

Initial explanation:
`Still far from the +0.50 recession trigger`

### 3. Initial Claims
Display name:
`Initial Claims`

Initial sample:
`206K`

Initial score:
`0`

Initial explanation:
`No broad layoff wave yet`

### 4. JOLTS Hires
Display name:
`JOLTS Hires`

Initial sample:
`3.2%`

Initial score:
`1`

Initial explanation:
`Hiring is weak`

### 5. JOLTS Quits
Display name:
`JOLTS Quits`

Initial sample:
`1.9%`

Initial score:
`1`

Initial explanation:
`Workers are less confident about changing jobs`

### 6. Wage Growth
Display name:
`Wage Growth`

Initial sample:
`+3.1% YoY`

Initial score:
`1`

Initial explanation:
`No unusual wage pressure despite constrained labor supply`

### 7. ISM Employment
Display name:
`ISM Employment`

Initial sample:
`Services 47.8 | Manufacturing 51.2`

Initial score:
`1`

Initial explanation:
`Weakness in services, but not broad-based`

### 8. ISM Activity / Orders
Display name:
`ISM Activity / Orders`

Initial sample:
`Services 55.4 | Manufacturing 54.6`

Initial score:
`0`

Initial explanation:
`Business activity is still expanding`

### 9. Yield Curve 2s10s
Display name:
`Yield Curve 2s10s`

Initial sample:
`~+33 bp`

Initial score:
`1`

Initial explanation:
`Curve is positive, but partly because long yields remain elevated`

### 10. LEI
Display name:
`LEI`

Initial sample:
`July +0.2% | 6 months +0.2%`

Initial score:
`0`

Initial explanation:
`Not currently signaling a fresh downturn`

---

## 6. Scoring system

Use:
- `0 = Healthy`
- `1 = Warning`
- `2 = Recessionary`

Maximum total:
`20`

Initial total:
`7 / 20`

Initial regime:
`Slowdown`

Do not infer scores from visual styling.

Scores must be calculated in Python from explicit threshold functions.

Each scoring function must have:
- input
- thresholds
- returned score
- comments explaining why

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

For indicators where thresholds are not yet finalized:
- use provisional rules
- clearly mark them with comments
- do not hide uncertainty

---

## 7. Total score regime

Use this first-pass regime mapping:

```text
0-5   = Healthy
6-10  = Slowdown
11-14 = Elevated Risk
15-20 = Recessionary
```

Store this in code, not only in the UI.

Example:

```python
def get_regime(total_score: int) -> str:
    if total_score <= 5:
        return "Healthy"
    elif total_score <= 10:
        return "Slowdown"
    elif total_score <= 14:
        return "Elevated Risk"
    return "Recessionary"
```

---

## 8. JSON schema

Create `data/current.json` with a structure similar to:

```json
{
  "generated_at": "2026-09-12T09:00:00Z",
  "country": "United States",
  "total_score": 7,
  "max_score": 20,
  "regime": "Slowdown",
  "summary": "Labor-market weakness is visible, but the economy is not yet in a full recession regime.",
  "indicators": [
    {
      "id": "payrolls",
      "name": "Payrolls",
      "category": "Labor",
      "value": 162000,
      "display_value": "August +162K | 12M avg +31K",
      "unit": "jobs",
      "score": 1,
      "explanation": "Weak beneath the headline number",
      "source": "BLS",
      "observation_date": "2026-08-01"
    }
  ]
}
```

The frontend must consume this JSON.

Do not make the frontend calculate macro scores.

---

## 9. History file

Create `data/history.json`.

Each entry should contain:

```json
{
  "date": "2026-09-12",
  "total_score": 7,
  "regime": "Slowdown"
}
```

When the update script runs:
- read existing history
- append a new record only when the date is new
- avoid duplicate dates
- keep history sorted by date

---

## 10. Frontend design direction

The site should visually resemble a clean Google Cloud architecture diagram mixed with a financial dashboard.

### Main visual direction
- light gray / white background
- dark navy typography
- Google-style blue as primary accent
- green for healthy
- yellow for warning
- red for recessionary
- rounded white cards
- thin gray borders
- subtle shadows
- clean vector-style icons
- responsive layout

### Gauge
At the top:
- large semicircular gauge
- green left section
- yellow middle section
- red right section
- needle position calculated from `total_score / max_score`
- animate the needle smoothly on page load
- show total score prominently
- show regime beneath the score

Gauge labels:
- Healthy
- Slowdown
- Recession

### Main score
Example:
`7 / 20`

### Cards
Two columns on desktop.
One column on mobile.

Each card should show:
- icon
- indicator title
- current display value
- score badge
- short explanation
- small source label

Score badge:
- green for 0
- yellow for 1
- red for 2

---

## 11. Hebrew support

The first UI version may be English internally, but the site must be easy to localize.

Prepare for:
- English
- Hebrew

Do not hardcode layout assumptions that break RTL.

Use CSS support for:

```css
direction: rtl;
```

where appropriate.

The final Hebrew dashboard should be able to use text such as:

```text
מדד קרבה למיתון
ארה״ב | ספטמבר 2026
ציון כולל
מצב נוכחי
בריא
האטה
מיתון
תמונה כוללת
```

---

## 12. Phase 1 — local static dashboard

First task:

Build the entire frontend using sample JSON only.

Do not connect to FRED or BLS yet.

Success criteria:
- `npm run dev` starts the site
- gauge renders
- score is 7/20
- 10 cards render
- responsive layout works
- cards read from JSON
- no values are manually duplicated in React components
- no API keys are needed

---

## 13. Phase 2 — Python scoring engine

After the frontend is stable:

Create Python scripts that:
1. load sample raw data
2. calculate score per indicator
3. calculate total score
4. calculate regime
5. generate `data/current.json`
6. update `data/history.json`
7. copy generated JSON to:
   `frontend/src/data/current.json`
   and
   `frontend/src/data/history.json`

Command:

```powershell
python scripts/build_dashboard_data.py
```

The script must print a clear summary:

```text
Payrolls: 1
Sahm: 0
Initial Claims: 0
...
Total Score: 7 / 20
Regime: Slowdown
current.json updated
history.json updated
```

---

## 14. Phase 3 — FRED integration

Add FRED after local sample mode works.

Environment variable:

```text
FRED_API_KEY=
```

Add to `.env.example`.

Do not commit `.env`.

Use FRED first for any series available there.

Implement a reusable helper:

```python
def fetch_fred_series(series_id: str, api_key: str):
    ...
```

The function should:
- request latest observations
- handle timeouts
- validate response
- raise a readable error
- return normalized Python data

If FRED fails:
- preserve the last valid data file
- do not replace the dashboard with empty/null data

---

## 15. Phase 4 — BLS integration

Use BLS only for series that are more reliable/direct there.

Implement:

```python
def fetch_bls_series(series_ids: list[str]):
    ...
```

Normalize all external data into the same internal structure before scoring.

---

## 16. Data-source policy

Every indicator must include a visible source.

Examples:
- BLS
- FRED
- Federal Reserve
- U.S. Treasury

Never scrape random financial websites for official macro data if an official public source exists.

If a source is manual, mark:
`source = "Manual"`

---

## 17. Error handling

The site must never break because one indicator failed to update.

Python should:
- catch HTTP failures
- log failed series
- retain previous valid values if possible
- produce a `data_status` field

Example:

```json
{
  "data_status": "partial",
  "warnings": [
    "ISM Services unavailable; previous value retained."
  ]
}
```

Frontend should show a small warning banner if:
`data_status != "ok"`

---

## 18. Git setup

Initialize Git in the project root.

Create `.gitignore` containing at least:

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

---

## 19. Python virtual environment

From project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Initial `requirements.txt`:

```text
requests
pandas
python-dotenv
```

---

## 20. Frontend setup

From project root:

```powershell
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install recharts
npm run dev
```

Do not add large UI frameworks in version 1.

Avoid:
- Material UI
- Bootstrap
- Tailwind

Use plain CSS for the first version.

---

## 21. README requirements

Create a short README with:

1. Project purpose
2. Architecture
3. Requirements
4. How to run locally
5. How to rebuild data
6. Environment variables
7. How scoring works
8. Deployment plan

Local run section should look like:

```powershell
# terminal 1
.\.venv\Scripts\Activate.ps1
python scripts/build_dashboard_data.py

# terminal 2
cd frontend
npm install
npm run dev
```

---

## 22. GitHub Actions — later phase

Create a workflow file:

`.github/workflows/update-data.yml`

The future workflow should:
- run on schedule
- run Python data update
- commit changed JSON
- push changes
- let Cloudflare Pages redeploy automatically

Do not enable this until local and GitHub manual runs are stable.

Target schedule later:

```yaml
schedule:
  - cron: "0 6 * * *"
```

One daily update is enough initially.

---

## 23. Cloudflare Pages deployment — later phase

Deployment target:
Cloudflare Pages

Build settings:

```text
Root directory: frontend
Build command: npm run build
Output directory: dist
```

The site should be compatible with static hosting.

Do not require a Node server in production.

---

## 24. OpenAI / LLM policy

Do not add OpenAI integration in phase 1.

Later, OpenAI may be used only to generate a short written market interpretation from already computed data.

Important:
- LLM output must not control scores
- LLM output must not modify thresholds
- OpenAI API key must never exist in frontend code
- OpenAI API calls should happen in a Python script or GitHub Action
- generated text should be saved into JSON

Desired future flow:

```text
Official macro data
        ↓
Rule-based scoring engine
        ↓
current.json
        ↓
optional OpenAI summary generation
        ↓
summary text saved into JSON
        ↓
static site deploy
```

Do not call OpenAI on every page load.

---

## 25. IDE / Codex behavior

The project is being built in VS Code using the official OpenAI Codex extension.

When working on this repository:

- Read this file before making structural changes.
- Prefer creating complete working files over partial snippets.
- After changes, run the appropriate test/build command.
- Explain any failure clearly.
- Do not silently change scoring thresholds.
- Do not install unnecessary dependencies.
- Do not introduce paid services.
- Do not introduce a backend unless strictly necessary.
- Keep Windows PowerShell compatibility.
- Keep code easy to understand for a technical user who wants to maintain the project locally.

---

## 26. First Codex task

When Codex reads this file, the first task should be:

> Build Phase 1 only. Create a local React + Vite + TypeScript recession-risk dashboard using sample JSON. Implement the gauge, score legend, summary panel, and all 10 indicator cards. Use the Google Cloud diagram-inspired visual style described above. Do not connect to external APIs yet. Do not add OpenAI API integration yet. Ensure `npm run dev` works.

After completing Phase 1:
- stop
- summarize what was created
- list files changed
- provide the exact command to run locally
- do not start Phase 2 until requested

---

## 27. Visual target

The target experience should feel like:

- Google Cloud architecture diagram clarity
- macro-financial dashboard functionality
- simple, clean, professional
- fast
- mobile-friendly
- data-first
- visually close to the previously designed recession infographic

The main screen should communicate within 5 seconds:

1. How close are we to recession?
2. What is the current total score?
3. Which indicators are causing the warning?
4. Which indicators are still healthy?

---

## 28. Final project philosophy

This is not a prediction engine.

It is a transparent macro monitoring dashboard.

The user should always be able to see:
- the raw indicator value
- the score
- the source
- the threshold logic
- the historical direction

The system should favor transparency and reproducibility over complexity.


---

## 29. ChatGPT handoff file

This project is being coordinated with ChatGPT outside the IDE.

After every meaningful work session, Codex must create or update a separate file in the project root named:

```text
CHATGPT_HANDOFF.md
```

The purpose of this file is to let the user send a compact, accurate project status back to ChatGPT without copying the full repository or long terminal output.

### Mandatory behavior

At the end of each requested phase or meaningful coding task:

1. Create `CHATGPT_HANDOFF.md` if it does not exist.
2. Replace its contents with the current project status.
3. Keep it concise but technically useful.
4. Do not include secrets, API keys, tokens, passwords, or `.env` values.
5. Do not paste entire source files into it.
6. Mention exact file paths when useful.
7. Mention unresolved problems and important decisions.
8. Include the exact next recommended task.
9. Include the exact local commands ChatGPT or the user may need to know.
10. If something failed, include the relevant error message or a short exact excerpt.

### Required format for `CHATGPT_HANDOFF.md`

Use this structure:

```markdown
# ChatGPT Project Handoff

## Project
US Recession Risk Dashboard

## Current Phase
Example: Phase 1 — Local Static Dashboard

## Status
Example: Completed / In Progress / Blocked

## What Was Done
- ...
- ...
- ...

## Files Created or Changed
- `frontend/src/App.tsx` — ...
- `frontend/src/components/RecessionGauge.tsx` — ...
- ...

## Current Architecture
Briefly describe the current implementation and data flow.

## Current Data / Score State
- Total score: ...
- Regime: ...
- Number of indicators implemented: ...
- Data source mode: sample / live / mixed

## Commands to Run Locally

```powershell
# Example
cd frontend
npm install
npm run dev
```

## Verification Performed
- `npm run build`: PASS / FAIL
- `npm run dev`: PASS / NOT TESTED
- Python data build: PASS / NOT IMPLEMENTED
- Other checks: ...

## Issues / Warnings
- ...
- ...

## Important Decisions
- ...
- ...

## Next Recommended Step
Describe exactly one recommended next step.

## Suggested Prompt for ChatGPT
Provide a short prompt the user can paste to ChatGPT together with this file.

Example:
"Here is the latest CHATGPT_HANDOFF.md from Codex. Review the current state and tell me the next step."
```

### Update policy

`CHATGPT_HANDOFF.md` is a living handoff file.

Codex must update it:
- after completing a phase
- after a significant refactor
- after adding a new data source
- after changing scoring logic
- after fixing an important bug
- after a failed task that requires outside guidance
- before telling the user that a requested task is complete

Do not create multiple timestamped handoff files unless explicitly requested.

Always keep the latest state in:

```text
CHATGPT_HANDOFF.md
```

### Interaction with ChatGPT

Assume the user will periodically send `CHATGPT_HANDOFF.md` to ChatGPT.

Therefore:
- explain changes in a way that another technical assistant can quickly understand
- include enough context to continue work without re-reading the entire repository
- distinguish clearly between completed work and planned work
- clearly identify provisional scoring thresholds or mocked data
- explicitly mention any manual steps the user performed outside the repository

---

## 30. First-task completion requirement

For the first Codex task defined in section 26, completion is not finished until:

1. Phase 1 has been implemented.
2. The relevant build/run verification has been performed.
3. `CHATGPT_HANDOFF.md` has been created in the project root.
4. The handoff file contains the actual current status.
5. Codex tells the user to send `CHATGPT_HANDOFF.md` back to ChatGPT for review.

