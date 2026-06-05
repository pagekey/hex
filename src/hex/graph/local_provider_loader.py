# Copyright 2026 PageKey Solutions, LLC


import importlib.util
from pathlib import Path

from hex.graph.models import Params, ProviderFunc


class LocalProviderLoader:
    def __init__(self, workspace: Path) -> None:
        self._workspace = workspace

    @staticmethod
    def _load_function_from_path(path, func_name):
        spec = importlib.util.spec_from_file_location("dynamic_module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, func_name)

    def __call__(self, provider_id: str) -> ProviderFunc:
        module_name, provider_info = provider_id.split(".")
        provider_name, provider_func = provider_info.split(":")
        provider_path = (
            self._workspace
            / "modules"
            / module_name
            / "providers"
            / f"{provider_name}.py"
        )
        provider = self._load_function_from_path(provider_path, provider_func)
        return lambda inputs: provider(
            Params(inputs=inputs, workspace=self._workspace),
        )
