# Copyright 2026 PageKey Solutions, LLC


from hex.errors import (
    CycleDetectedError,
    MissingGraphInputError,
    MissingGraphOutputError,
    UndeclaredOutputError,
    MissingOutputError,
)
from hex.graph.models import Execution, Graph, GraphLoader, GraphResults, ProviderLoader


def _check_if_node(value: str, graph: Graph):
    fields = value.split(".")
    if len(fields) != 2:
        return False
    else:
        node_name = fields[0]
        return (
            any([x for x in graph.nodes if x.name == node_name]) or node_name == "root"
        )


def run_dag(
    graph_id: str,
    graph_inputs: dict[str, str],
    graph_loader: GraphLoader,
    provider_loader: ProviderLoader,
) -> GraphResults:
    graph = graph_loader(graph_id)

    # Validate that all required inputs were provided.
    for required_input in graph.inputs:
        if required_input not in graph_inputs:
            raise MissingGraphInputError(graph_id, required_input)

    outputs: dict[str, str] = {
        f"root.{key}": value for key, value in graph_inputs.items()
    }
    executions: dict[str, Execution] = {}
    while len(executions) < len(graph.nodes):
        did_something = False
        for node in graph.nodes:
            if node.name in executions:
                continue
            has_needs = True
            for key, value in node.inputs.items():
                is_node = _check_if_node(value, graph)
                if is_node and value not in outputs:
                    print("Skip!", node.name, key)
                    has_needs = False
            if not has_needs:
                continue
            print(f"Executing: {node}")
            provider = provider_loader(node.provider)
            provider_inputs = {}
            for input_key, input_reference in node.inputs.items():
                # TODO: fail here if input_reference not in outputs
                is_node = _check_if_node(input_reference, graph)
                if is_node:
                    provider_inputs[input_key] = outputs[input_reference]
                else:
                    provider_inputs[input_key] = input_reference
            provider_outputs = provider(provider_inputs)
            # Make sure outputs are valid.
            for declared_output in node.outputs:
                if declared_output not in provider_outputs:
                    raise MissingOutputError(node.name, declared_output)
            # Check for unexpected outputs.
            for provider_output in provider_outputs.keys():
                if provider_output not in node.outputs:
                    raise UndeclaredOutputError(node.name, provider_output)
            for key, value in provider_outputs.items():
                outputs[f"{node.name}.{key}"] = value
            executions[node.name] = Execution(
                node=node.name,
                inputs=provider_inputs,
                outputs=provider_outputs,
            )
            did_something = True
        if not did_something:
            raise CycleDetectedError()
        print("Next pass.")

    graph_outputs: dict[str, str] = {}
    for key, value in graph.outputs.items():
        if value not in outputs:
            raise MissingGraphOutputError(graph_id, key, value)
        graph_outputs[key] = outputs[value]
    return GraphResults(outputs=graph_outputs, executions=executions)
