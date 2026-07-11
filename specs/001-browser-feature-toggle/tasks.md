# Tasks: Browser Feature Toggle Automation

**Input**: Design documents from /specs/001-browser-feature-toggle/

**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, quickstart.md

**Tests**: Test tasks are included because this feature explicitly requires automated validation for behavior-changing flows.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize project structure and baseline tooling.

- [X] T001 Create backend and frontend folder skeleton in backend/src and frontend/src
- [X] T002 Initialize backend project dependencies and tooling in backend/requirements.txt and backend/pyproject.toml
- [X] T003 [P] Initialize frontend project dependencies and scripts in frontend/package.json
- [X] T004 [P] Add environment templates in backend/.env.example and frontend/.env.example
- [X] T005 [P] Configure linting and formatting in backend/pyproject.toml and frontend/eslint.config.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared platform capabilities required by all stories.

**CRITICAL**: No user story tasks should start until this phase is complete.

- [X] T006 Implement database base models and session management in backend/src/models/base.py and backend/src/lib/db.py
- [X] T007 Implement SQLite initialization and migration bootstrap in backend/src/lib/migrations.py
- [X] T008 Create API app factory, routing registration, and middleware chain in backend/src/main.py and backend/src/api/app.py
- [X] T009 [P] Implement structured logging and run event schema in backend/src/observability/logging.py and backend/src/observability/events.py
- [X] T010 [P] Implement API error mapping and consistent error responses in backend/src/api/errors.py
- [X] T011 [P] Implement frontend API client and request error handling in frontend/src/services/apiClient.ts
- [X] T012 [P] Create contract test harness and API fixtures in backend/tests/contract/conftest.py
- [X] T013 [P] Create integration test fixture target page setup in backend/tests/integration/fixtures/test_target_page.py

**Checkpoint**: Foundation is ready for user story implementation.

---

## Phase 3: User Story 1 - Configure Browser Automation Target (Priority: P1)

**Goal**: Allow operators to create, edit, delete, and persist runnable automation targets.

**Independent Test**: Create a target with required fields, save it, reload it, and verify field integrity.

### Tests for User Story 1

- [X] T014 [P] [US1] Add contract tests for target CRUD endpoints in backend/tests/contract/test_targets_api.py
- [X] T015 [P] [US1] Add frontend integration test for target form and target list behavior in frontend/tests/integration/targets.spec.ts

### Implementation for User Story 1

- [X] T016 [P] [US1] Implement AutomationTarget model and persistence mapping in backend/src/models/automation_target.py
- [X] T017 [P] [US1] Implement extraction and toggle rule validators in backend/src/models/rules.py
- [X] T018 [US1] Implement target service for create/update/delete/list logic in backend/src/services/target_service.py
- [X] T019 [US1] Implement target API routes in backend/src/api/routes/targets.py
- [X] T020 [US1] Implement target management page in frontend/src/pages/TargetsPage.tsx
- [X] T021 [US1] Implement target form and validation UI in frontend/src/components/targets/TargetForm.tsx
- [X] T022 [US1] Implement target query and mutation hooks in frontend/src/features/targets/useTargets.ts

**Checkpoint**: User Story 1 is independently functional and testable.

---

## Phase 4: User Story 2 - Run Automation to Read and Toggle (Priority: P1)

**Goal**: Execute browser automation runs that capture configured information and enforce desired toggle state.

**Independent Test**: Run against a prepared target page and verify captured data plus final toggle state evidence.

### Tests for User Story 2

- [ ] T023 [P] [US2] Add contract tests for run trigger and run detail endpoints in backend/tests/contract/test_runs_api.py
- [ ] T024 [P] [US2] Add backend integration test for browser automation success and no-change paths in backend/tests/integration/test_run_automation_flow.py
- [ ] T025 [P] [US2] Add frontend integration test for run trigger and state selection in frontend/tests/integration/run-execution.spec.ts

### Implementation for User Story 2

- [ ] T026 [P] [US2] Implement AutomationRun and CapturedItem models in backend/src/models/automation_run.py and backend/src/models/captured_item.py
- [ ] T027 [P] [US2] Implement ToggleResult model in backend/src/models/toggle_result.py
- [ ] T028 [US2] Implement Playwright browser runner for navigate-extract-toggle-verify flow in backend/src/automation/browser_runner.py
- [ ] T029 [US2] Implement run orchestration service with terminal state transitions in backend/src/services/run_service.py
- [ ] T030 [US2] Implement run API routes in backend/src/api/routes/runs.py
- [ ] T031 [US2] Implement run execution page with desired state controls in frontend/src/pages/RunPage.tsx
- [ ] T032 [US2] Implement frontend run action hooks and status polling in frontend/src/features/runs/useRunActions.ts

