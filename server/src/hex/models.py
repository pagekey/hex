from pydantic import BaseModel


class Operation(BaseModel):
    name: str
    command: str


class Workflow(BaseModel):
    id: str
    username: str
    operations: list[Operation]


class WorkflowExecution(BaseModel):
    workflow_id: str
    # TODO add per-operation execution info
