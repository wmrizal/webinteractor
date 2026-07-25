from __future__ import annotations

from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, delete

from src.lib.db import get_engine, init_db, reset_engine_cache
from src.main import app


@pytest.fixture()
def integration_client(tmp_path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    database_path = tmp_path / "integration-test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path.as_posix()}")
    reset_engine_cache()
    init_db()

    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_database() -> Iterator[None]:
    yield

    with Session(get_engine()) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.exec(delete(table))
        session.commit()


@pytest.fixture()
def wait_for_terminal_run(integration_client: TestClient) -> Callable[[str], dict]:
    def _wait(run_id: str) -> dict:
        for _ in range(20):
            response = integration_client.get(f"/runs/{run_id}")
            payload = response.json()
            if payload["status"] in {"success", "failed", "no-change-needed"}:
                return payload
        raise AssertionError(f"Run {run_id} did not reach a terminal state")

    return _wait
