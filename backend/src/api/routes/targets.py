from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from src.lib.db import get_session
from src.models.automation_target import AutomationTargetCreate, AutomationTargetRead, AutomationTargetUpdate
from src.services.target_service import TargetService

router = APIRouter(prefix="/targets", tags=["targets"])
SessionDependency = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[AutomationTargetRead])
def list_targets(session: SessionDependency) -> list[AutomationTargetRead]:
    return TargetService(session).list_targets()


@router.post("", response_model=AutomationTargetRead, status_code=status.HTTP_201_CREATED)
def create_target(payload: AutomationTargetCreate, session: SessionDependency) -> AutomationTargetRead:
    return TargetService(session).create_target(payload)


@router.get("/{target_id}", response_model=AutomationTargetRead)
def get_target(target_id: UUID, session: SessionDependency) -> AutomationTargetRead:
    return TargetService(session).get_target(target_id)


@router.patch("/{target_id}", response_model=AutomationTargetRead)
def update_target(
    target_id: UUID,
    payload: AutomationTargetUpdate,
    session: SessionDependency,
) -> AutomationTargetRead:
    return TargetService(session).update_target(target_id, payload)


@router.delete("/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_target(target_id: UUID, session: SessionDependency) -> Response:
    TargetService(session).delete_target(target_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
