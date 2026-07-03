# Kube Copilot risk comparison

Target ESIPS brief: `Accenture_01 Kubernetes_DevOps.pdf`.

This report frames Kube Copilot as a small Kubernetes-based CI/CD pipeline assistant: generation is useful, but validation and human review remain the trust boundary.

| case | status | findings |
| --- | --- | --- |
| safe | PASS | none |
| risky | FAIL | image tag must not be latest; cpu limit is required; memory limit is required; cpu request is required; memory request is required; runAsNonRoot must be true; privileged containers are not allowed; privilege escalation must be disabled |

## Remediation checklist

- Pin image tags to immutable versions before deployment review.
- Set CPU and memory requests and limits for every container.
- Validate probes before rollout so health checks match the application contract.
- Require non-root security contexts and reject privileged containers.
- Keep generated manifests behind CI and human review gates.

## Interview framing

The generator can draft Kubernetes and CI/CD files, but the validator is the trust boundary.
The generated YAML is not production-ready until it passes policy checks.
Human review remains required for secrets, RBAC, production rollout, and business risk.

## Public references

This demo is intentionally much smaller than kube-linter, kubeconform, kube-score, Polaris, Kyverno, Gatekeeper, or Datree. The shared idea is that generated Kubernetes manifests need policy-style checks before they are trusted.
