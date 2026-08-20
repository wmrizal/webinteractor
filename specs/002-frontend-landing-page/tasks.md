# Tasks: Frontend Landing Page

**Input**: Design documents from `specs/002-frontend-landing-page/`

**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ui-routes.md ✅, quickstart.md ✅

**Tests**: Integration tests are included per the plan's risk-based verification requirement (route rendering + navigation actions). Tests are written task-first (write test → confirm it fails → implement).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Paths follow the web app convention (`frontend/src/`, `frontend/tests/`)

---

## Phase 1: Setup

**Purpose**: Route infrastructure — update the wildcard fallback so unknown paths land on `/` once the landing page exists.

- [X] T001 Update `*` wildcard redirect from `<Navigate to="/runs" />` to `<Navigate to="/" />` in `frontend/src/App.tsx` *(no LandingPage import required — the `/` route is added in T006)*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared navigation bar required by FR-006 (accessible from any page). Must be complete before any user story work begins.

**⚠️ CRITICAL**: User story pages cannot be navigated back to the landing page until this phase is complete.

- [X] T002 Create `frontend/src/components/layout/NavBar.tsx` with `<NavLink>` items: Home (`/`), Targets (`/targets`), Runs (`/runs`), Run History (`/history`) and `aria-current` active-state support
- [X] T003 [P] Add `.nav-bar` styles (layout, active-link highlight, responsive) to `frontend/src/styles.css`
- [X] T004 Wrap `<Routes>` in `frontend/src/App.tsx` with `<NavBar />` so it appears on every page

**Checkpoint**: Navigation bar renders on all pages; `/` route exists but shows nothing until Phase 3.

---

## Phase 3: User Story 1 - New User Orientation (Priority: P1) 🎯 MVP

**Goal**: A first-time visitor to `/` sees an app header, a brief application description, and three section cards — one each for Targets, Runs, and Run History — each with a title and a plain-language description.

**Independent Test**: Open `http://localhost:5173/`. The landing page renders with the app title, an application description, and three clearly labelled section cards. No backend must be running. No targets need to exist.

### Tests for User Story 1 ⚠️

> **Write these tests FIRST, confirm they FAIL, then implement.**

- [X] T005 [US1] Write integration tests: landing page renders at `/` with app title, and three card headings ("Targets", "Runs", "Run History") in `frontend/tests/integration/landing-page.spec.tsx`

### Implementation for User Story 1

- [X] T006 [US1] Create `frontend/src/pages/LandingPage.tsx` with an app title hero section and three section cards (title + description, no CTA or how-to yet), and add the `<Route path="/" element={<LandingPage />} />` entry to `frontend/src/App.tsx`
- [X] T007 [P] [US1] Add `.landing-grid` (CSS grid, 3 columns, responsive) and `.section-card` styles to `frontend/src/styles.css`

**Checkpoint**: User Story 1 is fully functional. `npm run test` passes T005. The landing page renders at `/` with zero API calls and shows all three section cards with descriptions.

---

## Phase 4: User Story 2 - Quick Navigation for Returning Users (Priority: P2)

**Goal**: Each section card has a clearly labelled CTA that navigates the user to the correct route in one click.

**Independent Test**: Click each card's CTA and confirm the URL changes to `/targets`, `/runs`, and `/history` respectively. Can be verified without a running backend.

### Tests for User Story 2 ⚠️

> **Write these tests FIRST, confirm they FAIL, then implement.**

- [X] T008 [P] [US2] Add navigation test cases to `frontend/tests/integration/landing-page.spec.tsx`: click each card CTA and assert route changes to `/targets`, `/runs`, `/history`

### Implementation for User Story 2

- [X] T009 [US2] Add `<Link to="...">` CTA button/link to each section card in `frontend/src/pages/LandingPage.tsx` with descriptive labels (e.g., "Manage Targets", "Start a Run", "View History")

**Checkpoint**: User Stories 1 AND 2 are independently functional. All navigation tests pass.

---

## Phase 5: User Story 3 - Contextual How-To Reference (Priority: P3)

**Goal**: Each section card shows an ordered how-to list with at least two actionable steps describing the workflow for that section, accurate to the actual page behaviour.

**Independent Test**: On each section card, verify that an ordered list with ≥ 2 steps is visible and the steps describe the real workflow (matches research.md Decision 4 content mapping).

### Tests for User Story 3 ⚠️

> **Write these tests FIRST, confirm they FAIL, then implement.**

- [X] T010 [P] [US3] Add how-to content tests to `frontend/tests/integration/landing-page.spec.tsx`: each section card renders an ordered list with ≥ 2 items

### Implementation for User Story 3

- [X] T011 [US3] Add `<ol>` how-to step lists to each section card in `frontend/src/pages/LandingPage.tsx` using content from `research.md` Decision 4 content mapping:
  - **Targets**: "Fill in Base URL, page path, and CSS selector." / "Save the target." / "Reuse it in any Run."
  - **Runs**: "Pick a saved Target from the dropdown." / "Choose desired state (on/off)." / "Click Run and monitor the status."
  - **Run History**: "Select a target to see its past runs." / "Click a run to inspect toggle results and captured screenshots."

**Checkpoint**: All three user stories are independently functional. All tests pass. Landing page is complete.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final quality pass before merge.

- [X] T012 [P] Run `npm run lint` in `frontend/` and fix any ESLint or TypeScript errors
- [X] T013 Run `npm run test` in `frontend/` and confirm all integration tests pass (including pre-existing `targets.spec.tsx`, `run-history.spec.tsx`, `run-execution.spec.tsx`)
- [X] T014 Validate quickstart.md steps: run `npm run dev` and manually verify all seven checks in `quickstart.md` "What to Verify Manually" table

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: No hard dependency on Phase 1 — T001 only changes the wildcard redirect and does not import `LandingPage`; T004 depends on T002 (NavBar must exist before wrapping)
- **User Stories (Phase 3–5)**: All depend on Phase 2 completion
  - US1, US2, US3 can proceed in priority order P1 → P2 → P3 (sequential recommended; all touch `LandingPage.tsx`)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — no dependencies on US2 or US3
- **US2 (P2)**: Can start after Phase 2 — builds on the cards created in US1 (T006 must exist)
- **US3 (P3)**: Can start after Phase 2 — builds on the cards created in US1 (T006 must exist); independent of US2

### Within Each User Story

- Test task (T005, T008, T010) MUST be written and FAIL before the implementation task runs
- T007 (styles) can run in parallel with T006 (component) since they touch different files
- T008 and T010 can be written in parallel (same test file, no code conflicts if on separate branches)

### Parallel Opportunities

| Parallel Group | Tasks | Condition |
|---|---|---|
| Phase 2 setup | T002, T003 | Different files (`NavBar.tsx` vs `styles.css`) |
| US1 implementation | T006, T007 | Different files (`LandingPage.tsx` vs `styles.css`) |
| US2 + US3 tests | T008, T010 | Same file but additive — safe if coordinated |
| Polish | T012 + T014 | Different concerns (lint vs manual check) |

---

## Implementation Strategy

**MVP scope** (deliver value fastest): Complete Phase 1 + Phase 2 + Phase 3 (T001–T007).
This gives a functional landing page at `/` with nav bar and section cards — enough for user testing.

**Incremental delivery**:
1. Phase 1+2: Routing + nav bar (invisible to end-users but required)
2. Phase 3: Cards with descriptions (US1 MVP complete)
3. Phase 4: Navigation CTAs on cards (US2 complete)
4. Phase 5: How-to lists on cards (US3 complete)
5. Phase 6: Polish and validation
