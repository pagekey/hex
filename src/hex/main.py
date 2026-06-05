# Copyright 2026 PageKey Solutions, LLC

import argparse
from dataclasses import asdict
from datetime import datetime
import json
from pathlib import Path
import sys
import os
import traceback

import yaml

from hex import __version__
from hex.graph import LocalGraphLoader, LocalProviderLoader, run_dag


def _run(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("run", help="Run a graph")
    parser.add_argument("id", help="Identifier of the graph. Format: {module}.{graph}")
    parser.add_argument(
        "-w",
        "--workspace",
        default=".",
        help="Path to the current workspace",
    )
    parser.add_argument(
        "-i",
        "--input",
        action="append",
        dest="inputs",
        help="Input values in key=value format (can be used multiple times)",
    )

    def _handler(args: argparse.Namespace) -> int:
        print(f"Running graph: {args.id}")
        workspace = Path(args.workspace)
        graph_inputs = {}
        if args.inputs:
            for item in args.inputs:
                if "=" in item:
                    key, value = item.split("=", 1)
                    graph_inputs[key] = value
        result = run_dag(
            args.id,
            graph_inputs,
            LocalGraphLoader(workspace),
            LocalProviderLoader(workspace),
        )
        print("-----")
        print("✅ Success! Outputs:")
        for key, value in result.outputs.items():
            print(f"    {key}: {value}")
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        results_dir = workspace / "results" / f"{timestamp}-{args.id}"
        results_dir.mkdir(parents=True, exist_ok=True)
        with (results_dir / "result.yaml").open("w") as file_handle:
            yaml.safe_dump(asdict(result), file_handle)
        print(json.dumps({"results_dir": str(results_dir)}))
        return 0

    parser.set_defaults(func=_handler)


def _ui(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("ui", help="Run the Hex debug UI.")

    def _handler(args: argparse.Namespace) -> int:
        try:
            from hex.ui import run_ui

            run_ui()
        except ImportError:
            print("Error: UI dependencies not found.")
            print("Please install them with: pip install 'hex[ui]'")
        return 0

    parser.set_defaults(func=_handler)


def _version(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("version", help="Version of Hex")

    def _handler(args: argparse.Namespace) -> int:
        print(__version__)
        return 0

    parser.set_defaults(func=_handler)


def main(argv=sys.argv[1:]) -> int:
    parser = argparse.ArgumentParser(
        description="PageKey Hex: Transparent Computation Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    _run(subparsers)
    _ui(subparsers)
    _version(subparsers)

    args = parser.parse_args(argv)

    if hasattr(args, "func"):
        try:
            return args.func(args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if os.getenv("HEX_DEBUG", "").lower() in ["1", "true"]:
                traceback.print_exc()
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
