from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Field as SQLField

from src.models.base import (
    ToggleAction,
    ToggleObservedState,
    ToggleVerificationMethod,
    UUIDPrimaryKeyModel,
)


class ToggleResultRecord(UUIDPrimaryKeyModel, table=True):
    __tablename__ = "toggle_results"

    run_id: UUID = SQLField(
        foreign_key="automation_runs.id",
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True},
    )
    state_before: ToggleObservedState = SQLField(nullable=False)
    state_after: ToggleObservedState = SQLField(nullable=False)
    action_taken: ToggleAction = SQLField(nullable=False)
    verification_method: ToggleVerificationMethod = SQLField(nullable=False)
    verified: bool = SQLField(nullable=False)


class ToggleResultRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    state_before: ToggleObservedState = Field(alias="stateBefore")
    state_after: ToggleObservedState = Field(alias="stateAfter")
    action_taken: ToggleAction = Field(alias="actionTaken")
    verified: bool


def serialize_toggle_result(record: ToggleResultRecord) -> ToggleResultRead:
    return ToggleResultRead.model_validate(
        {
            "stateBefore": record.state_before,
            "stateAfter": record.state_after,
            "actionTaken": record.action_taken,
            "verified": record.verified,
        }
    )
