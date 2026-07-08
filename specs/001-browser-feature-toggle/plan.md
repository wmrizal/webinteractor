# Implementation Plan: Browser Feature Toggle Automation

**Branch**: `001-browser-feature-toggle` | **Date**: 2026-07-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-browser-feature-toggle/spec.md`

## Summary

Build a web application that lets operators define automation targets (URL + selectors), execute Playwright-driven browser sessions to capture page information and toggle a feature on/off, and review run outcomes with clear pass/fail diagnostics.

Backend: FastAPI REST API + SQLite via SQLModel + Playwright runner.
Frontend: Vite-based SPA consuming the backend API.

## Technical Context

**Language/Version**: Python 3.12 (backend), Node.js 20+ (frontend)

**Primary Dependencies**: FastAPI 0.115, Uvicorn 0.30.6, SQLModel 0.0.22, Pydantic 2.9.2, Playwright 1.47 (backend); Vite (frontend)

**Storage**: SQLite via SQLModel (`data/app.db`); upgrade path to PostgreSQL possible via DATABASE_URL env var

**Testing**: pytest 8.3.3, pytest-asyncio 0.24.0, pytest-playwright 0.5.2, httpx 0.27.2 (backend); npm test (frontend)

**Target Platform**: Desktop web browser (Chrome/Edge); backend runs on local machine or server

**Project Type**: Web application — FastAPI backend + Vite frontend (Option 2 structure)

**Performance Goals**: 95% of valid automation runs complete within 90 seconds (SC-001); API responses for CRUD <500ms p95

**Constraints**: Runs require explicit user initiation (no background scheduling); secrets must not be committed; HTTPS required for all target `baseUrl` values

**Scale/Scope**: Single-operator tooling; tens to low-hundreds of targets; run history retained per target

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven delivery: Spec includes user stories (US1–3), measurable success criteria (SC-001–004), edge cases, and assumptions.
- [x] Independent value slices: US1 (target config), US2 (run execution), US3 (run review) are independently deliverable and testable.
- [x] Risk-based verification: Unit tests for validation/state-machine logic; integration tests for API endpoints; contract tests against OpenAPI spec; Playwright e2e tests for automation runner.
- [x] Observability: Each run emits step-level status (`failureStep`), terminal outcome, and diagnostic context in `AutomationRun.failureMessage`. Structured logs via `LOG_LEVEL` env var.
- [x] Secure and reversible change: Explicit user initiation only; credentials via OS keychain/env injection, never committed; recovery by re-running with opposite desired state.

## Project Structure

### Documentation (this feature)

```text
specs/001-browser-feature-toggle/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── api-openapi.yaml # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLModel entity definitions (AutomationTarget, AutomationRun, CapturedItem, ToggleResult)
│   ├── services/        # Business logic: runner service, toggle engine, capture service
│   ├── api/             # FastAPI routers: /targets, /runs
│   └── main.py          # App entrypoint
├── tests/
│   ├── contract/        # OpenAPI contract validation tests
│   ├── integration/     # API endpoint tests (httpx)
│   └── unit/            # Validation, state-transition, and service unit tests
└── requirements.txt

frontend/
├── src/
│   ├── components/      # Shared UI components
│   ├── pages/           # Target list, target detail, run detail views
│   └── services/        # API client
└── tests/
```

**Structure Decision**: Option 2 (Web application). The workspace already has `backend/` and `frontend/` directories established with matching dependencies.
