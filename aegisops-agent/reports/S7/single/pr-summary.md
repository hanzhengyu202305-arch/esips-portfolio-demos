# PR Summary

## Incident

Container security failure because the API runs as root

## Root Cause

`container_runs_as_root` with confidence `0.87`.

Decision: `PROPOSE_PATCH` because highest-scoring hypothesis has sufficient evidence and separation.

Policy validation flags a root container and missing privilege escalation controls.

## Files Changed

- `k8s/overlays/insecure/deployment.yaml`

## Validation

Validation: passed

Commands run:

- `python3 -m pytest apps/demo-api/tests -q`
- `python3 scripts/lint.py`
- `python3 scripts/devops_check.py --scenario S7 --patched-dir reports/S7/single/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `single`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.37`
- estimated_cost_usd: `0.000213`
- tool_calls: `6`
