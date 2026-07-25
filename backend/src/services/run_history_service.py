from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select

from src.api.errors import NotFoundError
from src.models.automation_run import (
    AutomationRunRecord,
    RunDetails,
    RunHistoryItem,
    serialize_run_details,
    serialize_run_history,
)
from src.models.automation_target import AutomationTargetRecord
from src.models.captured_item import CapturedItemRecord, serialize_captured_item
from src.models.toggle_result import ToggleResultRecord, serialize_toggle_result
from src.observability.run_event_store import RunEventRead, RunEventStore


class RunHistoryDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    run: RunDetails
    events: list[RunEventRead]


class RunHistoryService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.event_store = RunEventStore(session)

    def list_history_for_target(self, target_id: UUID) -> list[RunHistoryItem]:
        target = self.session.get(AutomationTargetRecord, target_id)
        if target is None:
            raise NotFoundError("Automation target was not found")

        runs = self.session.exec(
            select(AutomationRunRecord)
            .where(AutomationRunRecord.target_id == target_id)
            .order_by(AutomationRunRecord.started_at.desc())
        ).all()
        return [serialize_run_history(run) for run in runs]

    def get_run_history_details(self, run_id: UUID) -> RunHistoryDetails:
        run = self.session.get(AutomationRunRecord, run_id)
        if run is None:
            raise NotFoundError("Automation run was not found")

        captured = self.session.exec(
            select(CapturedItemRecord)
            .where(CapturedItemRecord.run_id == run.id)
            .order_by(CapturedItemRecord.captured_at.asc())
        ).all()
        toggle = self.session.exec(
            select(ToggleResultRecord).where(ToggleResultRecord.run_id == run.id)
        ).first()

        details = serialize_run_details(
            run,
            [serialize_captured_item(item) for item in captured],
            serialize_toggle_result(toggle) if toggle else None,
        )
        events = self.event_store.list_for_run(run.id)
        return RunHistoryDetails(run=details, events=events)
