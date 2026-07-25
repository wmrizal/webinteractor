from __future__ import annotations

from pathlib import Path
from uuid import UUID

from sqlmodel import Session

from src.lib.db import get_engine
from src.models.automation_target import AutomationTargetRecord
from src.models.base import DesiredState


def create_reversible_target(target_page_url: str) -> UUID:
    with Session(get_engine()) as session:
        record = AutomationTargetRecord(
            name="Reversal test target",
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
            default_desired_state=DesiredState.ON,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id


def test_toggle_reversal_workflow(
    integration_client,
    wait_for_terminal_run,
    target_page_factory,
):
    target_id = create_reversible_target(target_page_factory(initial_state="off"))

    on_response = integration_client.post(
        "/runs",
        json={"targetId": str(target_id), "requestedState": "on"},
    )
    assert on_response.status_code == 202
    on_run = wait_for_terminal_run(on_response.json()["id"])
    assert on_run["status"] == "success"
    assert on_run["toggleResult"]["stateAfter"] == "on"

    off_response = integration_client.post(
        "/runs",
        json={"targetId": str(target_id), "requestedState": "off"},
    )
    assert off_response.status_code == 202
    off_run = wait_for_terminal_run(off_response.json()["id"])
    assert off_run["status"] in {"success", "no-change-needed"}
    assert off_run["toggleResult"]["stateAfter"] == "off"
