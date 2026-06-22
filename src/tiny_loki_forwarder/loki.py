from __future__ import annotations

import json
import urllib.request

from tiny_loki_forwarder.tailer import Event


def build_loki_payload(events: list[Event]) -> bytes:
    streams: dict[tuple[tuple[str, str], ...], dict[str, object]] = {}
    for event in events:
        key = tuple(sorted(event.labels.items()))
        if key not in streams:
            streams[key] = {"stream": dict(key), "values": []}
        values = streams[key]["values"]
        assert isinstance(values, list)
        values.append([event.timestamp_ns, event.line])

    return json.dumps({"streams": list(streams.values())}).encode("utf-8")


def push_events(push_url: str, events: list[Event], *, timeout_seconds: int = 10) -> None:
    if not events:
        return

    request = urllib.request.Request(
        push_url,
        data=build_loki_payload(events),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        if response.status >= 300:
            raise RuntimeError(f"loki push failed with HTTP {response.status}")
