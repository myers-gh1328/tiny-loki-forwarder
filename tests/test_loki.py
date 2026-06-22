import json

from tiny_loki_forwarder.loki import build_loki_payload
from tiny_loki_forwarder.tailer import Event


def test_build_loki_payload_groups_by_labels():
    payload = build_loki_payload(
        [
            Event(
                labels={"host": "host-a", "service": "svc"},
                line='{"message":"one"}',
                timestamp_ns="100",
            ),
            Event(
                labels={"host": "host-a", "service": "svc"},
                line='{"message":"two"}',
                timestamp_ns="200",
            ),
        ]
    )

    decoded = json.loads(payload)
    assert len(decoded["streams"]) == 1
    assert decoded["streams"][0]["stream"] == {"host": "host-a", "service": "svc"}
    assert decoded["streams"][0]["values"] == [
        ["100", '{"message":"one"}'],
        ["200", '{"message":"two"}'],
    ]
