from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import JSON, Column
from sqlmodel import Field as SQLField
from sqlmodel import Session, select

from src.models.base import FailureStep, RunStatus, UUIDPrimaryKeyModel, utc_now


class RunEventRecord(UUIDPrimaryKeyModel, table=True):
    __tablename__ = "run_events"

    run_id: UUID = SQLField(foreign_key="automation_runs.id", nullable=False, index=True)
    event_type: str = SQLField(nullable=False)
    status: RunStatus = SQLField(nullable=False)
    failure_step: FailureStep | None = SQLField(default=None, nullable=True)
    message: str = SQLField(nullable=False)
    timestamp: datetime = SQLField(default_factory=utc_now, nullable=False)
    context: dict[str, Any] = SQLField(default_factory=dict, sa_column=Column(JSON, nullable=False))


class RunEventRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    run_id: UUID = Field(alias="runId")
    event_type: str = Field(alias="eventType")
    status: RunStatus
    failure_step: FailureStep | None = Field(default=None, alias="failureStep")
    message: str
    timestamp: datetime
    context: dict[str, Any]


class RunEventStore:
    def __init__(self, session: Session) -> None:
        self.session = session

    def append(
        self,
        run_id: UUID,
        event_type: str,
        status: RunStatus,
        message: str,
        *,
        failure_step: FailureStep | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.session.add(
            RunEventRecord(
                run_id=run_id,
                event_type=event_type,
                status=status,
                failure_step=failure_step,
                message=message,
                context=context or {},
            )
        )

    def list_for_run(self, run_id: UUID) -> list[RunEventRead]:
        rows = self.session.exec(
            select(RunEventRecord)
            .where(RunEventRecord.run_id == run_id)
            .order_by(RunEventRecord.timestamp.asc())
        ).all()
        return [
            RunEventRead.model_validate(
                {
                    "runId": row.run_id,
                    "eventType": row.event_type,
                    "status": row.status,
                    "failureStep": row.failure_step,
                    "message": row.message,
                    "timestamp": row.timestamp,
                    "context": row.context,
                }
            )
            for row in rows
        ]
