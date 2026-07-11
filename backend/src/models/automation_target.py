from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urlparse
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import JSON, Column
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel

from src.models.base import DesiredState, TimestampedModel, UUIDPrimaryKeyModel
from src.models.rules import CapturedItemRule, ToggleControlRule


class AutomationTargetRecord(UUIDPrimaryKeyModel, TimestampedModel, table=True):
    __tablename__ = "automation_targets"

    name: str = SQLField(index=True, nullable=False, sa_column_kwargs={"unique": True})
    base_url: str = SQLField(nullable=False)
    page_path: str = SQLField(default="/", nullable=False)
    auth_profile: str | None = SQLField(default=None, nullable=True)
    extraction_rules: list[dict[str, Any]] = SQLField(
        default_factory=list,
        sa_column=Column(JSON, nullable=False),
    )
    toggle_rule: dict[str, Any] = SQLField(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False),
    )
    default_desired_state: DesiredState = SQLField(nullable=False)


class AutomationTargetPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    name: str = Field(min_length=1, max_length=100)
    base_url: str = Field(alias="baseUrl")
    page_path: str = Field(default="/", alias="pagePath")
    auth_profile: str | None = Field(default=None, alias="authProfile")
    extraction_rules: list[CapturedItemRule] = Field(alias="extractionRules", min_length=1)
    toggle_rule: ToggleControlRule = Field(alias="toggleRule")
    default_desired_state: DesiredState = Field(alias="defaultDesiredState")

    @field_validator("name", "page_path")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Value is required")
        return stripped

    @field_validator("auth_profile")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @field_validator("base_url")
    @classmethod
    def validate_https_url(cls, value: str) -> str:
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("baseUrl must be a valid HTTPS URL")
        return value.rstrip("/")


class AutomationTargetCreate(AutomationTargetPayload):
    pass


class AutomationTargetUpdate(AutomationTargetPayload):
    pass


class AutomationTargetRead(AutomationTargetPayload):
    id: UUID
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


def serialize_target(record: AutomationTargetRecord) -> AutomationTargetRead:
    return AutomationTargetRead.model_validate(
        {
            "id": record.id,
            "name": record.name,
            "baseUrl": record.base_url,
            "pagePath": record.page_path,
            "authProfile": record.auth_profile,
            "extractionRules": record.extraction_rules,
            "toggleRule": record.toggle_rule,
            "defaultDesiredState": record.default_desired_state,
            "createdAt": record.created_at,
            "updatedAt": record.updated_at,
        }
    )


def payload_to_record_data(payload: AutomationTargetPayload) -> dict[str, Any]:
    return {
        "name": payload.name,
        "base_url": payload.base_url,
        "page_path": payload.page_path,
        "auth_profile": payload.auth_profile,
        "extraction_rules": [rule.model_dump() for rule in payload.extraction_rules],
        "toggle_rule": payload.toggle_rule.model_dump(by_alias=True),
        "default_desired_state": payload.default_desired_state,
    }