**Checkpoint**: User Story 2 is independently functional and testable.

---

## Phase 5: User Story 3 - Review Run Outcome and Failures (Priority: P2)

**Goal**: Provide clear run history and diagnostics for trust and troubleshooting.

**Independent Test**: Execute one successful run and one failure path; confirm detailed, actionable diagnostics in UI.

### Tests for User Story 3

- [ ] T033 [P] [US3] Add backend integration test for failure diagnostics and failure-step capture in backend/tests/integration/test_run_failure_diagnostics.py
- [ ] T034 [P] [US3] Add frontend integration test for run history and run details rendering in frontend/tests/integration/run-history.spec.ts

### Implementation for User Story 3

- [ ] T035 [US3] Implement run event persistence for step-level diagnostics in backend/src/observability/run_event_store.py
- [ ] T036 [US3] Implement run history query service in backend/src/services/run_history_service.py
- [ ] T037 [US3] Implement run history and detailed diagnostics API routes in backend/src/api/routes/run_history.py
- [ ] T038 [US3] Implement run history page in frontend/src/pages/RunHistoryPage.tsx
- [ ] T039 [US3] Implement run details diagnostics panel component in frontend/src/components/runs/RunDetailsPanel.tsx

**Checkpoint**: User Story 3 is independently functional and testable.

---

## Phase 6: Polish and Cross-Cutting Concerns

**Purpose**: Improve reliability, security posture, and operational readiness across stories.

- [ ] T040 [P] Update operational usage and troubleshooting guide in specs/001-browser-feature-toggle/quickstart.md
- [ ] T041 Implement log redaction and secret-safe diagnostics in backend/src/observability/logging.py and backend/src/services/run_service.py
- [ ] T042 [P] Add integration test for toggle reversal workflow in backend/tests/integration/test_toggle_reversal.py
- [ ] T043 Add integration performance smoke test for concurrent manual runs in backend/tests/integration/test_run_concurrency.py
- [ ] T044 Run quickstart validation and record evidence notes in specs/001-browser-feature-toggle/quickstart.md

---

## Dependencies and Execution Order

### Phase Dependencies

- Setup (Phase 1): No dependencies.
- Foundational (Phase 2): Depends on Setup; blocks all user stories.
- User Stories (Phase 3-5): Depend on Foundational completion.
- Polish (Phase 6): Depends on completion of desired user stories.

### User Story Dependencies

- US1: Can start immediately after Foundational.
- US2: Depends on Foundational and minimally on US1 target creation capability.
- US3: Depends on US2 run data and diagnostics events.

### Within Each User Story

- Tests before implementation.
- Models before services.
- Services before API routes.
- Backend routes before frontend integration wiring.

## Parallel Opportunities

- Setup: T003, T004, and T005 can run in parallel.
- Foundational: T009, T010, T011, T012, and T013 can run in parallel after T006-T008 start stabilizing.
- US1: T014, T015, T016, and T017 can run in parallel.
- US2: T023, T024, T025, T026, and T027 can run in parallel.
- US3: T033 and T034 can run in parallel; T038 and T039 can proceed in parallel after T037 contract stabilizes.

## Parallel Example: User Story 1

- Execute T014 and T015 together while model work starts.
- Execute T016 and T017 together.
- Then complete T018 -> T019 and frontend T020 -> T022.

## Parallel Example: User Story 2

- Execute T023, T024, and T025 together.
- Execute T026 and T027 together.
- Then complete T028 -> T030 while frontend executes T031 and T032.

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete US1 to establish reusable target configuration.
3. Complete US2 to deliver core browser read-and-toggle workflow.
4. Validate with acceptance scenarios before starting US3.

### Incremental Delivery

1. Deliver US1 (target management) and demo.
2. Deliver US2 (execution and toggle enforcement) and demo.
3. Deliver US3 (history and diagnostics) and demo.
4. Complete cross-cutting polish.

### Team Parallelization

1. Team completes Setup and Foundational together.
2. Backend and frontend developers split by story tasks marked [P].
3. Contract and integration test owners validate each story before merge.
