# UI Route Contract: Frontend Landing Page

**Feature**: 002-frontend-landing-page
**Date**: 2026-07-30

## Overview

This document defines the client-side route contract for the SPA after this feature
is implemented. All routes are served by React Router DOM v6 in `App.tsx`.

---

## Route Table

| Path          | Component         | Behaviour                                                   |
|---------------|-------------------|-------------------------------------------------------------|
| `/`           | `LandingPage`     | **NEW** — Static landing page; no API calls                 |
| `/targets`    | `TargetsPage`     | Existing — list and manage automation targets               |
| `/runs`       | `RunPage`         | Existing — trigger and monitor a run                        |
| `/history`    | `RunHistoryPage`  | Existing — browse past run history                          |
| `*` (wildcard)| `Navigate to /`   | **CHANGED** — previously redirected to `/runs`; now to `/`  |

---

## Navigation Contract

The shared `NavBar` component must render the following links on every page:

| Link label    | Target path  |
|---------------|--------------|
| Home          | `/`          |
| Targets       | `/targets`   |
| Runs          | `/runs`      |
| Run History   | `/history`   |

Active link MUST receive a visually distinct style (via React Router `<NavLink>`
`isActive` class or `aria-current="page"`).

---

## Stability Guarantee

- The `/` route is a new stable entry point. Existing bookmarks to `/targets`,
  `/runs`, and `/history` continue to work without change.
- The wildcard redirect change (`/runs` → `/`) is the only breaking change;
  users who previously bookmarked root (`/`) and expected `/runs` will now
  see the landing page instead. This is the intended behaviour per the spec.
