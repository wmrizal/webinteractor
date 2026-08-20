# Quickstart: Frontend Landing Page

**Feature**: 002-frontend-landing-page
**Date**: 2026-07-30

## Overview

This guide explains how to run, test, and verify the landing page feature locally.

---

## Prerequisites

- Node.js 20+ installed
- Frontend dependencies installed (`cd frontend && npm install`)
- Backend running on `http://localhost:8000` (only needed for Targets/Runs/History pages — **not** required to view the landing page itself)

---

## Running the Frontend

```powershell
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser. You should see the **landing page** (not the Runs page). The page loads with no network requests.

---

## What to Verify Manually

| Check | Expected result |
|---|---|
| Visit `http://localhost:5173/` | Landing page renders with application title and three section cards |
| Read each card | Targets, Runs, Run History cards each have a description and how-to steps |
| Click "Go to Targets" (or equivalent) | Navigates to `/targets` |
| Click "Go to Runs" | Navigates to `/runs` |
| Click "Go to Run History" | Navigates to `/history` |
| Nav bar link "Home" | Returns to `/` from any page |
| Visit `http://localhost:5173/unknown-path` | Redirects to `/` (landing page) |
| No network tab activity on `/` | DevTools Network tab shows zero API requests |

---

## Running Tests

```powershell
cd frontend
npm run test
```

The test file `tests/integration/landing-page.spec.tsx` covers:
- Landing page renders at the `/` route
- All three section card headings present
- Each card has ≥ 2 how-to steps
- Each CTA navigates to the correct route

---

## File Locations

| File | Purpose |
|---|---|
| `frontend/src/pages/LandingPage.tsx` | New landing page component |
| `frontend/src/components/layout/NavBar.tsx` | New shared navigation bar |
| `frontend/src/App.tsx` | Updated with `/` route and NavBar wrapper |
| `frontend/src/styles.css` | Updated with landing grid and nav styles |
| `frontend/tests/integration/landing-page.spec.tsx` | Integration tests |

---

## Rollback

If this feature needs to be reverted, the change to `App.tsx` is the only routing
change. Restoring the previous wildcard redirect (`<Navigate to="/runs" replace />`)
is a one-line edit that removes the landing page from the routing tree.
