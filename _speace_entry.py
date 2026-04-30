"""SPEACE setuptools entry point — bridges hyphenated filenames."""
import sys
import importlib.util
from pathlib import Path

_ROOT = Path(__file__).parent

def _run(script_rel: str) -> None:
    path = _ROOT / script_rel
    spec = importlib.util.spec_from_file_location("_entry", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_entry"] = mod
    spec.loader.exec_module(mod)
    sys.exit(getattr(mod, "main", lambda: 0)())

def cli() -> None:
    _run("scripts/speace-cli.py")
