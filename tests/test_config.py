from tiny_loki_forwarder.config import parse_config


def test_parse_config_requires_sources():
    try:
        parse_config(
            {
                "loki_push_url": "http://localhost:3100/loki/api/v1/push",
                "state_path": "/tmp/state.json",
                "sources": [],
            }
        )
    except ValueError as exc:
        assert "at least one source" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_parse_config_accepts_minimal_source():
    config = parse_config(
        {
            "loki_push_url": "http://localhost:3100/loki/api/v1/push",
            "state_path": "/tmp/state.json",
            "sources": [
                {
                    "labels": {"host": "host-a", "service": "svc"},
                    "include": ["/tmp/example.log"],
                }
            ],
        }
    )

    assert config.batch_size == 100
    assert config.start_at_end is True
    assert config.sources[0].labels["service"] == "svc"
