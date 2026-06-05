# Copyright 2026 PageKey Solutions, LLC

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class Node:
    name: str
    inputs: dict[str, str]
    outputs: list[str]
    provider: str


@dataclass
class Graph:
    inputs: list[str]
    outputs: dict[str, str]
    nodes: list[Node]


@dataclass
class Execution:
    node: str
    inputs: dict[str, str]
    outputs: dict[str, str]


@dataclass
class GraphResults:
    outputs: dict[str, str]
    executions: list[Execution]


@dataclass(frozen=True)
class Params:
    inputs: dict[str, str]
    workspace: Path


class ProviderFunc(Protocol):
    def __call__(
        self,
        params: Params,
    ) -> dict[str, str]: ...


class ProviderLoader(Protocol):
    def __call__(self, provider_id: str) -> ProviderFunc: ...


class GraphLoader(Protocol):
    def __call__(self, graph_id: str) -> Graph: ...
