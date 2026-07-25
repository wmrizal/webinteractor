from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.lib.db import get_session
from src.models.automation_run import AutomationRunRead, CreateRunRequest, RunDetails
from src.services.run_service import RunService

router = APIRouter(tags=["runs"])
SessionDependency = Annotated[Session, Depends(get_session)]


@router.post("/runs", response_model=AutomationRunRead, status_code=status.HTTP_202_ACCEPTED)
def create_run(payload: CreateRunRequest, session: SessionDependency) -> AutomationRunRead:
    return RunService(session).create_run(payload)


@router.get("/runs/{run_id}", response_model=RunDetails)
def get_run(run_id: UUID, session: SessionDependency) -> RunDetails:
    return RunService(session).get_run_details(run_id)


@router.get("/targets/{target_id}/runs", response_model=list[AutomationRunRead])
def list_target_runs(target_id: UUID, session: SessionDependency) -> list[AutomationRunRead]:
    return RunService(session).list_runs_for_target(target_id)
