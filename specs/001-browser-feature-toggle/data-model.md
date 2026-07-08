# Data Model: Browser Feature Toggle Automation

## Entity: AutomationTarget

- id: UUID (primary key)
- name: string (1-100 chars, unique per workspace)
- baseUrl: string (HTTPS URL)
- pagePath: string
- authProfile: string (reference to external auth config)
- extractionRules: JSON array of `CapturedItemRule`
- toggleRule: JSON object `ToggleControlRule`
- defaultDesiredState: enum (`on`, `off`)
- createdAt: datetime (UTC)
- updatedAt: datetime (UTC)

Validation rules:
- `baseUrl` MUST be a valid absolute HTTPS URL.
- At least one extraction rule is required.
- Toggle rule selector and state-detection selector are required.

## Entity: AutomationRun

- id: UUID (primary key)
- targetId: UUID (foreign key -> AutomationTarget.id)
- requestedState: enum (`on`, `off`)
- status: enum (`queued`, `running`, `success`, `failed`, `no-change-needed`)
- startedAt: datetime (UTC)
- finishedAt: datetime nullable (UTC)
- durationMs: integer nullable
- failureStep: enum nullable (`navigate`, `authenticate`, `extract`, `toggle`, `verify`)
- failureMessage: string nullable
- actor: string (user identifier)

Validation rules:
- `requestedState` is mandatory.
- `finishedAt` and `durationMs` are required when status is terminal.
- `failureStep` and `failureMessage` are required when status is `failed`.

State transitions:
- `queued` -> `running`
- `running` -> `success`
- `running` -> `failed`
- `running` -> `no-change-needed`

## Entity: CapturedItem

- id: UUID (primary key)
- runId: UUID (foreign key -> AutomationRun.id)
- key: string (1-100 chars)
- selector: string
- value: string
- capturedAt: datetime (UTC)

Validation rules:
- `key`, `selector`, and `value` are mandatory.
- `(runId, key)` should be unique per run.

## Entity: ToggleResult

- id: UUID (primary key)
- runId: UUID (foreign key -> AutomationRun.id, unique)
- stateBefore: enum (`on`, `off`, `unknown`)
- stateAfter: enum (`on`, `off`, `unknown`)
- actionTaken: enum (`none`, `toggle-once`, `retry-toggle`)
- verificationMethod: enum (`dom-attribute`, `text-label`, `aria-checked`)
- verified: boolean

Validation rules:
- `verified` MUST be true for status `success` and `no-change-needed`.
- `stateAfter` SHOULD equal requested state for non-failed runs.

## Relationships

- One `AutomationTarget` has many `AutomationRun`.
- One `AutomationRun` has many `CapturedItem`.
- One `AutomationRun` has one `ToggleResult`.
