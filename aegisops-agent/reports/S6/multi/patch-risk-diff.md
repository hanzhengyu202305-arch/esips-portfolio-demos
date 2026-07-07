# Patch Risk Diff

- scenario: `S6`
- root_cause_id: `image_tag_mismatch`
- overall_status: `REVIEW`
- recommended_owner: `platform reviewer`

## Files Changed

- `k8s/overlays/healthy/kustomization.yaml`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | k8s/overlays/healthy/kustomization.yaml matches the scenario allowlist |
| REVIEW | validation | Kubernetes dry-run validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
