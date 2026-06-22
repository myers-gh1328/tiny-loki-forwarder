from __future__ import annotations

from pathlib import Path
import argparse
import sys
import time
import urllib.error

from tiny_loki_forwarder.config import load_config
from tiny_loki_forwarder.loki import push_events
from tiny_loki_forwarder.state import load_state, save_state
from tiny_loki_forwarder.tailer import collect_events


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tiny-loki-forwarder",
        description="Tail explicit files and forward new lines to Grafana Loki.",
    )
    parser.add_argument("config", type=Path)
    parser.add_argument("--once", action="store_true", help="run one collection pass")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    state = load_state(config.state_path)

    while True:
        try:
            events = collect_events(
                config.sources,
                state,
                start_at_end=config.start_at_end,
                limit=config.batch_size,
            )
            push_events(config.loki_push_url, events)
            save_state(config.state_path, state)
        except (OSError, RuntimeError, urllib.error.URLError) as exc:
            print(f"tiny-loki-forwarder error: {exc}", file=sys.stderr)

        if args.once:
            return 0
        time.sleep(config.interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
