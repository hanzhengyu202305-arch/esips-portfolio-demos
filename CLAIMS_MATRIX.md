# Claims Matrix

| Claim | Status | Evidence | Boundary |
| --- | --- | --- | --- |
| AegisOps demonstrates evidence-derived DevOps RCA. | verified from repo | [`aegisops-agent/reports/S4/multi/diagnosis.json`](aegisops-agent/reports/S4/multi/diagnosis.json), [`docs/ADVERSARIAL_REVIEW.md`](docs/ADVERSARIAL_REVIEW.md) | deterministic rule harness and synthetic fixtures; not a live LLM or production automation |
| AegisOps stops remediation when evidence is missing or conflicting. | verified from adversarial controls | [`docs/ADVERSARIAL_REVIEW.json`](docs/ADVERSARIAL_REVIEW.json) | controlled negative cases, not a formal safety proof |
| AegisOps can rank proposed patch reviews across scenarios. | verified from repo | [`aegisops-agent/reports/patch-review-queue.md`](aegisops-agent/reports/patch-review-queue.md), [`aegisops-agent/reports/S4/multi/patch-risk-diff.md`](aegisops-agent/reports/S4/multi/patch-risk-diff.md) | deterministic review heuristics; not a production scanner or code-review replacement |
| Kube Copilot validates parsed Kubernetes manifests across YAML documents and containers. | verified from repo | [`kube-copilot/reports/adversarial-validation.md`](kube-copilot/reports/adversarial-validation.md), [`kube-copilot/reports/policy-pack.md`](kube-copilot/reports/policy-pack.md) | focused policy subset; not schema validation, a production scanner, or admission control |
| Haul Truck Planner demonstrates energy-aware route planning with explicit model assumptions. | verified from repo | [`haul-truck-planner/reports/route-experiment.md`](haul-truck-planner/reports/route-experiment.md), [`docs/ADVERSARIAL_REVIEW.md`](docs/ADVERSARIAL_REVIEW.md) | simplified mine-grid model with synthetic parameters; not trajectory control or fleet dispatch |
| EvidenceOps Scorecard checks public evidence completeness and structured consistency. | verified from repo | [`evidenceops-scorecard/reports/evidence-scorecard.md`](evidenceops-scorecard/reports/evidence-scorecard.md), [`evidenceops-scorecard/reports/release-gate.md`](evidenceops-scorecard/reports/release-gate.md) | self-authored completeness gate; not independent quality certification or official application approval |
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
