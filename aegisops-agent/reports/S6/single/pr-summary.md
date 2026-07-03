# PR Summary

## Incident

Kubernetes ImagePullBackOff because image tag is missing

## Root Cause

`image_tag_mismatch` with confidence `0.93`.

Deployment references an image tag that does not exist in the local registry.

## Files Changed

- `k8s/overlays/healthy/kustomization.yaml`

## Validation

Validation: passed

Commands run:

- `/opt/anaconda3/bin/python3.13 -m pytest apps/demo-api/tests -q`
- `/opt/anaconda3/bin/python3.13 scripts/lint.py`
- `/opt/anaconda3/bin/python3.13 scripts/devops_check.py --scenario S6 --patched-dir reports/S6/single/patched`

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `single`
- root_cause_correct: `True`
- fix_successful: `True`
- latency_seconds: `0.415`
- estimated_cost_usd: `0.000213`
- tool_calls: `6`
