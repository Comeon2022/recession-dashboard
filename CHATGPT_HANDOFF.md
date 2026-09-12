# ChatGPT Project Handoff

## Project
US Recession Risk Dashboard

## Current Phase
Deployment preparation — GitHub Actions data refresh

## Status
Workflow created and locally validated. GitHub-hosted live execution is pending repository-secret setup and a manual Actions run.

## What Was Done
- Created `.github/workflows/update-data.yml` with `workflow_dispatch` and weekday `14:00 UTC` schedule (`0 14 * * 1-5`).
- Configured the workflow to consume the repository secret `FRED_API_KEY` without printing or storing it.
- Added Python dependency installation, the existing data pipeline, generated-JSON validation, and frontend production build.
- Configured commits to stage only the four generated JSON files and push only when staged content changes.
- Updated `README.md` with GitHub secret setup and manual workflow instructions.

## Files Created or Changed
- `.github/workflows/update-data.yml` — automated FRED refresh workflow.
- `README.md` — GitHub Actions secret/setup documentation.
- `CHATGPT_HANDOFF.md` — current deployment-preparation status.
- Generated JSON files were refreshed by the local verification run.

## Current Architecture
GitHub Actions checks out the repository, installs Python dependencies, supplies `FRED_API_KEY` through the Actions secret environment, runs `scripts/build_dashboard_data.py`, validates root/frontend JSON synchronization, runs `npm ci` and `npm run build` from `frontend`, then commits only generated data files if they changed.

## Current Data / Score State
- Total score: 10 / 28
- Normalized risk score: 36 / 100
- Regime: Slowdown
- Indicators implemented: 18
- Live FRED-backed indicators: 15
- Manual/sample indicators: 3
- Data status: `ok` in the local `.env` verification run

## Commands to Run Locally
```powershell
# Local pipeline check
python scripts/build_dashboard_data.py

# Frontend build check
cd frontend
npm run build
```

## Verification Performed
- Workflow YAML parse: PASS using local PyYAML parser.
- Local Python pipeline with configured local key: PASS.
- Generated JSON validation and root/frontend synchronization: PASS.
- `npm run build`: PASS.
- GitHub Actions live run: NOT TESTED — requires the GitHub repository secret and a GitHub-hosted runner.

## Issues / Warnings
- The workflow cannot be fully live-tested from this workspace. The user must add the repository secret `FRED_API_KEY` in **Settings → Secrets and variables → Actions**, then manually run **Actions → Update macro dashboard data → Run workflow**.
- No Cloudflare-specific files were added.
- No BLS or OpenAI integration was added.

## Important Decisions
- Schedule is exactly weekdays at 14:00 UTC: `0 14 * * 1-5`.
- The workflow stages only `data/current.json`, `data/history.json`, `frontend/src/data/current.json`, and `frontend/src/data/history.json`.
- No scoring thresholds or indicators were changed.
- The secret is referenced only as `${{ secrets.FRED_API_KEY }}` and is never echoed.

## Next Recommended Step
Add the GitHub repository secret `FRED_API_KEY` and manually run the workflow once from GitHub Actions to validate the hosted refresh and conditional commit behavior.

## Suggested Prompt for ChatGPT
Here is the latest `CHATGPT_HANDOFF.md` from Codex. The GitHub Actions refresh workflow is locally validated, but its live run is pending repository-secret setup and manual dispatch. Review the workflow and README instructions.
