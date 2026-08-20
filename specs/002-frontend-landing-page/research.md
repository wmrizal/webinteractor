# Research: Frontend Landing Page

**Feature**: 002-frontend-landing-page
**Date**: 2026-07-30

## Summary

All decisions below resolve from the existing codebase and well-established React patterns.
No external research was required — there are no NEEDS CLARIFICATION items in the spec.

---

## Decision 1: Route Strategy

**Decision**: Add an explicit `/` route in `App.tsx` that renders `<LandingPage />`.
Change the wildcard fallback from `<Navigate to="/runs" />` to `<Navigate to="/" />`.

**Rationale**: React Router DOM v6 supports nested and indexed routes cleanly.
Adding a `/` `<Route>` is the canonical way to define a root page in a v6 SPA.
The existing wildcard redirect (`* → /runs`) bypasses the root entirely; replacing
its target with `/` means unknown URLs still fall back gracefully to the landing page.

**Alternatives considered**:
- Keeping `* → /runs` and adding an `index` route — rejected because it changes
  the meaning of "unknown paths" differently per user expectation.
- Making `/runs` the index route — rejected because it contradicts the spec requirement
  for an orientation landing page at root.

---

## Decision 2: Navigation Bar

**Decision**: Introduce a lightweight `NavBar.tsx` component that wraps the `<Routes>`
in `App.tsx`, providing links to Home (`/`), Targets (`/targets`), Runs (`/runs`),
and Run History (`/history`).

**Rationale**: The existing codebase has no shared navigation. Each page is self-contained.
The spec requires that users can return to the landing page from any page (FR-006).
A top-level nav bar is the standard pattern for a React SPA with 4 routes.
Using React Router's `<NavLink>` provides active-state styling with minimal code.

**Alternatives considered**:
- In-page "back" buttons on each page — rejected because it requires changes to every
  existing page component and still doesn't let users jump between sections.
- A sidebar — rejected as over-engineered for 4 links; also inconsistent with the
  existing full-width page-shell layout.

---

## Decision 3: Styling Approach

**Decision**: Reuse existing vanilla CSS classes (`.page-shell`, `.hero-card`, `.card`,
`.eyebrow`) and add only the new classes needed for the section card grid and nav bar.
No CSS framework or new npm package is introduced.

**Rationale**: The project uses plain CSS in `styles.css` with a coherent design system
(warm gradient background, glass-effect cards, Segoe UI, accent `#9a5b25`). The landing
page must feel visually consistent. New classes added: `.landing-grid` (CSS grid for
section cards), `.section-card` (card variant with how-to list), `.nav-bar` (top bar).

**Alternatives considered**:
- Tailwind CSS or CSS Modules — rejected; no framework is present and this feature
  is not the right moment to introduce one.
- Inline styles — rejected; inconsistent with the existing class-based approach.

---

## Decision 4: Section Card Content

**Decision**: Each card covers one frontend section with: an icon/emoji (decorative,
no alt-text requirement since it is `aria-hidden`), a section title, a one-sentence
description, a two-to-three-step how-to list, and a `<Link>` button to the section.

**Content mapping** (derived from codebase analysis):

| Section      | Route      | Description                                                 | How-To Steps                                                                        |
|--------------|------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Targets      | `/targets` | Store browser URLs and toggle selectors for reuse           | 1. Fill in Base URL + page path + selector. 2. Save. 3. Reuse in any Run.           |
| Runs         | `/runs`    | Trigger a one-off automation run against a saved target     | 1. Pick a Target. 2. Choose desired state (on/off). 3. Click Run.                   |
| Run History  | `/history` | Browse past run results, statuses, and captured screenshots | 1. Select a target from the list. 2. Choose a past run. 3. Inspect toggle results.  |

**Rationale**: Derived directly from the existing pages (`TargetsPage.tsx`, `RunPage.tsx`,
`RunHistoryPage.tsx`) and API routes. No invention required.

---

## Decision 5: Testing Strategy

**Decision**: Integration tests using Vitest + Testing Library React + MemoryRouter,
placed in `frontend/tests/integration/landing-page.spec.tsx`.

Tests to write:
1. Landing page renders at `/` route (FR-001)
2. All three section cards are present with correct headings (FR-003)
3. Each card contains at least two how-to steps (FR-004)
4. Each card's CTA navigates to the correct route (FR-005, FR-002)

**Rationale**: The existing test suite (`run-execution.spec.tsx`, `targets.spec.tsx`)
follows the same pattern: render with a router wrapper and assert on screen content.
No new test infrastructure is needed.

**Alternatives considered**:
- Unit tests on the component in isolation — acceptable but integration-level tests
  (with router context) are higher value here because FR-005 (navigation) requires routing.
- E2E Playwright tests — out of scope for this feature; the existing frontend tests
  don't include Playwright.
