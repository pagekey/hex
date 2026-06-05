# Copyright 2026 PageKey Solutions, LLC

from pathlib import Path

import yaml

from hex.graph.models import Graph, Node


class LocalGraphLoader:
    def __init__(self, workspace: Path) -> None:
        self._workspace = workspace

    @staticmethod
    def _load_graph_from_yaml(path: Path):
        with path.open("r") as graph_file:
            graph_dict = yaml.safe_load(graph_file)
        return Graph(
            inputs=graph_dict[
                "inputs"
            ],  # TODO: this should be a dict built from the yaml
            outputs=graph_dict["outputs"],
            nodes=[
                Node(
                    name=node_name,
                    inputs=node_dict["inputs"],
                    outputs=node_dict["outputs"],
                    provider=node_dict["provider"],
                )
                for node_name, node_dict in graph_dict["nodes"].items()
            ],
        )

    def __call__(self, graph_id: str) -> Graph:
        module_name, graph_name = graph_id.split(".")
        graph_path = (
            self._workspace / "modules" / module_name / "graphs" / f"{graph_name}.yaml"
        )
        return self._load_graph_from_yaml(graph_path)
