# PR Summary

## Incident

Kubernetes readiness probe path is wrong

## Root Cause

`wrong_readiness_probe_path` with confidence `0.97`.

The pod is running but not ready because readiness probes call /readyz.

## Files Changed

- `k8s/overlays/broken-probe/deployment.yaml`

## Validation

Validation: passed

Commands run:

- `/opt/anaconda3/bin/python3.13 -m pytest apps/demo-api/tests -q`
- `/opt/anaconda3/bin/python3.13 scripts/lint.py`
- `/opt/anaconda3/bin/python3.13 scripts/devops_check.py --scenario S5 --patched-dir reports/S5/multi/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `multi`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.4`
- estimated_cost_usd: `0.000326`
- tool_calls: `10`
