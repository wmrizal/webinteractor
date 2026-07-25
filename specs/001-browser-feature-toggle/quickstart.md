# Quickstart: Browser Feature Toggle Automation

## 1) Prerequisites

- Python 3.12+
- Node.js 20+
- Chromium install via Playwright
- Access credentials to target web application

## 2) Configure Environment

Backend environment variables:
- `APP_ENV=development`
- `DATABASE_URL=sqlite:///./data/app.db`
- `LOG_LEVEL=INFO`

Frontend environment variables:
- `VITE_API_BASE_URL=http://localhost:8000`

Security notes:
- Do not store credentials in source files.
- Use OS keychain or environment injection for secrets.

## 3) Install Dependencies

Backend:
- `cd backend`
- `python -m venv .venv`
- `.venv\\Scripts\\Activate.ps1` (Windows PowerShell)
- `pip install -r requirements.txt`
- `python -m playwright install chromium`

Frontend:
- `cd frontend`
- `npm install`

## 4) Run the App

Start backend API:
- `cd backend`
- `uvicorn src.main:app --reload --port 8000`

Start frontend:
- `cd frontend`
- `npm run dev`

## 5) Execute First Automation

1. Open the UI and create an automation target.
2. Configure extraction selectors and toggle selectors.
3. Start a run with desired state `on`.
4. Review captured info and terminal run status.

## 6) Verify Reversibility

1. Execute a second run with desired state `off`.
2. Confirm terminal status and final state evidence in run details.

## 7) Validation Commands

Backend tests:
- `cd backend`
- `pytest`

Frontend tests:
- `cd frontend`
- `npm test`

Contract tests:
- `cd backend`
- `pytest tests/contract`

Integration tests:
- `cd backend`
- `pytest tests/integration`

## 8) Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|-----------|
| Run status stuck at `running` | Playwright browser not installed | Run `python -m playwright install chromium` |
| `404` on `/targets/{id}` | Target UUID does not exist | Check target list via `GET /targets` |
| Toggle state after run differs from requested | Page element selectors changed | Update extraction rules and toggle selectors on target |
| Run status `failed` with `failureStep=navigate` | Page URL unreachable or timeout | Confirm `baseUrl` and `pagePath` are correct HTTPS URLs |
| Frontend cannot reach API | `VITE_API_BASE_URL` misconfigured | Set `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env` |
| Secrets appearing in logs | Misconfigured env vars | Never put secrets in log messages; use env injection |

## 9) Validation Evidence

- Backend contract tests: all targets API and runs API tests passing.
- Backend integration tests: US1 CRUD, US2 success and no-change paths, US3 failure diagnostics passing.
- Backend toggle reversal test: on → off → on round-trip passing.
- Frontend integration tests: targets page, run execution page, and run history page tests passing.
- Quickstart walkthrough validated against local SQLite `data/app.db` instance.
