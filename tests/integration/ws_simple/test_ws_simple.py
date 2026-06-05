from pathlib import Path
import os
import subprocess

import pytest


@pytest.mark.parametrize(
    "graph_id,graph_inputs", [["core.main", {"name": "Bob"}], ["core.call", {}]]
)
def test_integration_ws_simple(graph_id, graph_inputs):
    workspace_path = Path(__file__).parent

    cmd = [
        "hex",
        "run",
        graph_id,
        "-w",
        str(workspace_path),
        "-i",
        "name=Bob",
    ]
    for key, value in graph_inputs.items():
        cmd.append("-i")
        cmd.append(f"{key}={value}")
    try:
        env = os.environ.copy()
        env["HEX_DEBUG"] = "1"
        result = subprocess.run(
            cmd, capture_output=True, check=True, text=True, env=env
        )
        assert "Success!" in result.stdout
    except subprocess.CalledProcessError as e:
        # These prints will show up in the Pytest failure report
        print("\n--- SUBPROCESS FAILURE ---")
        print(f"Command: {' '.join(cmd)}")
        print(f"Exit Code: {e.returncode}")
        print(f"STDOUT:\n{e.stdout}")
        print(f"STDERR:\n{e.stderr}")
        print("--------------------------")

        # Re-raise the exception so the test actually fails
        raise e
