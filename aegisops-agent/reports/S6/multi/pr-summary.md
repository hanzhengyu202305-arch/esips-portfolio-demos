# PR Summary

## Incident

Kubernetes ImagePullBackOff because image tag is missing

## Root Cause

`image_tag_mismatch` with confidence `0.97`.

Deployment references an image tag that does not exist in the local registry.

## Files Changed

- `k8s/overlays/healthy/kustomization.yaml`

## Validation

Validation: passed

Commands run:

- `/opt/anaconda3/bin/python3.13 -m pytest apps/demo-api/tests -q`
- `/opt/anaconda3/bin/python3.13 scripts/lint.py`
- `/opt/anaconda3/bin/python3.13 scripts/devops_check.py --scenario S6 --patched-dir reports/S6/multi/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `multi`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.418`
- estimated_cost_usd: `0.000324`
- tool_calls: `10`
