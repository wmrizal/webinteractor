from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.lib.db import get_session
from src.models.automation_run import RunHistoryItem
from src.services.run_history_service import RunHistoryDetails, RunHistoryService

router = APIRouter(tags=["run-history"])
SessionDependency = Annotated[Session, Depends(get_session)]


@router.get("/targets/{target_id}/runs/history", response_model=list[RunHistoryItem])
def list_target_run_history(target_id: UUID, session: SessionDependency) -> list[RunHistoryItem]:
    return RunHistoryService(session).list_history_for_target(target_id)


@router.get("/runs/{run_id}/history", response_model=RunHistoryDetails)
def get_run_history(run_id: UUID, session: SessionDependency) -> RunHistoryDetails:
    return RunHistoryService(session).get_run_history_details(run_id)
