import os

from hex.models import Workflow, WorkflowExecution


def execute_workflow(workflow: Workflow):
    for operation in workflow.operations:
        # whoa! how insecure!
        # TODO make this a LOT better!!!!!!!!!!!!!!!!!
        os.system(operation.command)
    return WorkflowExecution(workflow_id=workflow.id)
