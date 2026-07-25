from __future__ import annotations

from uuid import UUID

from sqlmodel import Session

from src.automation.browser_runner import BrowserRunResult
from src.lib.db import get_engine
from src.models.automation_target import AutomationTargetRecord
from src.models.base import DesiredState, FailureStep, RunStatus
from src.services.run_service import RunService


class FakeFailingRunner:
    async def execute(self, target: AutomationTargetRecord, requested_state: DesiredState) -> BrowserRunResult:
        return BrowserRunResult(
            status=RunStatus.FAILED,
            failure_step=FailureStep.TOGGLE,
            failure_message=f"Toggle failed for {target.name} ({requested_state})",
        )


def create_target_record(target_page_url: str) -> UUID:
    with Session(get_engine()) as session:
        record = AutomationTargetRecord(
            name="Failure scenario target",
            base_url=target_page_url,
            page_path="",
            auth_profile=None,
            extraction_rules=[{"key": "featureName", "selector": "#feature-name"}],
            toggle_rule={
                "controlSelector": "#feature-toggle",
                "stateSelector": "#feature-state",
                "verificationMethod": "text-label",
            },
            default_desired_state=DesiredState.OFF,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id


def test_run_failure_diagnostics_capture_failure_step(
    integration_client,
    target_page_factory,
    monkeypatch,
):
    monkeypatch.setattr(RunService, "runner_factory", FakeFailingRunner)
    target_id = create_target_record(target_page_factory(initial_state="off"))

    response = integration_client.post(
        "/runs",
        json={"targetId": str(target_id), "requestedState": "on"},
    )
    assert response.status_code == 202
    run_id = response.json()["id"]

    run_detail = integration_client.get(f"/runs/{run_id}")
    assert run_detail.status_code == 200
    detail_payload = run_detail.json()
    assert detail_payload["status"] == "failed"
    assert detail_payload["failureStep"] == "toggle"
    assert "Toggle failed" in detail_payload["failureMessage"]

    history_response = integration_client.get(f"/runs/{run_id}/history")
    assert history_response.status_code == 200
    history_payload = history_response.json()

    assert history_payload["run"]["id"] == run_id
    assert history_payload["run"]["failureStep"] == "toggle"
    assert any(event["eventType"] == "step-failed" for event in history_payload["events"])
