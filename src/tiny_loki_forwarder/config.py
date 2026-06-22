from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Source:
    labels: dict[str, str]
    include: list[str]


@dataclass(frozen=True)
class Config:
    loki_push_url: str
    state_path: Path
    interval_seconds: int
    batch_size: int
    start_at_end: bool
    sources: list[Source]


def load_config(path: Path) -> Config:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return parse_config(raw)


def parse_config(raw: dict[str, Any]) -> Config:
    sources = raw.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("config must include at least one source")

    parsed_sources = [_parse_source(source) for source in sources]

    return Config(
        loki_push_url=_required_str(raw, "loki_push_url"),
        state_path=Path(_required_str(raw, "state_path")),
        interval_seconds=int(raw.get("interval_seconds", 5)),
        batch_size=int(raw.get("batch_size", 100)),
        start_at_end=bool(raw.get("start_at_end", True)),
        sources=parsed_sources,
    )


def _parse_source(raw: Any) -> Source:
    if not isinstance(raw, dict):
        raise ValueError("source must be an object")

    labels = raw.get("labels")
    if not isinstance(labels, dict) or not labels:
        raise ValueError("source must include labels")
    parsed_labels = {str(key): str(value) for key, value in labels.items()}

    include = raw.get("include")
    if not isinstance(include, list) or not include:
        raise ValueError("source must include at least one include path")

    return Source(labels=parsed_labels, include=[str(item) for item in include])


def _required_str(raw: dict[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"config must include {key}")
    return value
