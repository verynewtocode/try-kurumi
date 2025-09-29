"""Anki add-on entry point for the Kurumi "My Honey" theme."""

from __future__ import annotations

import importlib.util
import os
from types import ModuleType


def _load_main_module() -> ModuleType | None:
    """Dynamically load the themed module whose filename contains spaces."""

    module_path = os.path.join(os.path.dirname(__file__), "kurumi says my honey.py")
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Expected Kurumi module at {module_path!r}.")

    spec = importlib.util.spec_from_file_location("kurumi_says_my_honey", module_path)
    if spec is None or spec.loader is None:
        raise ImportError("Unable to locate the Kurumi theme module.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_load_main_module()

