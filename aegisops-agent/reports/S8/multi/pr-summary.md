# PR Summary

## Incident

Latency regression because order scoring uses a nested loop

## Root Cause

`nested_loop_latency_regression` with confidence `0.97`.

The scoring path regressed after adding an O(n^2) customer aggregation loop.

## Files Changed

- `apps/demo-api/app/service.py`

## Validation

Validation: passed

Commands run:

- `/opt/anaconda3/bin/python3.13 -m pytest apps/demo-api/tests -q`
- `/opt/anaconda3/bin/python3.13 scripts/lint.py`
- `/opt/anaconda3/bin/python3.13 scripts/devops_check.py --scenario S8 --patched-dir reports/S8/multi/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `multi`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.392`
- estimated_cost_usd: `0.000325`
- tool_calls: `10`
