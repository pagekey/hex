import re
from unittest.mock import MagicMock

import pytest

from hex.errors import (
    MissingGraphInputError,
    MissingGraphOutputError,
    UndeclaredOutputError,
    MissingOutputError,
)
from hex.graph.dag import run_dag
from hex.graph.models import Execution, Graph, GraphResults, Node


def test_dag_with_one_node_returns_valid_results():
    # Arrange.
    graph_inputs = {}
    mock_provider_func = MagicMock()
    mock_provider_func.return_value = {"apple": "three"}
    mock_graph_loader = MagicMock()
    mock_graph_loader.return_value = Graph(
        inputs=[],
        outputs={
            "final": "my-node.apple",
        },
        nodes=[
            Node(
                name="my-node",
                inputs={},
                outputs=["apple"],
                provider=mock_provider_func,
            )
        ],
    )
    mock_provider_loader = MagicMock()
    mock_provider_loader.return_value = mock_provider_func

    # Act.
    results = run_dag("graph.id", graph_inputs, mock_graph_loader, mock_provider_loader)

    # Assert.
    assert results == GraphResults(
        outputs={
            "final": "three",
        },
        executions={
            "my-node": Execution(node="my-node", inputs={}, outputs={"apple": "three"}),
        },
    )


def test_one_node_with_missing_output_raises_error():
    # Arrange.
    graph_inputs = {}
    mock_provider_func = MagicMock()
    mock_provider_func.return_value = {}
    mock_graph_loader = MagicMock()
    mock_graph_loader.return_value = Graph(
        inputs=[],
        outputs={},
        nodes=[
            Node(
                name="my-node",
                inputs={},
                outputs=["the-forgotten-thing"],
                provider=mock_provider_func,
            )
        ],
    )
    mock_provider_loader = MagicMock()
    mock_provider_loader.return_value = mock_provider_func

    # Act.
    with pytest.raises(
        MissingOutputError,
        match="Expected node my-node to provide output the-forgotten-thing but it was not found.",
    ):
        run_dag("graph.id", graph_inputs, mock_graph_loader, mock_provider_loader)


def test_one_node_with_undeclared_output_raises_error():
    # Arrange.
    graph_inputs = {}
    mock_provider_func = MagicMock()
    mock_provider_func.return_value = {
        "expected-thing": "yeah",
        "unexpected-thing": "whoa!!!!!!! who's this guy?!?!",
    }
    mock_graph_loader = MagicMock()
    mock_graph_loader.return_value = Graph(
        inputs=[],
        outputs={},
        nodes=[
            Node(
                name="my-node",
                inputs={},
                outputs=["expected-thing"],
                provider=mock_provider_func,
            )
        ],
    )
    mock_provider_loader = MagicMock()
    mock_provider_loader.return_value = mock_provider_func

    # Act.
    with pytest.raises(
        UndeclaredOutputError,
        match="Node my-node has undeclared output unexpected-thing.",
    ):
        run_dag("graph.id", graph_inputs, mock_graph_loader, mock_provider_loader)


def test_two_nodes_with_inputs_and_outputs_pass_to_each_other():
    # Arrange.
    graph_inputs = {
        "sum": 0,
    }
    mock_provider_func = MagicMock()
    mock_provider_func.side_effect = [
        {"sum": 1},
        {"sum": 2},
    ]
    mock_graph_loader = MagicMock()
    mock_graph_loader.return_value = Graph(
        inputs=["sum"],
        outputs={
            "final_sum": "node2.sum",
        },
        nodes=[
            Node(
                name="node1",
                inputs={
                    "sum": "root.sum",
                },
                outputs=["sum"],
                provider=mock_provider_func,
            ),
            Node(
                name="node2",
                inputs={"sum": "node1.sum"},
                outputs=["sum"],
                provider=mock_provider_func,
            ),
        ],
    )
    mock_provider_loader = MagicMock()
    mock_provider_loader.return_value = mock_provider_func

    # Act.
    results = run_dag("graph.id", graph_inputs, mock_graph_loader, mock_provider_loader)

    # Assert.
    assert results == GraphResults(
        outputs={
            "final_sum": 2,
        },
        executions={
            "node1": Execution(
                node="node1",
                inputs={
                    "sum": 0,
                },
                outputs={"sum": 1},
            ),
            "node2": Execution(
                node="node2",
                inputs={
                    "sum": 1,
                },
                outputs={"sum": 2},
            ),
        },
    )


def test_graph_with_missing_input_raises_error():
    # Arrange.
    graph_inputs = {}
    mock_graph_loader = MagicMock()
    mock_graph_loader.return_value = Graph(
        inputs=["required-input"],
        outputs={},
        nodes=[],
    )
    mock_provider_loader = MagicMock()

    # Act.
    with pytest.raises(
        MissingGraphInputError,
        match="Graph graph.id requires input required-input which was not provided.",
    ):
        run_dag("graph.id", graph_inputs, mock_graph_loader, mock_provider_loader)


def test_graph_with_missing_output_raises_error():
    # Arrange.
    graph_inputs = {}
    mock_provider_func = MagicMock()
    mock_provider_func.return_value = {"apple": "three"}
    mock_graph_loader = MagicMock()
    mock_graph_loader.return_value = Graph(
        inputs=[],
        outputs={
            "final": "my-node.apple2",
        },
        nodes=[
            Node(
                name="my-node",
                inputs={},
                outputs=["apple"],
                provider=mock_provider_func,
            )
        ],
    )
    mock_provider_loader = MagicMock()
    mock_provider_loader.return_value = mock_provider_func

    # Act.
    with pytest.raises(
        MissingGraphOutputError,
        match=re.escape("Graph output final (my-node.apple2) not found for graph.id."),
    ):
        run_dag("graph.id", graph_inputs, mock_graph_loader, mock_provider_loader)


def test_node_with_input_not_matching_node_name_receives_literal():
    # Arrange.
    graph_inputs = {}
    mock_provider_func = MagicMock()
    mock_provider_func.return_value = {"apple": "three"}
    mock_graph_loader = MagicMock()
    mock_graph_loader.return_value = Graph(
        inputs=[],
        outputs={
            "final": "my-node.apple",
        },
        nodes=[
            Node(
                name="my-node",
                inputs={"literal-input": "not-a.node"},
                outputs=["apple"],
                provider=mock_provider_func,
            )
        ],
    )
    mock_provider_loader = MagicMock()
    mock_provider_loader.return_value = mock_provider_func

    # Act.
    results = run_dag("graph.id", graph_inputs, mock_graph_loader, mock_provider_loader)

    # Assert.
    assert results == GraphResults(
        outputs={
            "final": "three",
        },
        executions={
            "my-node": Execution(
                node="my-node",
                inputs={
                    "literal-input": "not-a.node",
                },
                outputs={"apple": "three"},
            ),
        },
    )
