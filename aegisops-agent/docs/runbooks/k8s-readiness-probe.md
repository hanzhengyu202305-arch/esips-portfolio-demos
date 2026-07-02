# Kubernetes Readiness Probe Failures

Symptoms:

- Pod runs but never becomes ready.
- Events show readiness probe 404 or timeout.

Fix pattern:

- Compare probe path with application routes.
- Point readiness to a lightweight endpoint such as `/health`.
