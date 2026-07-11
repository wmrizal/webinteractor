from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class DesiredState(StrEnum):
    ON = "on"
    OFF = "off"


class RunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    NO_CHANGE_NEEDED = "no-change-needed"


class FailureStep(StrEnum):
    NAVIGATE = "navigate"
    AUTHENTICATE = "authenticate"
    EXTRACT = "extract"
    TOGGLE = "toggle"
    VERIFY = "verify"


class ToggleObservedState(StrEnum):
    ON = "on"
    OFF = "off"
    UNKNOWN = "unknown"


class ToggleAction(StrEnum):
    NONE = "none"
    TOGGLE_ONCE = "toggle-once"
    RETRY_TOGGLE = "retry-toggle"


class ToggleVerificationMethod(StrEnum):
    DOM_ATTRIBUTE = "dom-attribute"
    TEXT_LABEL = "text-label"
    ARIA_CHECKED = "aria-checked"


def utc_now() -> datetime:
    return datetime.now(UTC)


class TimestampedModel(SQLModel):
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=utc_now, nullable=False)


class UUIDPrimaryKeyModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
