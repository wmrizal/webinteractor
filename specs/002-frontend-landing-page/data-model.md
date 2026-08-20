# Data Model: Frontend Landing Page

**Feature**: 002-frontend-landing-page
**Date**: 2026-07-30

## Summary

The landing page is entirely static. It introduces **no new data entities**, no new
database tables, and makes no backend API calls. All content is hard-coded in the
React component.

---

## UI Data Structure

Although there are no persisted entities, the landing page operates over a conceptual
in-code `SectionCard` shape used to render each card. Documenting it here clarifies
the component interface.

### SectionCard (compile-time constant, not a model)

| Field        | Type       | Description                                          |
|--------------|------------|------------------------------------------------------|
| `title`      | `string`   | Section name displayed as the card heading           |
| `description`| `string`   | One-sentence explanation of the section's purpose    |
| `steps`      | `string[]` | Ordered how-to steps (minimum 2)                     |
| `route`      | `string`   | React Router path to navigate to on CTA click        |
| `ctaLabel`   | `string`   | Label text for the call-to-action button/link        |

**Implementation note**: This shape is defined as a local constant array inside
`LandingPage.tsx` — it does not need to be exported or shared.

---

## State Transitions

None. The landing page has no interactive state beyond the router navigation provided
by React Router DOM's `<Link>` component.

---

## Existing Entities (unchanged)

The following entities exist in the backend and frontend but are **not touched** by
this feature. Listed for completeness.

| Entity            | Owned by | Used on landing page |
|-------------------|----------|----------------------|
| AutomationTarget  | Backend  | No                   |
| AutomationRun     | Backend  | No                   |
| RunHistoryItem    | Backend  | No                   |
