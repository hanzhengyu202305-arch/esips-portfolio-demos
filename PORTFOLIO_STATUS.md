# Portfolio Status

Overall status: **PASS**

Generated at: `2026-07-06T08:44:02+00:00`

| check | status | command |
| --- | --- | --- |
| top-level tests | PASS | `make test AEGISOPS_PY=/opt/anaconda3/bin/python3.13` |
| AegisOps acceptance | PASS | `make -C aegisops-agent acceptance PYTHON=/opt/anaconda3/bin/python3.13` |
| Kube Copilot report | PASS | `make -C kube-copilot report` |
| Haul Truck Planner report | PASS | `make -C haul-truck-planner report` |
| public boundary check | PASS | `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 scripts/public_boundary_check.py` |

## Boundary

This status file is generated from local deterministic checks. It does not prove production readiness and does not include private application material.
