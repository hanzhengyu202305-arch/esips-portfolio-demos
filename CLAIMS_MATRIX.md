# Claims Matrix

| Claim | Status | Evidence | Boundary |
| --- | --- | --- | --- |
| AegisOps demonstrates agentic DevOps RCA. | verified from repo | [`aegisops-agent/reports/final-portfolio-report.md`](aegisops-agent/reports/final-portfolio-report.md), [`aegisops-agent/reports/S4/multi/issue-to-pr-report.md`](aegisops-agent/reports/S4/multi/issue-to-pr-report.md) | synthetic/local demo; not production automation |
| Kube Copilot validates generated Kubernetes/CI-CD files. | verified from repo | [`kube-copilot/reports/risk-comparison.md`](kube-copilot/reports/risk-comparison.md), [`kube-copilot/reports/policy-matrix.md`](kube-copilot/reports/policy-matrix.md), [`kube-copilot/reports/policy-pack.md`](kube-copilot/reports/policy-pack.md) | not a production scanner or admission controller |
| Haul Truck Planner demonstrates energy-aware route planning. | verified from repo | [`haul-truck-planner/reports/route-experiment.md`](haul-truck-planner/reports/route-experiment.md), [`haul-truck-planner/reports/algorithm-comparison.md`](haul-truck-planner/reports/algorithm-comparison.md) | simplified mine-grid prototype; not fleet dispatch |
| EvidenceOps Scorecard checks public portfolio evidence quality. | verified from repo | [`evidenceops-scorecard/reports/evidence-scorecard.md`](evidenceops-scorecard/reports/evidence-scorecard.md), [`evidenceops-scorecard/reports/submission-readiness.md`](evidenceops-scorecard/reports/submission-readiness.md) | not official application approval |
| Current ESIPS deadline. | needs official confirmation | current official system before submission | do not hard-code in public repo |
| SONIA exact fields. | needs official confirmation | current official form before submission | private application pack only |
| CV/transcript/GitHub requirement. | needs official confirmation | current official form before submission | private pack only; do not publish personal documents |
| SCDL3991 EE credit substitution. | needs official confirmation | faculty/school approval | do not claim substitution without approval |
| ELEC5308-style wording. | technical inspiration only | README and project boundary notes | perception + planning language, not official coursework output |

## External Reference Boundary

| Reference family | Safe use | Do not claim |
| --- | --- | --- |
| Agentic software engineering projects | Use as ecosystem language for issue/failure -> patch preview -> validation. | AegisOps is equivalent to SWE-agent, SWE-bench, OpenHands, or LangGraph. |
| Kubernetes official docs and validators | Use as justification for deterministic checks around resources, probes, security context, and CI. | Kube Copilot replaces kube-linter, kubeconform, Kyverno, Gatekeeper, or production admission control. |
| Robotics and EV routing references | Use as vocabulary for A*, Dijkstra, vehicle routing, charging, reserve, and constraints. | Haul Truck Planner is a production mine dispatch or EV routing optimiser. |
| Evidence and supply-chain references | Use as vocabulary for scorecards, release gates, public artifact checks, and review readiness. | EvidenceOps is OpenSSF Scorecard, a SLSA implementation, or regulatory certification. |

## Safe Portfolio Statement

These are local, synthetic, reproducible portfolio demos. The value is in the engineering workflow, validation, reporting, and clear limitations. Generated Kubernetes manifests and patch previews require validation and human review.
