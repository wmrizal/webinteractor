# WebInteractor

A web application that lets operators define automation targets, execute Playwright-driven browser sessions to capture page information and toggle a feature on or off, and review run outcomes with clear diagnostics.

## How It Works

### Overview

WebInteractor is a two-tier application:

- **Backend** — FastAPI REST API backed by SQLite (via SQLModel). Handles target configuration, run orchestration, and Playwright browser automation.
- **Frontend** — Vite/React SPA that consumes the backend API. Provides pages to manage targets, trigger runs, and review history.

### Core Concepts

**Automation Target**
A saved configuration describing:
- The URL to open (`baseUrl` + optional `pagePath`)
- One or more extraction rules — CSS selectors whose text values are captured during each run
- A toggle rule — the CSS selector for the toggle control, how to verify its state (`dom-attribute`, `aria-checked`, or `text-label`), and which attribute/value signals ON vs OFF
- An optional auth profile identifier
- A default desired state (`on` or `off`)

**Run**
An explicit, user-initiated execution against a saved target. The operator chooses the desired toggle state (`on`/`off`) at run time. The run goes through these steps in order:

1. **Navigate** — Playwright opens a headless Chromium browser and navigates to the target URL.
2. **Extract** — Each configured extraction selector is evaluated and its text value is captured.
3. **Detect state** — The toggle's current state is read from the DOM.
4. **Toggle (if needed)** — If the current state already matches the desired state, the run ends with `no-change-needed`. Otherwise the toggle control is clicked and the state is verified.
5. **Record outcome** — The run is persisted with a terminal status (`success`, `failed`, or `no-change-needed`), the captured values, the before/after toggle states, and a failure message/step if something went wrong.

### Run Statuses

| Status | Meaning |
|---|---|
| `queued` | Run created, not yet started |
| `running` | Browser session is active |
| `success` | Toggle reached desired state and was verified |
| `no-change-needed` | Toggle was already in desired state; no action taken |
| `failed` | An error occurred; `failureStep` and `failureMessage` explain where and why |

### Failure Steps

When a run fails, the `failureStep` field tells you where in the pipeline it stopped:

| Step | Cause |
|---|---|
| `navigate` | Page could not be loaded within the timeout |
| `authenticate` | Auth wall encountered and credentials unavailable |
| `extract` | A required extraction selector returned no element |
| `toggle` | Toggle control not found or could not be clicked |
| `verify` | State after click did not match desired state |

---

## Project Structure

```
backend/
  src/
    main.py                  # App entry point
    api/
      app.py                 # FastAPI app factory + middleware
      routes/
        targets.py           # CRUD endpoints for /targets
        runs.py              # Run creation and detail endpoints
        run_history.py       # Run history per target
        system.py            # Health check
    automation/
      browser_runner.py      # Playwright execution engine
    models/
      automation_target.py   # Target entity + request/response schemas
      automation_run.py      # Run entity + request/response schemas
      captured_item.py       # Captured extraction value
      toggle_result.py       # Toggle before/after outcome
      base.py                # Shared enums and base models
    services/
      target_service.py      # Target business logic
      run_service.py         # Run orchestration
      run_history_service.py # Run history queries
    lib/
      db.py                  # SQLite session management
      migrations.py          # Schema bootstrap
    observability/
      logging.py             # Structured JSON logging
      events.py              # Run event definitions
      run_event_store.py     # Step-level event persistence

frontend/
  src/
    App.tsx                  # Route definitions
    pages/
      TargetsPage.tsx        # List and manage automation targets
      RunPage.tsx            # Trigger runs against a target
      RunHistoryPage.tsx     # View past run results
    components/
      targets/TargetForm.tsx # Target create/edit form
      runs/RunDetailsPanel.tsx # Run outcome viewer
    features/
      targets/useTargets.ts  # Target data hooks
      runs/useRunActions.ts  # Run trigger and status hooks
    services/
      apiClient.ts           # Typed fetch wrapper for the backend API
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Chromium (installed via Playwright)

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

Create a `.env` file in `backend/`:

```env
APP_ENV=development
DATABASE_URL=sqlite:///./data/app.db
LOG_LEVEL=INFO
```

Start the API:

```powershell
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

### Frontend

```powershell
cd frontend
npm install
```

Create a `.env` file in `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start the dev server:

```powershell
npm run dev
```

---

## API Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/targets` | List all automation targets |
| `POST` | `/targets` | Create a new target |
| `GET` | `/targets/{id}` | Get a single target |
| `PATCH` | `/targets/{id}` | Update a target |
| `DELETE` | `/targets/{id}` | Delete a target |
| `POST` | `/runs` | Start a run (returns `202 Accepted`) |
| `GET` | `/runs/{id}` | Get run details including captured items and toggle result |
| `GET` | `/targets/{id}/runs` | List all runs for a target |

Full OpenAPI specification: [`specs/001-browser-feature-toggle/contracts/api-openapi.yaml`](specs/001-browser-feature-toggle/contracts/api-openapi.yaml)

---

## Running Tests

**Backend**

```powershell
cd backend
pytest
```

**Frontend**

```powershell
cd frontend
npm test
```

---

## Security Notes

- `baseUrl` values must be HTTPS.
- Do not commit credentials. Use environment variables or OS keychain injection via `authProfile`.
- All runs require explicit user initiation; there is no background scheduling.
