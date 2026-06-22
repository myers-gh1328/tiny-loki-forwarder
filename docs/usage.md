# Usage

`tiny-loki-forwarder` tails explicitly configured files and pushes new lines to
Grafana Loki.

## Install From Source

```bash
git clone https://github.com/myers-gh1328/tiny-loki-forwarder.git
cd tiny-loki-forwarder
python -m tiny_loki_forwarder.cli --help
```

For a source checkout without packaging, set `PYTHONPATH`:

```bash
PYTHONPATH=src python -m tiny_loki_forwarder.cli /etc/tiny-loki-forwarder/config.json
```

## Configuration

Use a JSON config file. Every source must define explicit paths or globs.

```json
{
  "loki_push_url": "http://127.0.0.1:3100/loki/api/v1/push",
  "state_path": "/var/lib/tiny-loki-forwarder/state.json",
  "interval_seconds": 5,
  "batch_size": 100,
  "start_at_end": true,
  "sources": [
    {
      "labels": {
        "host": "example-host",
        "service": "example-service",
        "source_type": "service_log"
      },
      "include": ["/var/log/example-service/*.log"]
    }
  ]
}
```

## Operations

The process stores file offsets in `state_path`. It starts at the end of files
by default, so first startup does not backfill historical logs unless
`start_at_end` is set to `false`.
