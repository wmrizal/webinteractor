from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.base import FailureStep, RunStatus, utc_now


class RunEventType(StrEnum):
    RUN_STATE_CHANGED = "run-state-changed"
    STEP_STARTED = "step-started"
    STEP_COMPLETED = "step-completed"
    STEP_FAILED = "step-failed"


class RunEvent(BaseModel):
    run_id: UUID
    event_type: RunEventType
    status: RunStatus
    failure_step: FailureStep | None = None
    message: str
    timestamp: datetime = Field(default_factory=utc_now)
    context: dict[str, Any] = Field(default_factory=dict)
