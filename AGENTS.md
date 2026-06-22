# Agent Guidance

This is an open-source utility repo. Keep it generic.

## Boundaries

- Do not add private hostnames, domains, IP addresses, usernames, repo names, or
  deployment paths.
- Do not add vendor-specific deployment details beyond generic examples.
- Do not add secrets, tokens, credentials, or private config.
- Keep runtime behavior config-driven.
- Keep dependencies minimal; the current implementation uses only the Python
  standard library.

## Checks

Run:

```bash
python tests/run.py
python -m compileall src tests
```

Before publishing changes, scan for accidental private references.
