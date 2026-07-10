# ESIPS Reviewer Guide

Portfolio thesis: **AI software engineering with validation: turning industry briefs into reproducible, testable, reviewable engineering demos.**

This portfolio is not three unrelated mini-projects. It is one reviewer-facing product story: each demo generates or plans something, then validates it, reports it, and states its boundary.

## Three-Line Map

| ESIPS preference | project | what it proves | first report |
| --- | --- | --- | --- |
| `Accenture_02 SDLC_Agents` | `aegisops-agent` | An AI-assisted DevOps RCA workflow can move from incident evidence to a guarded, human-reviewable patch preview. | [`aegisops-agent/reports/final-portfolio-report.md`](../aegisops-agent/reports/final-portfolio-report.md) |
| `Accenture_01 Kubernetes_DevOps` | `kube-copilot` | AI-drafted infrastructure is not trusted until Kubernetes policy checks and human review pass. | [`kube-copilot/reports/risk-comparison.md`](../kube-copilot/reports/risk-comparison.md) |
| `RTSIH electric haul truck trajectory planning` | `haul-truck-planner` | Electric haul routing must consider battery reserve, grade, charging access, and perception risk, not only shortest path. | [`haul-truck-planner/reports/route-experiment.md`](../haul-truck-planner/reports/route-experiment.md) |

Read the short application framing in [`THREE_LINE_ESIPS_PLAN.md`](../THREE_LINE_ESIPS_PLAN.md).

## Evidence Path

| demo | command | evidence to inspect |
| --- | --- | --- |
| AegisOps Agent | `make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=python3` | [`aegisops-agent/reports/S4/multi/demo-report.md`](../aegisops-agent/reports/S4/multi/demo-report.md), [`aegisops-agent/reports/S4/multi/pr-summary.md`](../aegisops-agent/reports/S4/multi/pr-summary.md) |
| Kube Copilot | `make -C kube-copilot report` | [`kube-copilot/reports/risk-comparison.md`](../kube-copilot/reports/risk-comparison.md) |
| Haul Truck Planner | `make -C haul-truck-planner report` | [`haul-truck-planner/reports/route-experiment.md`](../haul-truck-planner/reports/route-experiment.md) |
| Whole portfolio | `make portfolio-check` | [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md), [`PORTFOLIO_STATUS.json`](../PORTFOLIO_STATUS.json) |

If the local Python path differs, run:

```bash
make portfolio-check AEGISOPS_PY=python3
```

## What Each Demo Proves

| project | technical claim | validation boundary |
| --- | --- | --- |
| AegisOps Agent | Evidence collection, runbook retrieval, deterministic RCA, patch preview, validation logs, and PR-style reporting can be connected into one SDLC workflow. | Patch targets are checked against scenario allowlists, tests are run locally, and generated patches remain review previews. |
| Kube Copilot | Kubernetes manifests, Dockerfiles, and CI workflows can be generated from structured requirements. | Policy checks reject unsafe image tags, missing resource controls, missing probes, weak security contexts, and absent CI. |
| Haul Truck Planner | Energy-aware routing can reject shortest paths that violate battery reserve and find feasible charging-aware alternatives. | The mine map is synthetic, Dijkstra remains the correctness baseline, and A* is a small algorithmic comparison. |

## Do Not Overclaim

| safe claim | avoid saying |
| --- | --- |
| "This is a deterministic local portfolio demo." | "This is ready for autonomous production DevOps." |
| "The data and incidents are synthetic fixtures." | "This used live company, university, or customer data." |
| "The Kube validator demonstrates policy-style checks." | "This replaces production scanners or admission controllers." |
| "The route planner is a small constrained-planning experiment." | "This is a production mine dispatch optimizer." |
| "ELEC5308-style means perception + planning vocabulary." | "This is an official ELEC5308 submission or certification." |

## Five-Minute Interview Demo Script

1. Open the top-level README and state the thesis: AI software engineering with validation.
2. Open `THREE_LINE_ESIPS_PLAN.md` and show why AegisOps is the main line.
3. Run `make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=python3`.
4. Open [`aegisops-agent/reports/S4/multi/pr-summary.md`](../aegisops-agent/reports/S4/multi/pr-summary.md) and point to root cause, allowed file, validation, and metrics.
5. Open [`kube-copilot/reports/risk-comparison.md`](../kube-copilot/reports/risk-comparison.md) to show the generated-config trust boundary.
6. Open [`haul-truck-planner/reports/route-experiment.md`](../haul-truck-planner/reports/route-experiment.md) to show shortest path versus constrained planning.
7. Close with the boundary: local fixtures, reproducible commands, no production mutation, human review required.

## Follow-Up Questions To Prepare

- Why is the deterministic `MockLLM` a strength for an interview demo?
- How would AegisOps change if connected to a real issue tracker and CI system?
- Which Kube checks belong in CI and which belong in admission control?
- Why can the shortest haul-truck route be operationally invalid?
- How would the A* heuristic need to be designed to preserve correctness under charging constraints?
