from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.models.base import ToggleVerificationMethod


class CapturedItemRule(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    selector: str = Field(min_length=1)

    @field_validator("key", "selector")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Value is required")
        return stripped


class ToggleControlRule(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    control_selector: str = Field(alias="controlSelector", min_length=1)
    state_selector: str = Field(alias="stateSelector", min_length=1)
    verification_method: ToggleVerificationMethod = Field(alias="verificationMethod")

    @field_validator("control_selector", "state_selector")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Value is required")
        return stripped
