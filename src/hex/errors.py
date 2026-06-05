# Copyright 2026 PageKey Solutions, LLC


class CycleDetectedError(Exception):
    """Cycle has been detected in graph - stop now."""

    def __init__(self) -> None:
        super().__init__("Cycle detected, stopping graph execution.")


class UndeclaredOutputError(Exception):
    """When an output is missing from a node run."""

    def __init__(self, node_name: str, output_name: str) -> None:
        message = f"Node {node_name} has undeclared output {output_name}."
        super().__init__(message)


class MissingOutputError(Exception):
    """When an output is missing from a node run."""

    def __init__(self, node_name: str, output_name: str) -> None:
        message = f"Expected node {node_name} to provide output {output_name} but it was not found."
        super().__init__(message)


class MissingGraphInputError(Exception):
    """When an input is missing from a graph run."""

    def __init__(self, graph_id: str, input_name: str) -> None:
        message = (
            f"Graph {graph_id} requires input {input_name} which was not provided."
        )
        super().__init__(message)


class MissingGraphOutputError(Exception):
    """When an output for the graph is not found."""

    def __init__(self, graph_id: str, output_key: str, output_value: str) -> None:
        message = (
            f"Graph output {output_key} ({output_value}) not found for {graph_id}."
        )
        super().__init__(message)
