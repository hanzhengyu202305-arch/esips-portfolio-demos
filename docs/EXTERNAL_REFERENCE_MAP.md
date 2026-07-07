# External Reference Map

Reviewed on 2026-07-06. This file links the portfolio demos to public, authoritative, or mature open-source references. The references are used for positioning and next-step language, not as copied implementations or production-readiness claims.

## Official ESIPS Context

| source | what it supports | how to use it safely |
| --- | --- | --- |
| [University of Sydney Engineering Sydney Industry Placement Scholarship](https://www.sydney.edu.au/engineering/study/scholarships/engineering-sydney-industry-placement-scholarship.html) | ESIPS is an industry placement scholarship context and the official source family for current requirements. | Use it as the public official anchor. Do not hard-code deadlines or application fields in this repo. |

## AegisOps Agent: Agentic SDLC References

| source | useful pattern | how AegisOps uses the idea | boundary |
| --- | --- | --- | --- |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | Issue/failure context to attempted code change. | AegisOps uses a local S4 issue fixture and produces evidence, diagnosis, patch preview, validation, and PR-style summary. | Not equivalent to SWE-agent; no real GitHub automation by default. |
| [SWE-bench](https://github.com/swe-bench/SWE-bench) | Software-engineering agents are often evaluated through real issue-to-patch tasks. | AegisOps borrows the review shape: issue, evidence, patch, and validation. | Synthetic scenarios only, not benchmark results. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Mature autonomous software-engineering platform direction. | The portfolio uses the same broad problem space but keeps the scope deterministic and local. | Not a full autonomous developer platform. |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Graph-style agent workflows and multi-step stateful orchestration. | AegisOps frames single-agent and multi-agent RCA as workflow design, not a chatbot answer. | No dependency on LangGraph in the default demo. |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | Public repository security-posture checks. | Useful next-step language for repository hardening beyond the portfolio demo. | Not currently part of the validation gate. |

Current AegisOps patch review evidence now includes [`aegisops-agent/reports/patch-review-queue.md`](../aegisops-agent/reports/patch-review-queue.md), which keeps the issue-to-patch inspiration but limits the claim to deterministic local fixtures and human-review prioritisation.

## Kube Copilot: Kubernetes Validation References

| source | useful pattern | how Kube Copilot uses the idea | boundary |
| --- | --- | --- | --- |
| [Kubernetes resource management docs](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) | CPU and memory requests/limits are core scheduling and reliability controls. | Validator checks CPU/memory requests and limits. | Demonstration check only. |
| [Kubernetes probe docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) | Readiness and liveness probes support rollout and recovery behavior. | Validator checks readiness and liveness probes. | Does not run a real cluster health model. |
| [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) | Non-root execution, privileged-container avoidance, and privilege-escalation controls are part of the official security posture vocabulary. | Validator groups these findings as blocking issues. | Pre-deployment review only; not cluster enforcement. |
| [Kubernetes Security Context docs](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) | Pod and container security settings are configured through `securityContext`. | Supports the security-context rule language in the report. | Demonstration check only. |
| [kube-linter](https://github.com/stackrox/kube-linter) | Static analysis for Kubernetes YAML. | Kube Copilot mirrors the idea of readable pre-deployment findings. | Not a replacement scanner. |
| [kubeconform](https://github.com/yannh/kubeconform) | Fast manifest validation. | Generated YAML is treated as draft material until checks pass. | Does not perform full schema validation. |
| [Kyverno](https://github.com/kyverno/kyverno) and [Gatekeeper](https://github.com/open-policy-agent/gatekeeper) | Policy-as-code and admission-control direction. | This repo uses policy vocabulary for pre-deployment review. | Not an admission controller. |

## Haul Truck Planner: Planning And EV Routing References

| source | useful pattern | how Haul Truck Planner uses the idea | boundary |
| --- | --- | --- | --- |
| [PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics) | Clear robotics path-planning examples including grid search and A*. | The demo compares shortest path, battery-state Dijkstra, and A* on an inspectable grid. | Not a full robotics stack. |
| [Google OR-Tools routing documentation](https://developers.google.com/optimization/routing) | Vehicle routing and constrained route optimisation vocabulary. | The next-step language can mention richer EV routing constraints such as time windows and charging. | Current demo is not an OR-Tools solver. |
| [EVRPTW-PR-ALNS](https://github.com/wornSweater/EVRPTW-PR-ALNS) | Electric-vehicle routing with partial recharge strategy. | Supports the idea that charging access and battery state matter operationally. | Not a fleet dispatch or industrial optimiser. |

## EvidenceOps Scorecard: Evidence Readiness References

| source | useful pattern | how EvidenceOps uses the idea | boundary |
| --- | --- | --- | --- |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | Automated checks can summarize repository health and review risk. | EvidenceOps applies the scorecard pattern to portfolio evidence artifacts. | Not the OpenSSF tool and not a formal repository rating. |
| [SLSA](https://slsa.dev/) | Evidence, provenance, and release-gate vocabulary. | EvidenceOps uses the same style of traceable public artifacts and validation gates. | Not a SLSA compliance implementation. |
| [OpenTelemetry documentation](https://opentelemetry.io/docs/) | Observability vocabulary for traces, metrics, and logs. | EvidenceOps treats reports and status files as visible evidence signals. | Does not instrument a live distributed system. |
| [Google SRE monitoring chapter](https://sre.google/sre-book/monitoring-distributed-systems/) | Reliability work should use visible, actionable signals. | EvidenceOps keeps public portfolio evidence explicit and inspectable. | Not production SRE monitoring. |

## Interview Use

Use these references to show that the three demos sit in mature engineering ecosystems:

- AegisOps: agentic software engineering and issue-to-patch workflow.
- Kube Copilot: Kubernetes policy validation and generated-IaC trust boundaries.
- Haul Truck Planner: path planning plus EV routing constraints.
- EvidenceOps Scorecard: public evidence readiness, release gates, and claim boundaries.

Do not say the portfolio matches or replaces any of these projects. The safe claim is that the portfolio implements smaller, deterministic, reviewable demos inspired by the same engineering patterns.
