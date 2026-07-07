# Patch Risk Diff

- scenario: `S7`
- root_cause_id: `container_runs_as_root`
- overall_status: `REVIEW`
- recommended_owner: `platform/security reviewer`

## Files Changed

- `k8s/overlays/insecure/deployment.yaml`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | k8s/overlays/insecure/deployment.yaml matches the scenario allowlist |
| PASS | container security | runAsNonRoot is enabled in the proposed patch |
| PASS | container security | allowPrivilegeEscalation=false is present in the proposed patch |
| REVIEW | validation | security dry-run validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
