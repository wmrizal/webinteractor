from __future__ import annotations

import os
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

DEFAULT_DATABASE_URL = "sqlite:///./data/app.db"


def database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def _sqlite_connect_args(resolved_database_url: str) -> dict[str, bool]:
    return {"check_same_thread": False} if resolved_database_url.startswith("sqlite") else {}


def _ensure_sqlite_parent(resolved_database_url: str) -> None:
    if not resolved_database_url.startswith("sqlite:///"):
        return

    database_path = resolved_database_url.removeprefix("sqlite:///")
    if not database_path or database_path == ":memory:":
        return

    Path(database_path).parent.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    resolved_database_url = database_url()
    _ensure_sqlite_parent(resolved_database_url)
    return create_engine(
        resolved_database_url,
        connect_args=_sqlite_connect_args(resolved_database_url),
        echo=False,
    )


def reset_engine_cache() -> None:
    get_engine.cache_clear()


def init_db() -> None:
    SQLModel.metadata.create_all(get_engine())


def get_session() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session
