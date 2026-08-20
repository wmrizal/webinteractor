# Implementation Plan: Frontend Landing Page

**Branch**: `002-frontend-landing-page` | **Date**: 2026-07-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-frontend-landing-page/spec.md`

## Summary

Add a static landing page at the root path `/` that introduces all three sections of
the WebInteractor frontend (Targets, Runs, Run History), explains each one in plain
language, and provides a short how-to workflow per section. The page replaces the
current `* → /runs` wildcard redirect and acts as the application entry point and
navigation hub. No backend API calls are required; the page is entirely static.

## Technical Context

**Language/Version**: TypeScript 5.7 / React 18.3

**Primary Dependencies**: React Router DOM v6.28, @tanstack/react-query 5.x (existing), Vite 6, Vitest 2, Testing Library React 16

**Storage**: N/A — static page with no data persistence

**Testing**: Vitest 2 + Testing Library React + jsdom (existing `frontend/tests/integration/` suite)

**Target Platform**: Browser SPA served by Vite dev server (`http://localhost:5173`)

**Project Type**: Web application frontend (React SPA); backend is FastAPI (unchanged by this feature)

**Performance Goals**: Page must render with zero network requests; Time-to-interactive < 200ms on localhost

**Constraints**: Vanilla CSS only (no CSS framework); must reuse existing `.page-shell`, `.hero-card`, `.card`, `.eyebrow` utility classes from `styles.css`; no new npm packages required

**Scale/Scope**: 1 new page, 1 optional layout component, 1 App.tsx route change, 1 test file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven delivery: Spec includes 3 user stories, 4 measurable success criteria,
  2 edge cases, and 6 assumptions.
- [x] Independent value slices: P1 (orientation), P2 (navigation), P3 (how-to) are each
  independently testable and deliverable.
- [x] Risk-based verification: Integration tests required for route rendering and
  navigation actions; no backend contract tests needed (page is static).
- [x] Observability: Static page — no new logging required. Spec documents this
  explicitly under Constitution Alignment.
- [x] Secure and reversible change: No security impact (public static page). Rollback =
  revert `App.tsx` route change (one-line change).

**Post-Phase 1 re-check**: ✅ Design adds no cross-story coupling. Section cards are
independently renderable UI units. Test plan covers all acceptance criteria.

## Project Structure

### Documentation (this feature)

```text
specs/002-frontend-landing-page/
├── plan.md        ← this file
├── research.md    ← Phase 0 output
├── data-model.md  ← Phase 1 output (no new entities; documents static structure)
├── quickstart.md  ← Phase 1 output
├── contracts/
│   └── ui-routes.md   ← Phase 1 output (route contract)
└── tasks.md       ← Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── App.tsx                          ← add `/` route; add NavBar wrapper
│   ├── styles.css                       ← add landing + nav styles
│   ├── components/
│   │   └── layout/
│   │       └── NavBar.tsx               ← NEW: shared top navigation bar
│   └── pages/
│       └── LandingPage.tsx              ← NEW: static landing page component
└── tests/
    └── integration/
        └── landing-page.spec.tsx        ← NEW: route + navigation + content tests
```

**Structure Decision**: Web application (Option 2). Only frontend is changed.
The new `LandingPage.tsx` lives alongside existing page components. `NavBar.tsx`
is placed in `components/layout/` following the existing `components/` convention.
No backend changes are required.

## Complexity Tracking

> No constitution violations. Table omitted.
