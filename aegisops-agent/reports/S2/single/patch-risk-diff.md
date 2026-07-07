# Patch Risk Diff

- scenario: `S2`
- root_cause_id: `missing_python_dependency`
- overall_status: `REVIEW`
- recommended_owner: `platform reviewer`

## Files Changed

- `apps/demo-api/requirements.txt`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | apps/demo-api/requirements.txt matches the scenario allowlist |
| REVIEW | validation | Docker dry-run validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
