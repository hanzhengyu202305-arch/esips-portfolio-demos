# PR Summary

## Incident

Kubernetes readiness probe path is wrong

## Root Cause

`wrong_readiness_probe_path` with confidence `0.87`.

Decision: `PROPOSE_PATCH` because highest-scoring hypothesis has sufficient evidence and separation.

The pod is running but not ready because readiness probes call /readyz.

## Files Changed

- `k8s/overlays/broken-probe/deployment.yaml`

## Validation

Validation: passed

Commands run:

- `python3 -m pytest apps/demo-api/tests -q`
- `python3 scripts/lint.py`
- `python3 scripts/devops_check.py --scenario S5 --patched-dir reports/S5/single/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `single`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.35`
- estimated_cost_usd: `0.000215`
- tool_calls: `6`
