# Patch Risk Diff

- scenario: `S3`
- root_cause_id: `missing_app_mode_env`
- overall_status: `REVIEW`
- recommended_owner: `devex reviewer`

## Files Changed

- `ci/env.example.yml`

## Findings

| status | area | message |
| --- | --- | --- |
| PASS | target guardrail | ci/env.example.yml matches the scenario allowlist |
| REVIEW | validation | CI dry-run validation must pass and be reviewed |

## Boundary

Human review required before merge or deployment.
This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.
