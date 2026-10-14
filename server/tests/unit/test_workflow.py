from unittest.mock import patch

from hex.models import Operation, Workflow
from hex.workflow import execute_workflow


def test_execute_workflow():
    # Arrange.
    workflow = Workflow(
        id="workflow1",
        username="me",
        operations=[
            Operation(
                name="do-thing",
                command="echo hi",
            )
        ],
    )

    # Act.
    with patch("hex.workflow.os.system") as system:
        result = execute_workflow(workflow)

    assert result.workflow_id == workflow.id
    system.assert_called_once_with(workflow.operations[0].command)
