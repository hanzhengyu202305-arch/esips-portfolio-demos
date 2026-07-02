# PR Summary

## Incident

GitHub Actions failure because APP_MODE is missing

## Root Cause

`missing_app_mode_env` with confidence `0.97`.

CI starts the app with an empty APP_MODE environment variable.

## Files Changed

- `ci/env.example.yml`

## Validation

Validation: passed

Commands run:

- `/opt/anaconda3/bin/python3.13 -m pytest apps/demo-api/tests -q`
- `/opt/anaconda3/bin/python3.13 scripts/lint.py`
- `/opt/anaconda3/bin/python3.13 scripts/devops_check.py --scenario S3 --patched-dir reports/S3/multi/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `multi`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.405`
- estimated_cost_usd: `0.000327`
- tool_calls: `10`
