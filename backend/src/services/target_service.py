from __future__ import annotations

from uuid import UUID

from sqlmodel import Session, select

from src.api.errors import ConflictError, NotFoundError
from src.models.automation_target import (
    AutomationTargetCreate,
    AutomationTargetRead,
    AutomationTargetRecord,
    AutomationTargetUpdate,
    payload_to_record_data,
    serialize_target,
)
from src.models.base import utc_now


class TargetService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_targets(self) -> list[AutomationTargetRead]:
        statement = select(AutomationTargetRecord).order_by(AutomationTargetRecord.updated_at.desc())
        records = self.session.exec(statement).all()
        return [serialize_target(record) for record in records]

    def get_target(self, target_id: UUID) -> AutomationTargetRead:
        record = self._get_record(target_id)
        return serialize_target(record)

    def create_target(self, payload: AutomationTargetCreate) -> AutomationTargetRead:
        self._ensure_name_is_available(payload.name)
        record = AutomationTargetRecord(**payload_to_record_data(payload))
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return serialize_target(record)

    def update_target(self, target_id: UUID, payload: AutomationTargetUpdate) -> AutomationTargetRead:
        record = self._get_record(target_id)
        self._ensure_name_is_available(payload.name, excluded_target_id=target_id)

        for field_name, value in payload_to_record_data(payload).items():
            setattr(record, field_name, value)
        record.updated_at = utc_now()

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return serialize_target(record)

    def delete_target(self, target_id: UUID) -> None:
        record = self._get_record(target_id)
        self.session.delete(record)
        self.session.commit()

    def _get_record(self, target_id: UUID) -> AutomationTargetRecord:
        record = self.session.get(AutomationTargetRecord, target_id)
        if record is None:
            raise NotFoundError("Automation target was not found")
        return record

    def _ensure_name_is_available(self, name: str, excluded_target_id: UUID | None = None) -> None:
        statement = select(AutomationTargetRecord).where(AutomationTargetRecord.name == name)
        existing = self.session.exec(statement).first()
        if existing is None:
            return
        if excluded_target_id is not None and existing.id == excluded_target_id:
            return
        raise ConflictError("Automation target name must be unique")
