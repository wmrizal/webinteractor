from __future__ import annotations

import threading
from uuid import UUID

from sqlmodel import Session

from src.lib.db import get_engine
from src.models.automation_target import AutomationTargetRecord
from src.models.base import DesiredState


def create_target(name: str, page_url: str) -> UUID:
    with Session(get_engine()) as session:
        record = AutomationTargetRecord(
            name=name,
            base_url=page_url,
            page_path="",
            auth_profile=None,
            extraction_rules=[{"key": "featureState", "selector": "#feature-state"}],
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


def test_concurrent_manual_runs(
    integration_client,
    wait_for_terminal_run,
    target_page_factory,
):
    target_ids = [
        create_target(f"Concurrent target {i}", target_page_factory(initial_state="off"))
        for i in range(3)
    ]

    run_ids: list[str] = []
    errors: list[str] = []
    lock = threading.Lock()

    def trigger_run(target_id: UUID) -> None:
        response = integration_client.post(
            "/runs",
            json={"targetId": str(target_id), "requestedState": "on"},
        )
        with lock:
            if response.status_code == 202:
                run_ids.append(response.json()["id"])
            else:
                errors.append(f"Unexpected status {response.status_code}")

    threads = [threading.Thread(target=trigger_run, args=(tid,)) for tid in target_ids]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=120)

    assert not errors, f"Run trigger errors: {errors}"
    assert len(run_ids) == 3

    for run_id in run_ids:
        detail = wait_for_terminal_run(run_id)
        assert detail["status"] in {"success", "failed", "no-change-needed"}
