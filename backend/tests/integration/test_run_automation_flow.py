from __future__ import annotations

from pathlib import Path
from uuid import UUID

from sqlmodel import Session

from src.lib.db import get_engine
from src.models.automation_target import AutomationTargetRecord
from src.models.base import DesiredState


def create_target_record(target_page_url: str) -> UUID:
    target_name = "Checkout flag on" if "-on.html" in target_page_url else "Checkout flag off"
    with Session(get_engine()) as session:
        record = AutomationTargetRecord(
            name=target_name,
            base_url=target_page_url,
            page_path="",
            auth_profile=None,
            extraction_rules=[
                {"key": "featureName", "selector": "#feature-name"},
                {"key": "featureState", "selector": "#feature-state"},
            ],
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


def test_run_automation_success_and_no_change_paths(
    integration_client,
    wait_for_terminal_run,
    target_page_factory,
):
    off_target_id = create_target_record(target_page_factory(initial_state="off"))
    on_target_id = create_target_record(target_page_factory(initial_state="on"))

    success_response = integration_client.post(
        "/runs",
        json={"targetId": str(off_target_id), "requestedState": "on"},
    )
    assert success_response.status_code == 202
    success_detail = wait_for_terminal_run(success_response.json()["id"])
    assert success_detail["status"] == "success"
    assert success_detail["toggleResult"]["stateBefore"] == "off"
    assert success_detail["toggleResult"]["stateAfter"] == "on"
    assert success_detail["toggleResult"]["actionTaken"] == "toggle-once"
    assert any(item["key"] == "featureName" for item in success_detail["capturedItems"])

    no_change_response = integration_client.post(
        "/runs",
        json={"targetId": str(on_target_id), "requestedState": "on"},
    )
    assert no_change_response.status_code == 202
    no_change_detail = wait_for_terminal_run(no_change_response.json()["id"])
    assert no_change_detail["status"] == "no-change-needed"
    assert no_change_detail["toggleResult"]["stateBefore"] == "on"
    assert no_change_detail["toggleResult"]["stateAfter"] == "on"
    assert no_change_detail["toggleResult"]["actionTaken"] == "none"
