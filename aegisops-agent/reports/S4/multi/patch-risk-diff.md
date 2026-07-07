# Patch Risk Diff

- scenario: `S4`
- root_cause_id: `invalid_app_mode_env`
- overall_status: `REVIEW`
- recommended_owner: `platform reviewer`

## Files Changed

- `k8s/overlays/broken-env/deployment.yaml`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | k8s/overlays/broken-env/deployment.yaml matches the scenario allowlist |
| REVIEW | kubernetes image | image tag still uses latest and needs reviewer confirmation |
| REVIEW | validation | Kubernetes dry-run validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
