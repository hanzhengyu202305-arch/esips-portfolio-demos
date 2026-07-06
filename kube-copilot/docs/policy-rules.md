# Kube Copilot Policy Rules

Kube Copilot treats generated infrastructure as a draft. The validator is the trust boundary before any human considers deployment.

## External Anchors

The rules are aligned with Kubernetes documentation and mature validation ecosystems:

- Kubernetes documents CPU and memory requests/limits as resource-management controls.
- Kubernetes documents readiness, liveness, and startup probes as application-health signals.
- Tools such as kube-linter, kubeconform, Kyverno, and Gatekeeper show why generated manifests should pass policy-style checks before trust.

This project keeps those ideas small and deterministic for a portfolio demo. It does not replace production scanners, schema validators, or admission controllers.

| rule | why it matters | safe example | risky example |
| --- | --- | --- | --- |
| No `latest` image tag | Reproducible deployments need immutable image versions. | `ghcr.io/example/api:1.2.0` | `example/api:latest` |
| CPU requests required | Scheduling needs a realistic baseline. | `requests.cpu: "250m"` | missing or empty CPU request |
| Memory requests required | Scheduling and capacity planning need a baseline. | `requests.memory: "256Mi"` | missing or empty memory request |
| CPU limits required | Containers should have bounded CPU use. | `limits.cpu: "500m"` | missing or empty CPU limit |
| Memory limits required | Containers should have bounded memory use. | `limits.memory: "512Mi"` | missing or empty memory limit |
| Readiness probe required | Rollouts should wait until the app is ready for traffic. | `readinessProbe.httpGet.path: /health` | no readiness probe |
| Liveness probe required | Stuck containers need an automated recovery signal. | `livenessProbe.httpGet.path: /health` | no liveness probe |
| `runAsNonRoot: true` | Pods should not default to root execution. | pod security context sets non-root | pod runs as root or unspecified |
| Privileged containers rejected | Privileged mode expands host-level risk. | `privileged: false` | `privileged: true` |
| Privilege escalation disabled | Containers should not gain extra privileges after start. | `allowPrivilegeEscalation: false` | missing or `true` |
| CI workflow present | Generated manifests need repeatable validation before review. | `.github/workflows/ci.yml` exists | no CI workflow |

## Report Cases

`make report` writes `reports/risk-comparison.md` with three deterministic cases:

- `safe`: generated with pinned image, resources, probes, secure context, and CI.
- `partial`: mostly remediated but still missing rollout/CI evidence.
- `risky`: latest tag, missing resources, insecure security context.

This is intentionally smaller than production tools such as kube-linter, kubeconform, kube-score, Polaris, Kyverno, Gatekeeper, or Datree. The portfolio claim is the workflow shape: generation plus visible policy checks and human review.
