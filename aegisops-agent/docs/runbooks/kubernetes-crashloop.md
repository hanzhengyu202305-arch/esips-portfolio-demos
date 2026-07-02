# Kubernetes CrashLoopBackOff

Symptoms:

- Pod status shows `CrashLoopBackOff`.
- Application logs show startup validation failures.

Fix pattern:

- Inspect deployment environment values.
- Patch the overlay so application settings use supported values.
- Rerun Kubernetes dry-run validation before rollout.
