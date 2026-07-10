# Kube Copilot Adversarial Validation

These cases attack validator assumptions that plain text search commonly misses.

| case | expected | observed | key findings |
| --- | --- | --- | --- |
| safe baseline | PASS | PASS | none |
| comment spoof | FAIL | FAIL | image tag must not be latest; cpu request is required; memory request is required; cpu limit is required; memory limit is required |
| unsafe sidecar | FAIL | FAIL | image tag must not be latest; cpu request is required; memory request is required; cpu limit is required; memory limit is required |
| unsafe second document | FAIL | FAIL | host namespaces are not allowed; hostPath volumes are not allowed; image tag must not be latest; cpu request is required; memory request is required |

## Why This Matters

The validator parses every YAML document and every application or init container. Comments do not count as controls, and an unsafe sidecar or second Deployment cannot hide behind a safe first container.

## Boundary

This is a focused local policy demo, not schema validation, admission control, or a replacement for mature Kubernetes security tools.
