# Container Security Context

Symptoms:

- Policy checks flag root container execution.
- `allowPrivilegeEscalation` is missing or true.

Fix pattern:

- Set `runAsNonRoot: true`.
- Use a non-root numeric user.
- Disable privilege escalation.
