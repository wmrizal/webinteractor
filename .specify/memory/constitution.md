<!--
Sync Impact Report
- Version change: template-draft -> 1.0.0
- Modified principles:
	- Placeholder Principle 1 -> I. Spec-Driven Delivery
	- Placeholder Principle 2 -> II. Independent Value Slices
	- Placeholder Principle 3 -> III. Risk-Based Verification (NON-NEGOTIABLE)
	- Placeholder Principle 4 -> IV. Observability as a Feature
	- Placeholder Principle 5 -> V. Secure and Reversible Change
- Added sections:
	- Engineering Constraints
	- Delivery Workflow & Quality Gates
- Removed sections:
	- None
- Templates requiring updates:
	- .specify/templates/plan-template.md: ✅ updated
	- .specify/templates/spec-template.md: ✅ updated
	- .specify/templates/tasks-template.md: ✅ updated
	- .specify/templates/commands/*.md: ⚠ pending (directory not present)
- Follow-up TODOs:
	- None
-->

# WebInteractor Constitution

## Core Principles

### I. Spec-Driven Delivery
Every feature MUST begin with a written specification that defines user stories,
functional requirements, measurable success criteria, and explicit assumptions.
Implementation work MUST trace to approved specification artifacts.
Rationale: shared intent reduces rework and prevents accidental scope drift.

### II. Independent Value Slices
Work MUST be organized into independently testable user stories where each story
can deliver user-visible value on its own. Plans and tasks MUST preserve story-level
independence and avoid cross-story coupling unless explicitly justified.
Rationale: independent slices enable faster validation, safer rollout, and
incremental delivery.

### III. Risk-Based Verification (NON-NEGOTIABLE)
All behavior changes MUST include automated verification at the highest-value
layer for the risk involved (unit, integration, or contract). Bug fixes MUST
include a regression test unless technically impossible; exceptions MUST be
documented in the plan's Complexity Tracking section.
Rationale: verification depth must match risk while keeping delivery practical.

### IV. Observability as a Feature
New or changed workflows MUST emit actionable diagnostics (structured logs,
error context, and clear failure signals) sufficient for triage without
reproducing the issue locally. Operationally significant flows MUST define
basic success/failure signals in specification or quickstart artifacts.
Rationale: maintainability and incident response depend on first-class visibility.

### V. Secure and Reversible Change
Changes MUST follow least-privilege and fail-safe defaults, and they MUST define
a rollback or recovery path for high-impact behavior changes. Secrets MUST never
be committed, and security-relevant assumptions MUST be stated explicitly.
Rationale: safe iteration requires both prevention (secure defaults) and recovery
(reversibility).

## Engineering Constraints

- Plans MUST document language/runtime version and primary dependencies.
- Performance or resource constraints MUST be captured when relevant to user value.
- Interfaces that affect other components MUST include explicit contract notes.
- Any intentional complexity increase MUST include a rejected simpler alternative.

## Delivery Workflow & Quality Gates

- Constitution Check in plan artifacts MUST pass before Phase 0 research and be
	revalidated after Phase 1 design.
- Specifications MUST include edge cases and assumptions before planning begins.
- Tasks MUST be grouped by user story and include paths for all implementation
	and validation work.
- Pull requests MUST confirm constitution compliance, test evidence, and operational
	impact notes for changed behavior.

## Governance

This constitution supersedes conflicting local conventions for specification,
planning, and execution workflows.

Amendment process:
1. Propose a constitution change in a dedicated pull request.
2. Include rationale, impacted templates, and migration guidance.
3. Obtain maintainer approval before merge.

Versioning policy:
- MAJOR: Removal or incompatible redefinition of a principle or governance rule.
- MINOR: New principle/section or materially expanded mandatory guidance.
- PATCH: Clarifications, wording improvements, and non-semantic edits.

Compliance review expectations:
- Every plan MUST document Constitution Check outcomes.
- Every task set MUST reflect verification and operational impact work where applicable.
- Reviewers MUST block merges that violate NON-NEGOTIABLE requirements.

**Version**: 1.0.0 | **Ratified**: 2026-05-21 | **Last Amended**: 2026-05-21
