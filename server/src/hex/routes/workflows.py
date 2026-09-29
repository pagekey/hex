from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from hex.globals import (
    session_manager,
    storage_manager,
)


router = APIRouter(prefix="/workflows", tags=["sessions"])


@router.get("")
async def home():
    return "Hello from workflows"


class Operation(BaseModel):
    name: str
    command: str


class Workflow(BaseModel):
    id: str
    username: str
    operations: list[Operation]


class CreateWorkflowRequest(BaseModel):
    id: str
    operations: list[Operation]


@router.post("")
async def create_workflow(
    request: CreateWorkflowRequest, session_id: str | None = Cookie(default=None)
):
    # TODO eventually turn this into a shared helper
    if session_id is None:
        return JSONResponse(status_code=401, content={"message": "Not logged in"})

    username = session_manager.get_session_username(session_id)

    if username is None:
        return JSONResponse(status_code=401, content={"message": "Not logged in"})

    storage_manager.save(
        "workflows",
        Workflow(
            id=request.id,
            operations=request.operations,
            username=username,
        ).model_dump(),
    )

    return JSONResponse(
        status_code=200, content={"message": f"Created workflow {request.id}"}
    )
