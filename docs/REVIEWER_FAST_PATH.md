# Reviewer Fast Path

## 2-Minute Path

1. Read the thesis in [`docs/EXECUTIVE_ONE_PAGE.md`](EXECUTIVE_ONE_PAGE.md).
2. Confirm the three project mapping in [`THREE_LINE_ESIPS_PLAN.md`](../THREE_LINE_ESIPS_PLAN.md).
3. Open the main evidence artifact: [`aegisops-agent/reports/S4/multi/pr-summary.md`](../aegisops-agent/reports/S4/multi/pr-summary.md).

## 10-Minute Evidence Path

| project | inspect first | why |
| --- | --- | --- |
| AegisOps Agent | [`aegisops-agent/reports/S4/multi/issue-to-pr-report.md`](../aegisops-agent/reports/S4/multi/issue-to-pr-report.md) | Shows issue -> evidence -> RCA -> patch -> validation -> PR summary. |
| Kube Copilot | [`kube-copilot/reports/policy-matrix.md`](../kube-copilot/reports/policy-matrix.md) | Shows deterministic Kubernetes policy checks. |
| Haul Truck Planner | [`haul-truck-planner/reports/algorithm-comparison.md`](../haul-truck-planner/reports/algorithm-comparison.md) | Shows shortest path vs Dijkstra vs A* under energy constraints. |
| Whole repo | [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md) | Shows the latest local verification gate. |

## 30-Minute Local Validation

```bash
make test
make portfolio-check
make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13
make -C kube-copilot report
make -C haul-truck-planner report
```

If the local AegisOps Python path differs:

```bash
make portfolio-check AEGISOPS_PY=python3
```

## Reviewer Boundary

The useful evidence is the reproducible workflow, not a production claim. The demos use local fixtures, deterministic checks, and generated reports so they can be inspected without external accounts, cloud credentials, or private data.
