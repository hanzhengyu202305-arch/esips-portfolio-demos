# PR Summary

## Incident

GitHub Actions failure because APP_MODE is missing

## Root Cause

`missing_app_mode_env` with confidence `0.77`.

Decision: `PROPOSE_PATCH` because highest-scoring hypothesis has sufficient evidence and separation.

CI starts the app with an empty APP_MODE environment variable.

## Files Changed

- `ci/env.example.yml`

## Validation

Validation: passed

Commands run:

- `python3 -m pytest apps/demo-api/tests -q`
- `python3 scripts/lint.py`
- `python3 scripts/devops_check.py --scenario S3 --patched-dir reports/S3/single/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `single`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.33`
- estimated_cost_usd: `0.000216`
- tool_calls: `6`
