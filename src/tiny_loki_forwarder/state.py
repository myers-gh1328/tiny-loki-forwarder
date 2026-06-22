from __future__ import annotations

import json
from pathlib import Path


State = dict[str, int]


def load_state(path: Path) -> State:
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except FileNotFoundError:
        return {}

    if not isinstance(raw, dict):
        raise ValueError("state file must contain an object")

    return {str(key): int(value) for key, value in raw.items()}


def save_state(path: Path, state: State) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(f"{path.suffix}.tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, sort_keys=True)
        handle.write("\n")
    temp_path.replace(path)
