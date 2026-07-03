# Kube Copilot policy matrix

This matrix documents the deterministic checks used by Kube Copilot. The demo is pre-deployment validation, not a replacement for kube-linter, kubeconform, Gatekeeper, Kyverno, or production admission control.

| rule | why it matters | fixture evidence |
| --- | --- | --- |
| image tag must not be `latest` | reproducibility | safe passes; risky fails |
| CPU request required | scheduler reliability | safe passes; risky fails |
| memory request required | scheduler reliability | safe passes; risky fails |
| CPU limit required | blast-radius control | safe passes; risky fails |
| memory limit required | OOM risk control | safe passes; risky fails |
| readiness probe required | rollout safety | safe passes |
| liveness probe required | recovery safety | partial fails |
| `runAsNonRoot: true` | container security | safe passes; risky fails |
| privileged container rejected | privilege boundary | risky fails |
| privilege escalation disabled | least privilege | risky fails |
| GitHub Actions workflow present | CI validation gate | partial fails |

## Fixtures

- `fixtures/safe/` shows a pinned image, resources, probes, security context, and CI.
- `fixtures/partial/` shows incremental remediation with a missing liveness probe and missing CI workflow.
- `fixtures/risky/` shows a latest tag, missing resources, and insecure container settings.

## Trust Boundary

AI-generated Kubernetes YAML is a draft. The validator and human review decide whether the draft is suitable for further engineering work.
