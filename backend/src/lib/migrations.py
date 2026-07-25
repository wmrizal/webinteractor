from sqlmodel import SQLModel

from src.lib.db import get_engine

# Import all model modules so SQLModel metadata is fully registered.
from src.models import automation_run, automation_target, captured_item, toggle_result  # noqa: F401
from src.observability import run_event_store  # noqa: F401


def bootstrap_database() -> None:
    SQLModel.metadata.create_all(get_engine())
