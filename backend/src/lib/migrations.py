from sqlmodel import SQLModel

from src.lib.db import get_engine


def bootstrap_database() -> None:
    SQLModel.metadata.create_all(get_engine())
