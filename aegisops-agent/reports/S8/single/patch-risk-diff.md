# Patch Risk Diff

- scenario: `S8`
- root_cause_id: `nested_loop_latency_regression`
- overall_status: `REVIEW`
- recommended_owner: `application performance reviewer`

## Files Changed

- `apps/demo-api/app/service.py`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | apps/demo-api/app/service.py matches the scenario allowlist |
| REVIEW | performance | benchmark dry-run evidence should be reviewed before merge |
| REVIEW | validation | benchmark dry-run validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
