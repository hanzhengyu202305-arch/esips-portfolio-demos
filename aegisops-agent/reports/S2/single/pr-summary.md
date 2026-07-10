# PR Summary

## Incident

Docker build failure because a dependency is missing

## Root Cause

`missing_python_dependency` with confidence `0.87`.

Decision: `PROPOSE_PATCH` because highest-scoring hypothesis has sufficient evidence and separation.

Docker build imports pydantic but the image requirements omit it.

## Files Changed

- `apps/demo-api/requirements.txt`

## Validation

Validation: passed

Commands run:

- `python3 -m pytest apps/demo-api/tests -q`
- `python3 scripts/lint.py`
- `python3 scripts/devops_check.py --scenario S2 --patched-dir reports/S2/single/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `single`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.32`
- estimated_cost_usd: `0.000218`
- tool_calls: `6`
