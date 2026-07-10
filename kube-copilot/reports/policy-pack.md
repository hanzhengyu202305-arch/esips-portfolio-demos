# Kube Copilot Policy Pack

- pack_id: `kube-copilot-predeploy`
- version: `0.2.0`
- scope: `pre-deployment generated Kubernetes and CI artifacts`

## Rules

| id | severity | category | rule | validator finding | evidence |
| --- | --- | --- | --- | --- | --- |
| KC001_IMAGE_TAG_PINNED | blocking | reproducibility | Image tag is pinned | image tag must not be latest | fixtures/safe passes; fixtures/risky fails |
| KC002_CPU_REQUEST | warning | scheduler reliability | CPU request is set | cpu request is required | fixtures/safe passes; fixtures/risky fails |
| KC003_MEMORY_REQUEST | warning | scheduler reliability | Memory request is set | memory request is required | fixtures/safe passes; fixtures/risky fails |
| KC004_CPU_LIMIT | warning | blast-radius control | CPU limit is set | cpu limit is required | fixtures/safe passes; fixtures/risky fails |
| KC005_MEMORY_LIMIT | warning | OOM risk control | Memory limit is set | memory limit is required | fixtures/safe passes; fixtures/risky fails |
| KC006_PROBES_PRESENT | warning | rollout safety | Readiness and liveness probes are present | readiness probe is required; liveness probe is required | fixtures/safe passes; fixtures/partial fails liveness |
| KC007_RUN_AS_NON_ROOT | blocking | container security | Pod runs as non-root | runAsNonRoot must be true | fixtures/safe passes; fixtures/risky fails |
| KC008_NO_PRIVILEGED_CONTAINER | blocking | privilege boundary | Privileged containers are rejected | privileged containers are not allowed | fixtures/safe passes; fixtures/risky fails |
| KC009_NO_PRIVILEGE_ESCALATION | blocking | least privilege | Privilege escalation is disabled | privilege escalation must be disabled | fixtures/safe passes; fixtures/risky fails |
| KC010_RESOURCE_REQUESTS | warning | scheduler reliability | Resource requests block exists | resource requests are required | fixtures/safe passes; fixtures/risky fails |
| KC011_CI_WORKFLOW_PRESENT | blocking | CI validation gate | CI workflow validates generated artifacts | ci workflow is required | fixtures/safe passes; fixtures/partial fails |
| KC012_STRUCTURAL_YAML_PARSE | blocking | validator integrity | Manifest is parsed structurally | deployment YAML must be structurally valid | adversarial comment and multi-document cases |
| KC013_EVERY_CONTAINER_CHECKED | blocking | policy coverage | Every application and init container is checked | container-level findings are aggregated across the pod | adversarial unsafe-sidecar case |
| KC014_HOST_BOUNDARY | blocking | host isolation | Host namespaces and hostPath are rejected | host namespaces are not allowed; hostPath volumes are not allowed | adversarial host-boundary cases |

## Trust Boundary

Generated Kubernetes and CI files remain draft artifacts. The policy pack helps reviewers decide what to reject, what to fix, and what still requires human review.

This policy pack is not a replacement for kube-linter, kubeconform, Gatekeeper, Kyverno, or admission control.
