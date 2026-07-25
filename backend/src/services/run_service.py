from __future__ import annotations

import asyncio
from time import perf_counter
from uuid import UUID

from sqlmodel import Session, select

from src.api.errors import NotFoundError
from src.automation.browser_runner import BrowserRunner
from src.models.automation_run import (
    AutomationRunRead,
    AutomationRunRecord,
    CreateRunRequest,
    RunDetails,
    serialize_run,
    serialize_run_details,
)
from src.models.automation_target import AutomationTargetRecord
from src.models.base import RunStatus, utc_now
from src.models.captured_item import CapturedItemRecord, serialize_captured_item
from src.models.toggle_result import ToggleResultRecord, serialize_toggle_result
from src.observability.logging import get_logger
from src.observability.run_event_store import RunEventStore

_logger = get_logger(__name__)


class RunService:
    runner_factory = BrowserRunner

    def __init__(self, session: Session) -> None:
        self.session = session
        self.event_store = RunEventStore(session)

    def create_run(self, payload: CreateRunRequest) -> AutomationRunRead:
        target = self.session.get(AutomationTargetRecord, payload.target_id)
        if target is None:
            raise NotFoundError("Automation target was not found")

        run_record = AutomationRunRecord(
            target_id=payload.target_id,
            requested_state=payload.requested_state,
            status=RunStatus.QUEUED,
            started_at=utc_now(),
        )
        self.session.add(run_record)
        self.event_store.append(
            run_record.id,
            "run-state-changed",
            RunStatus.QUEUED,
            "Run queued",
        )
        self.session.commit()
        self.session.refresh(run_record)

        self._execute_run(run_record.id, target)

        self.session.refresh(run_record)
        return serialize_run(run_record)

    def get_run_details(self, run_id: UUID) -> RunDetails:
        run_record = self.session.get(AutomationRunRecord, run_id)
        if run_record is None:
            raise NotFoundError("Automation run was not found")

        captured = self.session.exec(
            select(CapturedItemRecord)
            .where(CapturedItemRecord.run_id == run_record.id)
            .order_by(CapturedItemRecord.captured_at.asc())
        ).all()
        toggle = self.session.exec(
            select(ToggleResultRecord).where(ToggleResultRecord.run_id == run_record.id)
        ).first()

        captured_items = [serialize_captured_item(item) for item in captured]
        toggle_result = serialize_toggle_result(toggle) if toggle else None
        return serialize_run_details(run_record, captured_items, toggle_result)

    def list_runs_for_target(self, target_id: UUID) -> list[AutomationRunRead]:
        target = self.session.get(AutomationTargetRecord, target_id)
        if target is None:
            raise NotFoundError("Automation target was not found")

        runs = self.session.exec(
            select(AutomationRunRecord)
            .where(AutomationRunRecord.target_id == target_id)
            .order_by(AutomationRunRecord.started_at.desc())
        ).all()
        return [serialize_run(run) for run in runs]

    def _execute_run(self, run_id: UUID, target: AutomationTargetRecord) -> None:
        run_record = self.session.get(AutomationRunRecord, run_id)
        if run_record is None:
            return

        run_record.status = RunStatus.RUNNING
        run_record.failure_step = None
        run_record.failure_message = None
        self.session.add(run_record)
        self.event_store.append(
            run_record.id,
            "run-state-changed",
            RunStatus.RUNNING,
            "Run started",
        )
        self.session.commit()

        started = perf_counter()

        try:
            result = asyncio.run(self.runner_factory().execute(target, run_record.requested_state))
        except Exception as exc:
            _logger.error("run_execution_crashed", extra={"event": "run-crashed", "context": {"runId": str(run_id)}})
            run_record.status = RunStatus.FAILED
            run_record.failure_message = f"Run execution crashed: {exc}"
            run_record.finished_at = utc_now()
            run_record.duration_ms = int((perf_counter() - started) * 1000)
            self.session.add(run_record)
            self.event_store.append(
                run_record.id,
                "step-failed",
                RunStatus.FAILED,
                run_record.failure_message,
                failure_step=run_record.failure_step,
            )
            self.session.commit()
            return

        for captured_item in result.captured_items:
            self.session.add(
                CapturedItemRecord(
                    run_id=run_record.id,
                    key=captured_item.key,
                    selector=captured_item.selector,
                    value=captured_item.value,
                )
            )

        if result.toggle_result is not None:
            self.session.add(
                ToggleResultRecord(
                    run_id=run_record.id,
                    state_before=result.toggle_result.state_before,
                    state_after=result.toggle_result.state_after,
                    action_taken=result.toggle_result.action_taken,
                    verification_method=result.toggle_result.verification_method,
                    verified=result.toggle_result.verified,
                )
            )

        run_record.status = result.status
        run_record.failure_step = result.failure_step
        run_record.failure_message = result.failure_message
        run_record.finished_at = utc_now()
        run_record.duration_ms = int((perf_counter() - started) * 1000)
        self.session.add(run_record)
        self.event_store.append(
            run_record.id,
            "run-state-changed",
            run_record.status,
            f"Run finished with status {run_record.status}",
            failure_step=run_record.failure_step,
        )
        if run_record.failure_message:
            self.event_store.append(
                run_record.id,
                "step-failed",
                run_record.status,
                run_record.failure_message,
                failure_step=run_record.failure_step,
            )
        self.session.commit()
