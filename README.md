# US Recession Risk Dashboard

Phase 1 is a local React + Vite + TypeScript static dashboard backed by sample JSON. It displays a deterministic sample score of 7/20 across ten macro indicators. Live data and Python scoring are deferred to Phase 2.

## Run locally

```powershell
cd frontend
npm install
npm run dev
```

Build for production with `npm run build`. The frontend reads `frontend/src/data/current.json`; no API keys are required.
