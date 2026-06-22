from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    failures = 0

    for path in sorted((root / "tests").glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            print(f"failed to load {path}")
            failures += 1
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in sorted(dir(module)):
            if not name.startswith("test_"):
                continue
            test_func = getattr(module, name)
            if not callable(test_func):
                continue
            if test_func.__code__.co_argcount:
                print(f"skip {path.name}::{name} (requires pytest fixture)")
                continue
            try:
                test_func()
            except Exception as exc:
                print(f"FAIL {path.name}::{name}: {exc}")
                failures += 1
            else:
                print(f"ok {path.name}::{name}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
