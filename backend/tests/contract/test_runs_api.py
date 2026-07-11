from __future__ import annotations

from uuid import UUID

from sqlmodel import Session

from src.automation.browser_runner import BrowserRunResult, CapturedValue, ToggleOutcome
from src.lib.db import get_engine
from src.models.automation_target import AutomationTargetRecord
from src.models.base import DesiredState, ToggleAction, ToggleObservedState, ToggleVerificationMethod
from src.services.run_service import RunService


class FakeRunner:
    async def execute(self, target: AutomationTargetRecord, requested_state: DesiredState) -> BrowserRunResult:
        return BrowserRunResult(
            status="success",
            captured_items=[CapturedValue(key="featureName", selector="#feature-name", value=target.name)],
            toggle_result=ToggleOutcome(
                state_before=ToggleObservedState.OFF,
                state_after=ToggleObservedState.ON,
                action_taken=ToggleAction.TOGGLE_ONCE,
                verification_method=ToggleVerificationMethod.TEXT_LABEL,
                verified=True,
            ),
        )


def create_target_record() -> UUID:
    with Session(get_engine()) as session:
        record = AutomationTargetRecord(
            name="Checkout flag",
            base_url="https://example.test",
            page_path="/flags",
            auth_profile="qa-session",
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


def test_run_trigger_and_detail_endpoints(contract_client, monkeypatch):
    monkeypatch.setattr(RunService, "runner_factory", FakeRunner)
    target_id = create_target_record()

    create_response = contract_client.post(
        "/runs",
        json={"targetId": str(target_id), "requestedState": "on"},
    )
    assert create_response.status_code == 202
    queued_run = create_response.json()
    assert queued_run["targetId"] == str(target_id)
    assert queued_run["requestedState"] == "on"

    detail_response = contract_client.get(f"/runs/{queued_run['id']}")
    assert detail_response.status_code == 200
    detail_payload = detail_response.json()
    assert detail_payload["status"] == "success"
    assert detail_payload["toggleResult"]["stateAfter"] == "on"
    assert detail_payload["capturedItems"][0]["value"] == "Checkout flag"
