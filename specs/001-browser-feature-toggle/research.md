# Research: Browser Feature Toggle Automation

**Branch**: `001-browser-feature-toggle` | **Date**: 2026-07-09

## Overview

All technical unknowns were resolved from the existing project dependencies (`backend/requirements.txt`, `frontend/.env.example`) and Playwright/FastAPI ecosystem best practices. No blocking unknowns remain.

---

## Decision: Browser Automation Library

**Decision**: Playwright 1.47 (already pinned in `requirements.txt`)

**Rationale**:
- Supports Chromium, Firefox, and WebKit headless/headed modes.
- Native async API integrates cleanly with FastAPI async request handlers and `asyncio`.
- `pytest-playwright` 0.5.2 provides fixture-based test integration without extra setup.
- `page.locator()` API supports CSS, XPath, and ARIA selectors — sufficient for all toggle and extraction rules defined in the data model.

**Alternatives considered**:
- Selenium: larger runtime overhead, no native async support, slower to configure.
- Puppeteer (Node.js): would require a separate Node.js automation process and IPC layer, adding complexity.

---

## Decision: Backend Web Framework

**Decision**: FastAPI 0.115 with Uvicorn 0.30.6 (already pinned)

**Rationale**:
- Async-first framework; aligns with Playwright's async execution model.
- Pydantic 2.x models double as request/response validation and SQLModel ORM definitions, reducing duplication.
- Built-in OpenAPI docs generation validates against `contracts/api-openapi.yaml`.

**Alternatives considered**:
- Flask: synchronous by default; would require threading or greenlets for non-blocking Playwright runs.
- Django: heavier framework with ORM conventions not aligned to SQLModel's lightweight approach.

---

## Decision: Data Storage

**Decision**: SQLite via SQLModel 0.0.22 for development; DATABASE_URL env var enables PostgreSQL upgrade

**Rationale**:
- Zero-config for local operator use.
- SQLModel unifies Pydantic validation models and SQLAlchemy ORM — single source of truth for entity schemas.
- Alembic (bundled with SQLAlchemy) supports schema migration when upgrading to PostgreSQL.

**Alternatives considered**:
- Raw SQLAlchemy: more boilerplate, no automatic Pydantic validation integration.
- MongoDB: document store offers no query advantages over relational for this structured run-history model.

---

## Decision: Async Run Execution Pattern

**Decision**: Background task via FastAPI `BackgroundTasks` for initial release; upgrade path to Celery/RQ noted.

**Rationale**:
- `POST /runs` returns `202 Accepted` immediately; Playwright run executes asynchronously in the same process.
- `BackgroundTasks` requires no external broker, matching the "zero external dependencies" constraint of initial release.
- `AutomationRun.status` transitions (`queued → running → terminal`) are polled by the frontend via `GET /runs/{runId}`.

**Alternatives considered**:
- Celery + Redis: appropriate for multi-user or high-concurrency scheduling; over-engineered for single-operator initial scope.
- Threading: more complex error isolation than `asyncio` coroutines.

---

## Decision: Frontend Framework

**Decision**: Vite-based SPA (framework TBD by frontend scaffold; `VITE_API_BASE_URL` env var already present)

**Rationale**:
- Vite is already referenced in `frontend/.env.example`.
- Decoupled SPA consumes the REST API, making backend and frontend independently testable.
- `npm test` integration is framework-agnostic.

**Alternatives considered**:
- Server-side rendering (e.g., Jinja2 templates from FastAPI): tighter coupling, harder to test UI independently.

---

## Decision: Toggle State Detection

**Decision**: Support three verification methods defined in `ToggleResult.verificationMethod`: `dom-attribute`, `text-label`, `aria-checked`.

**Rationale**:
- Different target applications expose toggle state differently; no single method is universal.
- `aria-checked` is the most semantically reliable when present; `dom-attribute` and `text-label` serve as fallbacks.
- All three are expressible via Playwright `page.locator().get_attribute()` and `inner_text()`.

**Alternatives considered**:
- Screenshot diffing: brittle, slow, not human-readable in run logs.
- Accessibility tree only: not all applications expose proper ARIA roles.

---

## Decision: Credential / Auth Handling

**Decision**: Reuse existing browser session via Playwright `storage_state` JSON files; reference by `authProfile` field on `AutomationTarget`.

**Rationale**:
- Session files (cookies + localStorage) can be pre-exported from a logged-in browser and injected per run.
- Avoids storing raw credentials; meets "secrets must not be committed" constraint.
- Aligns with the spec assumption: "enterprise authentication/session practices already available to operators."

**Alternatives considered**:
- Username/password form automation: requires storing credentials; violates security constraint.
- OAuth token injection: target-app-specific; not generalisable.

---

## Resolved Unknowns Summary

| Unknown | Resolution |
|---------|------------|
| Async run execution | FastAPI `BackgroundTasks`; poll via `GET /runs/{runId}` |
| Toggle state detection | 3-method enum in `ToggleResult.verificationMethod` |
| Auth/session handling | Playwright `storage_state` JSON per `authProfile` |
| Storage upgrade path | DATABASE_URL env var; Alembic migrations |
| Frontend framework | Vite SPA (scaffold to be confirmed on first `npm init`) |
