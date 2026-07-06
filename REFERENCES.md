# Public References And Roadmap

This repository is a portfolio demo set, not a fork or copy of the projects below. The references show the engineering ecosystems that informed the three demo lines: agentic SDLC remediation, Kubernetes validation, and electric haul-truck route planning.

For the source-backed reviewer version, read [`docs/EXTERNAL_REFERENCE_MAP.md`](docs/EXTERNAL_REFERENCE_MAP.md).

## AegisOps Agent

Local demo: [`aegisops-agent`](aegisops-agent)

| reference | useful pattern | how this repo uses the idea |
| --- | --- | --- |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | GitHub issue to attempted code fix | A local CI/CD incident becomes evidence, RCA, patch preview, validation, and report. |
| [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | Compact agent loop | The demo keeps the workflow small enough to inspect in an interview. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Larger agentic software-engineering platform | AegisOps stays deterministic and local instead of claiming full autonomous development. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Graph-style agent workflows | The demo compares single-agent and multi-agent runs over fixed scenarios. |
| [SWE-bench](https://github.com/swe-bench/SWE-bench) | Issue-to-patch evaluation framing | AegisOps uses a smaller synthetic issue-to-PR evidence path without claiming benchmark results. |

Current evidence:

- `aegisops-agent/fixtures/issues/S4_crashloopbackoff_issue.md` starts from a GitHub-style issue fixture.
- `aegisops-agent/reports/S4/multi/issue-to-pr-report.md` shows issue -> evidence -> diagnosis -> patch preview -> validation -> PR summary.
- Keep deterministic fixtures as the default so validation is reproducible without credentials or API keys.
- Compare agent modes on accuracy, fix success, latency, and tool-call count.

## Kube Copilot

Local demo: [`kube-copilot`](kube-copilot)

| reference | useful pattern | how this repo uses the idea |
| --- | --- | --- |
| [kube-linter](https://github.com/stackrox/kube-linter) | Kubernetes static analysis | The validator flags risky generated manifests before review. |
| [kubeconform](https://github.com/yannh/kubeconform) | Manifest validation | Generated YAML is treated as incomplete until it passes validation. |
| [kube-score](https://github.com/zegl/kube-score) | Reliability and security recommendations | The report explains risks as review findings. |
| [Polaris](https://github.com/FairwindsOps/polaris) | Kubernetes best-practice auditing | The demo uses best-practice checks as rollout gates. |
| [Kyverno](https://github.com/kyverno/kyverno) | Policy as code | Kube Copilot frames generation plus checks as a policy-aware workflow. |
| [Gatekeeper](https://github.com/open-policy-agent/gatekeeper) | Kubernetes admission policy | This repo only demonstrates pre-deployment checks, not production admission control. |
| [Datree](https://github.com/datreeio/datree) | CI-friendly misconfiguration checks | The workflow treats CI and human review as the trust boundary. |
| [Kubernetes resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) | CPU/memory request and limit concepts | Validator checks generated manifests for resource controls. |
| [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) | Readiness/liveness health behavior | Validator checks generated manifests for rollout and recovery signals. |

Current evidence:

- `kube-copilot/docs/policy-rules.md` documents the policy table.
- `kube-copilot/fixtures/safe/`, `fixtures/partial/`, and `fixtures/risky/` show the validation cases.
- `kube-copilot/reports/policy-matrix.md` maps rules to reviewer-facing evidence.
- Keep checks readable and deterministic rather than trying to replace production scanners.

## Haul Truck Planner

Local demo: [`haul-truck-planner`](haul-truck-planner)

| reference | useful pattern | how this repo uses the idea |
| --- | --- | --- |
| [PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics) | Robotics path-planning examples | The route planner is framed as a small, inspectable planning algorithm. |
| [PathPlanning](https://github.com/zhm-real/PathPlanning) | A*, D*, RRT, and related planners | The next algorithm upgrade is an A*/Dijkstra comparison over the same mine map. |
| [python_motion_planning](https://github.com/ai-winter/python_motion_planning) | AGV/AMR planning and tracking | The demo connects path planning to vehicle constraints. |
| [EVRPTW-PR-ALNS](https://github.com/wornSweater/EVRPTW-PR-ALNS) | Electric-vehicle routing with partial charging | The report uses charging and reserve constraints as the central feasibility question. |
| [evrp-python](https://github.com/NeiH4207/evrp-python) | Compact EV routing problem implementation | The demo borrows the EV routing vocabulary without claiming production dispatch coverage. |
| [Google OR-Tools routing](https://developers.google.com/optimization/routing) | Vehicle routing optimisation vocabulary | The next-step discussion can mention richer constraints such as time windows and charging decisions. |

Current evidence:

- `haul-truck-planner/docs/algorithm-comparison.md` explains shortest path vs Dijkstra vs A*.
- `haul-truck-planner/reports/algorithm-comparison.md` reports feasibility, energy margin, expanded states, charging use, and risk-cell avoidance.
- Add richer EV routing constraints such as charge time, queueing, payload mass, and route windows.
- Keep the mining context explicit: this is not a production haul-road optimizer or fleet dispatcher.

## Public Boundary

- No private Canvas, SONIA, CV, transcript, WAM, mailbox, or application-form data belongs in this public repository.
- The demos use synthetic fixtures and local reports.
- External references are learning and positioning references, not dependencies or copied implementations.
