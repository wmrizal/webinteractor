from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Field as SQLField

from src.models.captured_item import CapturedItemRead
from src.models.base import DesiredState, FailureStep, RunStatus, TimestampedModel, UUIDPrimaryKeyModel
from src.models.toggle_result import ToggleResultRead


class AutomationRunRecord(UUIDPrimaryKeyModel, TimestampedModel, table=True):
    __tablename__ = "automation_runs"

    target_id: UUID = SQLField(foreign_key="automation_targets.id", nullable=False, index=True)
    requested_state: DesiredState = SQLField(nullable=False)
    status: RunStatus = SQLField(default=RunStatus.QUEUED, nullable=False)
    started_at: datetime = SQLField(default_factory=datetime.utcnow, nullable=False)
    finished_at: datetime | None = SQLField(default=None, nullable=True)
    duration_ms: int | None = SQLField(default=None, nullable=True)
    failure_step: FailureStep | None = SQLField(default=None, nullable=True)
    failure_message: str | None = SQLField(default=None, nullable=True)
    actor: str = SQLField(default="manual", nullable=False)


class CreateRunRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    target_id: UUID = Field(alias="targetId")
    requested_state: DesiredState = Field(alias="requestedState")


class AutomationRunRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: UUID
    target_id: UUID = Field(alias="targetId")
    requested_state: DesiredState = Field(alias="requestedState")
    status: RunStatus
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime | None = Field(default=None, alias="finishedAt")
    duration_ms: int | None = Field(default=None, alias="durationMs")


class RunDetails(AutomationRunRead):
    captured_items: list[CapturedItemRead] = Field(default_factory=list, alias="capturedItems")
    toggle_result: ToggleResultRead | None = Field(default=None, alias="toggleResult")
    failure_step: FailureStep | None = Field(default=None, alias="failureStep")
    failure_message: str | None = Field(default=None, alias="failureMessage")


class RunHistoryItem(AutomationRunRead):
    failure_step: FailureStep | None = Field(default=None, alias="failureStep")
    failure_message: str | None = Field(default=None, alias="failureMessage")


def serialize_run(record: AutomationRunRecord) -> AutomationRunRead:
    return AutomationRunRead.model_validate(
        {
            "id": record.id,
            "targetId": record.target_id,
            "requestedState": record.requested_state,
            "status": record.status,
            "startedAt": record.started_at,
            "finishedAt": record.finished_at,
            "durationMs": record.duration_ms,
        }
    )


def serialize_run_history(record: AutomationRunRecord) -> RunHistoryItem:
    return RunHistoryItem.model_validate(
        {
            "id": record.id,
            "targetId": record.target_id,
            "requestedState": record.requested_state,
            "status": record.status,
            "startedAt": record.started_at,
            "finishedAt": record.finished_at,
            "durationMs": record.duration_ms,
            "failureStep": record.failure_step,
            "failureMessage": record.failure_message,
        }
    )


def serialize_run_details(
    record: AutomationRunRecord,
    captured_items: list[CapturedItemRead],
    toggle_result: ToggleResultRead | None,
) -> RunDetails:
    return RunDetails.model_validate(
        {
            "id": record.id,
            "targetId": record.target_id,
            "requestedState": record.requested_state,
            "status": record.status,
            "startedAt": record.started_at,
            "finishedAt": record.finished_at,
            "durationMs": record.duration_ms,
            "capturedItems": captured_items,
            "toggleResult": toggle_result,
            "failureStep": record.failure_step,
            "failureMessage": record.failure_message,
        }
    )
