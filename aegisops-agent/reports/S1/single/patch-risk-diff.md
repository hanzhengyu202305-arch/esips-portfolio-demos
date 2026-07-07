# Patch Risk Diff

- scenario: `S1`
- root_cause_id: `wrong_discount_logic`
- overall_status: `REVIEW`
- recommended_owner: `application reviewer`

## Files Changed

- `apps/demo-api/app/service.py`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | apps/demo-api/app/service.py matches the scenario allowlist |
| REVIEW | validation | pytest validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
