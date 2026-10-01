from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from hex.models import Operation, Workflow
from hex.workflow import execute_workflow
from pydantic import BaseModel

from hex.globals import (
    session_manager,
    storage_manager,
)


router = APIRouter(prefix="/workflows", tags=["sessions"])


def _get_login_error(session_id: str) -> JSONResponse | None:
    if session_id is None:
        return JSONResponse(status_code=401, content={"message": "Not logged in"})
    if session_manager.get_session_username(session_id) is None:
        return JSONResponse(status_code=401, content={"message": "Not logged in"})


class CreateWorkflowRequest(BaseModel):
    id: str
    operations: list[Operation]


@router.post("")
async def create_workflow(
    request: CreateWorkflowRequest, session_id: str | None = Cookie(default=None)
):
    login_error = _get_login_error(session_id)
    if login_error is not None:
        return login_error
    username = session_manager.get_session_username(session_id)
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


@router.get("")
async def list_workflows(session_id: str | None = Cookie(default=None)):
    login_error = _get_login_error(session_id)
    if login_error is not None:
        return login_error

    workflows = storage_manager.load_many("workflows")
    return JSONResponse(status_code=200, content=workflows)


class RunWorkflowRequest(BaseModel):
    id: str


@router.post("/run")
async def run_workflow(
    request: RunWorkflowRequest, session_id: str | None = Cookie(default=None)
):
    login_error = _get_login_error(session_id)
    if login_error is not None:
        return login_error
    workflow_dict = storage_manager.load("workflows", request.id)
    workflow = Workflow(**workflow_dict)
    # TODO make sure the user owns it, blah blah blah
    if not workflow:
        return JSONResponse(
            status_code=404, content={"message": f"Workflow {request.id} not found"}
        )
    result = execute_workflow(workflow)
    return JSONResponse(status_code=200, content={"execution": result.model_dump()})
