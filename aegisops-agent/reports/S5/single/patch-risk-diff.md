# Patch Risk Diff

- scenario: `S5`
- root_cause_id: `wrong_readiness_probe_path`
- overall_status: `REVIEW`
- recommended_owner: `platform reviewer`

## Files Changed

- `k8s/overlays/broken-probe/deployment.yaml`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | k8s/overlays/broken-probe/deployment.yaml matches the scenario allowlist |
| REVIEW | validation | Kubernetes dry-run validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
