# tiny-loki-forwarder

`tiny-loki-forwarder` is a small file tailer for Grafana Loki. It reads only
the files you explicitly configure, tracks offsets locally, and pushes new log
lines to Loki's `/loki/api/v1/push` endpoint.

It is intended for small hosts where a full log agent is more than you need.

## Goals

- Forward an explicit allowlist of files or globs.
- Store offsets in a local state file.
- Handle append-only logs and basic log rotation.
- Start at the end of files by default to avoid backfilling old logs.
- Use only the Python standard library.
- Keep labels and file paths entirely config-driven.

## Non-goals

- General-purpose `/var/log` scraping.
- Secret detection or redaction.
- Structured log parsing.
- Service discovery.
- Loki administration.

## Example Config

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

Each source must define:

- `labels`: Loki labels applied to lines from that source.
- `include`: one or more explicit file paths or globs.

## Run

```bash
tiny-loki-forwarder /etc/tiny-loki-forwarder/config.json
```

The process runs continuously until stopped.

## systemd

An example unit is included in `examples/tiny-loki-forwarder.service`.

## Dependency Updates

Dependency updates are managed by Dependabot through `.github/dependabot.yml`.
Dependabot opens weekly grouped PRs for Python packaging and GitHub Actions
updates. These PRs are never auto-merged; review and run the normal
verification path before merge.

## License

MIT
