# PR Summary

## Incident

pytest failure because discount logic is wrong

## Root Cause

`wrong_discount_logic` with confidence `0.93`.

pytest assertion fails because gold customer discount is 1% instead of 10%.

## Files Changed

- `apps/demo-api/app/service.py`

## Validation

Validation: passed

Commands run:

- `/opt/anaconda3/bin/python3.13 -m pytest apps/demo-api/tests -q`
- `/opt/anaconda3/bin/python3.13 scripts/lint.py`
- `/opt/anaconda3/bin/python3.13 scripts/devops_check.py --scenario S1 --patched-dir reports/S1/single/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `single`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.397`
- estimated_cost_usd: `0.000214`
- tool_calls: `6`
