# Issue: Kubernetes deployment CrashLoopBackOff after config change

## Symptoms

- Pod enters CrashLoopBackOff.
- CI deploy validation fails for the Kubernetes overlay.
- Logs show invalid APP_MODE for the demo service.

## Expected

The service starts with a supported `APP_MODE` value and the deployment passes validation.

## Observed

The container exits during startup because the environment configuration is not accepted by the application.

## Candidate Evidence

- `reports/S4/evidence.json`
- `k8s/overlays/broken-env/deployment.yaml`
- `reports/S4/raw_failure.log`
- `reports/S4/multi/validation.log`

## Reviewer Boundary

This issue is a deterministic local fixture. It is not connected to a real GitHub issue, real repository mutation, or a live Kubernetes cluster.
