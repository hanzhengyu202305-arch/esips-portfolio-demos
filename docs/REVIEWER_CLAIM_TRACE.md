# Reviewer Claim Trace

This file maps reviewer-facing claims to public evidence, regeneration commands, and claim boundaries. It is the safest path for checking that the portfolio story is supported by runnable artifacts.

## Claim-To-Evidence Table

| claim | strongest public evidence | regeneration command | current status | boundary |
| --- | --- | --- | --- | --- |
| AegisOps Agent shows an SDLC agent workflow from incident evidence to RCA, patch preview, validation, and report. | [`aegisops-agent/reports/S4/multi/issue-to-pr-report.md`](../aegisops-agent/reports/S4/multi/issue-to-pr-report.md), [`aegisops-agent/reports/S4/multi/pr-summary.md`](../aegisops-agent/reports/S4/multi/pr-summary.md) | `make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=<python>` | verified by `make demo-all` and `make portfolio-check` | deterministic local demo, not a full autonomous developer platform |
| AegisOps can rank multiple incidents before remediation. | [`aegisops-agent/reports/triage-queue.md`](../aegisops-agent/reports/triage-queue.md) | `make -C aegisops-agent triage PYTHON=<python>` | verified by `make demo-all` and `make portfolio-check` | synthetic priority scoring only, not incident-management software |
| Patch Risk Diff connects AegisOps patch preview with policy-style review. | [`aegisops-agent/reports/S4/multi/patch-risk-diff.md`](../aegisops-agent/reports/S4/multi/patch-risk-diff.md) | `make -C aegisops-agent patch-risk SCENARIO=S4 MODE=multi PYTHON=<python>` | verified by `make demo-all` and `make portfolio-check` | static review heuristics only, not a production security scanner |
| Kube Copilot shows generated Kubernetes and CI/CD artifacts must pass validation before review. | [`kube-copilot/reports/risk-comparison.md`](../kube-copilot/reports/risk-comparison.md), [`kube-copilot/reports/policy-matrix.md`](../kube-copilot/reports/policy-matrix.md) | `make -C kube-copilot report` | verified by `make demo-all` and `make portfolio-check` | pre-deployment checks only, not cluster admission control |
| Haul Truck Planner shows electric haul routing must consider battery reserve, charging access, grade, and perception risk. | [`haul-truck-planner/reports/route-experiment.md`](../haul-truck-planner/reports/route-experiment.md), [`haul-truck-planner/reports/algorithm-comparison.md`](../haul-truck-planner/reports/algorithm-comparison.md) | `make -C haul-truck-planner report` | verified by `make demo-all` and `make portfolio-check` | simplified planning prototype, not mine dispatch software |
| EvidenceOps Scorecard checks whether the public evidence package is complete enough to review. | [`evidenceops-scorecard/reports/evidence-scorecard.md`](../evidenceops-scorecard/reports/evidence-scorecard.md), [`evidenceops-scorecard/reports/submission-readiness.md`](../evidenceops-scorecard/reports/submission-readiness.md) | `make -C evidenceops-scorecard report` | verified by `make demo-all` and `make portfolio-check` | evidence inventory only, not application approval or compliance certification |
| The whole portfolio can be regenerated and reviewed locally. | [`docs/DEMO_OUTPUT_INDEX.md`](DEMO_OUTPUT_INDEX.md), [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md) | `make demo-all && make portfolio-check` | reviewed by local validation gates | local environment must have the required Python tooling |
| Final submission details require current official confirmation. | Current official public source and active application form | manual check before submission | needs official confirmation | do not hard-code changing submission fields in the public repository |

## Reviewer Checks

Run the short path:

```bash
make demo-all
make portfolio-check
```

Then inspect:

- [`docs/DEMO_OUTPUT_INDEX.md`](DEMO_OUTPUT_INDEX.md)
- [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md)
- [`CLAIMS_MATRIX.md`](../CLAIMS_MATRIX.md)

## Safe Interview Wording

Use this wording:

> This portfolio is a set of deterministic, local demos showing how I turn industry briefs into reproducible engineering evidence. The strongest line is AegisOps Agent for SDLC remediation. Kube Copilot and Haul Truck Planner support the same validation story from Kubernetes and EE/mining planning angles. EvidenceOps Scorecard then checks whether the public evidence is present, reviewable, and bounded.

Avoid saying:

- The demos are production systems.
- The scorecard is formal approval.
- The planning prototype is a full dispatch optimiser.
- The Kubernetes checks replace production scanners or admission policy.
- The SDLC agent equals a mature autonomous software-engineering platform.
