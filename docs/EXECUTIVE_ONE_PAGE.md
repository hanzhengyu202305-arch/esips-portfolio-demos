# ESIPS Portfolio Executive Overview

## Thesis

**AI software engineering with validation: turning industry briefs into reproducible, testable, reviewable engineering demos.**

This portfolio is one coherent story, not three unrelated mini-projects. The common pattern is:

```text
industry brief -> scoped prototype -> deterministic validation -> report -> human-review boundary
```

EvidenceOps Scorecard adds the fourth layer: public evidence readiness.

## Three Lines

| Preference | Project | What it proves | Evidence |
| --- | --- | --- | --- |
| `Accenture_02 SDLC_Agents` | AegisOps Agent | RAG/runbook retrieval -> RCA -> patch preview -> validation -> report | [`aegisops-agent/reports/final-portfolio-report.md`](../aegisops-agent/reports/final-portfolio-report.md), [`aegisops-agent/reports/S4/multi/pr-summary.md`](../aegisops-agent/reports/S4/multi/pr-summary.md) |
| `Accenture_01 Kubernetes_DevOps` | Kube Copilot | Docker/Kubernetes/GitHub Actions generation plus deterministic validation | [`kube-copilot/reports/risk-comparison.md`](../kube-copilot/reports/risk-comparison.md), [`kube-copilot/reports/policy-matrix.md`](../kube-copilot/reports/policy-matrix.md) |
| `RTSIH electric haul truck trajectory planning` | Haul Truck Planner | Battery reserve, grade, charging access, perception risk, and energy-aware planning | [`haul-truck-planner/reports/route-experiment.md`](../haul-truck-planner/reports/route-experiment.md), [`haul-truck-planner/reports/algorithm-comparison.md`](../haul-truck-planner/reports/algorithm-comparison.md) |
| Portfolio evidence readiness | EvidenceOps Scorecard | Checks public evidence artifacts, reports, status files, and manual-review boundaries | [`evidenceops-scorecard/reports/evidence-scorecard.md`](../evidenceops-scorecard/reports/evidence-scorecard.md), [`evidenceops-scorecard/reports/submission-readiness.md`](../evidenceops-scorecard/reports/submission-readiness.md) |

## Main Project And Supporting Lines

| role | project | why it is placed there |
| --- | --- | --- |
| Main story | AegisOps Agent | Best fit for SDLC agents and the strongest evidence for AI-assisted software engineering workflow. |
| DevOps/platform support | Kube Copilot | Shows Kubernetes and CI/CD generation is useful only when policy validation and human review are explicit. |
| EE/mining support | Haul Truck Planner | Keeps the Electrical Engineering and mining-systems angle visible through constrained route planning. |
| Evidence layer | EvidenceOps Scorecard | Shows the public portfolio can be audited by generated evidence, not only narrative. |

## 2-Minute Reviewer Path

1. Read this page.
2. Open [`README.md`](../README.md) and scan the Reviewer Fast Path.
3. Open [`THREE_LINE_ESIPS_PLAN.md`](../THREE_LINE_ESIPS_PLAN.md) for the application framing.
4. Inspect the S4 AegisOps PR-style summary: [`aegisops-agent/reports/S4/multi/pr-summary.md`](../aegisops-agent/reports/S4/multi/pr-summary.md).

## 10-Minute Evidence Path

| demo | command | report |
| --- | --- | --- |
| AegisOps Agent | `make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13` | [`aegisops-agent/reports/S4/multi/issue-to-pr-report.md`](../aegisops-agent/reports/S4/multi/issue-to-pr-report.md) |
| Kube Copilot | `make -C kube-copilot report` | [`kube-copilot/reports/risk-comparison.md`](../kube-copilot/reports/risk-comparison.md) |
| Haul Truck Planner | `make -C haul-truck-planner report` | [`haul-truck-planner/reports/algorithm-comparison.md`](../haul-truck-planner/reports/algorithm-comparison.md) |
| EvidenceOps Scorecard | `make -C evidenceops-scorecard report` | [`evidenceops-scorecard/reports/evidence-scorecard.md`](../evidenceops-scorecard/reports/evidence-scorecard.md) |
| Whole portfolio | `make portfolio-check` | [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md) |

## Boundaries

- These are synthetic, local, reproducible portfolio demos.
- They are not production systems.
- Generated Kubernetes manifests and patch previews require validation and human review.
- Haul Truck Planner is a simplified planning prototype, not a production mine dispatch optimizer.
- EvidenceOps Scorecard checks local public evidence only; it does not approve an application.
- Private application material, credentials, academic records, mailbox content, and local machine paths do not belong in the public repo.
