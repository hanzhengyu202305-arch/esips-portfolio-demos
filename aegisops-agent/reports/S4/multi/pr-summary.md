# PR Summary

## Incident

Kubernetes CrashLoopBackOff because APP_MODE is invalid

## Root Cause

`invalid_app_mode_env` with confidence `0.89`.

Decision: `PROPOSE_PATCH` because highest-scoring hypothesis has sufficient evidence and separation.

Pod restarts because APP_MODE is set to an unsupported value.

## Files Changed

- `k8s/overlays/broken-env/deployment.yaml`

## Validation

Validation: passed

Commands run:

- `python3 -m pytest apps/demo-api/tests -q`
- `python3 scripts/lint.py`
- `python3 scripts/devops_check.py --scenario S4 --patched-dir reports/S4/multi/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `multi`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.39`
- estimated_cost_usd: `0.000328`
- tool_calls: `10`
