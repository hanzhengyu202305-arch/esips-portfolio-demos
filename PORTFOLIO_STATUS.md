# Portfolio Status

Overall status: **PASS**

Generated at: `2026-07-10T02:18:47+00:00`

| check | status | command |
| --- | --- | --- |
| top-level tests | PASS | `make test AEGISOPS_PY=python3` |
| AegisOps acceptance | PASS | `make -C aegisops-agent acceptance PYTHON=python3` |
| AegisOps patch review queue | PASS | `make -C aegisops-agent patch-review-queue PYTHON=python3` |
| Kube Copilot report | PASS | `make -C kube-copilot report` |
| Kube Policy Pack | PASS | `make -C kube-copilot policy-pack` |
| Haul Truck Planner report | PASS | `make -C haul-truck-planner report` |
| adversarial review | PASS | `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 scripts/adversarial_review.py` |
| EvidenceOps scorecard | PASS | `make -C evidenceops-scorecard report` |
| public boundary check | PASS | `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 scripts/public_boundary_check.py` |
| EvidenceOps release gate | PASS | `make -C evidenceops-scorecard release-gate` |

## Boundary

This status file is generated from local deterministic checks. It does not prove production readiness and does not include private application material.
