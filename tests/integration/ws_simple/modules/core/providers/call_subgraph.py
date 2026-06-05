import json
from pathlib import Path
from hex import run_dag, Params
from hex.graph.local_graph_loader import LocalGraphLoader
from hex.graph.local_provider_loader import LocalProviderLoader


def run(params: Params) -> dict[str, str]:
    results = run_dag(
        params.inputs["graph_id"],
        json.loads(params.inputs["graph_inputs"]),
        LocalGraphLoader(Path(params.inputs["workspace"])),
        LocalProviderLoader(Path(params.inputs["workspace"])),
    )
    return results.outputs
