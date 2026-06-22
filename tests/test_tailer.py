from pathlib import Path
import tempfile

from tiny_loki_forwarder.config import Source
from tiny_loki_forwarder.tailer import read_new_lines


def test_read_new_lines_starts_at_end_by_default():
    with tempfile.TemporaryDirectory() as temp_dir:
        log_path = Path(temp_dir) / "app.log"
        log_path.write_text("old\n", encoding="utf-8")
        state = {}
        source = Source(
            labels={"host": "host-a", "service": "svc"}, include=[str(log_path)]
        )

        assert read_new_lines(source, log_path, state, start_at_end=True, limit=10) == []

        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("new\n")

        events = read_new_lines(source, log_path, state, start_at_end=True, limit=10)
        assert len(events) == 1
        assert '"message":"new"' in events[0].line


def test_read_new_lines_can_backfill_when_requested():
    with tempfile.TemporaryDirectory() as temp_dir:
        log_path = Path(temp_dir) / "app.log"
        log_path.write_text("old\n", encoding="utf-8")
        state = {}
        source = Source(
            labels={"host": "host-a", "service": "svc"}, include=[str(log_path)]
        )

        events = read_new_lines(source, log_path, state, start_at_end=False, limit=10)

        assert len(events) == 1
        assert '"message":"old"' in events[0].line
