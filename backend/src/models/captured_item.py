from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Field as SQLField

from src.models.base import UUIDPrimaryKeyModel, utc_now


class CapturedItemRecord(UUIDPrimaryKeyModel, table=True):
    __tablename__ = "captured_items"

    run_id: UUID = SQLField(foreign_key="automation_runs.id", index=True, nullable=False)
    key: str = SQLField(nullable=False)
    selector: str = SQLField(nullable=False)
    value: str = SQLField(nullable=False)
    captured_at: datetime = SQLField(default_factory=utc_now, nullable=False)


class CapturedItemRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    key: str
    selector: str
    value: str
    captured_at: datetime = Field(alias="capturedAt")


def serialize_captured_item(record: CapturedItemRecord) -> CapturedItemRead:
    return CapturedItemRead.model_validate(
        {
            "key": record.key,
            "selector": record.selector,
            "value": record.value,
            "capturedAt": record.captured_at,
        }
    )
