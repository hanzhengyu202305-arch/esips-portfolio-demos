# Issue: Kubernetes deployment fails container security policy

## Symptoms

- Policy validation fails for the API deployment.
- The container can run as root.
- `allowPrivilegeEscalation` is not explicitly disabled.

## Expected

The deployment should use a non-root container security context and disable privilege escalation.

## Observed

The deployment security context allows root execution, which violates the local policy fixture.

## Candidate Evidence

- `reports/S7/evidence.json`
- `k8s/overlays/insecure/deployment.yaml`
- `reports/S7/raw_failure.log`
- `reports/S7/multi/validation.log`

## Reviewer Boundary

This is a deterministic local security-policy fixture. It does not run a production admission controller and does not mutate a live cluster.
