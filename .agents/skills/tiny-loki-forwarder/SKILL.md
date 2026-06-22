---
name: tiny-loki-forwarder
description: Work on tiny-loki-forwarder, a generic open-source Python file-to-Loki forwarder.
---

Use this skill when changing `tiny-loki-forwarder`.

Rules:

- Keep the project generic and open-source clean.
- Do not add private hostnames, domains, IPs, usernames, repo names, or paths.
- Do not add secrets or deployment-specific config.
- Prefer Python standard library code unless a dependency clearly pays for
  itself.
- Keep inputs explicit and allowlist-based.

Validation:

```bash
python tests/run.py
python -m compileall src tests
rg -n "aegir|nanobot|pihole|printpi|phish|dradi|192\\.168|aegirtech|aegirscuba" .
```
