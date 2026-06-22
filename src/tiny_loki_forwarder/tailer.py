from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import glob
import json
import os
import time

from tiny_loki_forwarder.config import Source
from tiny_loki_forwarder.state import State


@dataclass(frozen=True)
class Event:
    labels: dict[str, str]
    line: str
    timestamp_ns: str


def collect_events(
    sources: list[Source],
    state: State,
    *,
    start_at_end: bool,
    limit: int,
) -> list[Event]:
    events: list[Event] = []
    for source in sources:
        for path in _expand_paths(source.include):
            events.extend(
                read_new_lines(
                    source,
                    path,
                    state,
                    start_at_end=start_at_end,
                    limit=limit - len(events),
                )
            )
            if len(events) >= limit:
                return events
    return events


def read_new_lines(
    source: Source,
    path: Path,
    state: State,
    *,
    start_at_end: bool,
    limit: int,
) -> list[Event]:
    if limit <= 0:
        return []

    try:
        stat_result = path.stat()
    except FileNotFoundError:
        return []

    key = _file_key(path, stat_result)
    offset = state.get(key)
    if offset is None:
        offset = stat_result.st_size if start_at_end else 0
    elif offset > stat_result.st_size:
        offset = 0

    events: list[Event] = []
    with path.open("rb") as handle:
        handle.seek(offset)
        for raw_line in handle:
            message = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
            if not message:
                continue
            events.append(_event_from_line(source, message))
            if len(events) >= limit:
                break
        state[key] = handle.tell()
    return events


def _event_from_line(source: Source, message: str) -> Event:
    payload = {
        **source.labels,
        "message": message,
    }
    return Event(
        labels=source.labels,
        line=json.dumps(payload, separators=(",", ":")),
        timestamp_ns=str(time.time_ns()),
    )


def _expand_paths(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(Path(path) for path in sorted(glob.glob(pattern)))
    return paths


def _file_key(path: Path, stat_result: os.stat_result) -> str:
    return f"{path}:{stat_result.st_dev}:{stat_result.st_ino}"
