# Public References And Roadmap

This repository is a portfolio demo set, not a fork or copy of the projects below. The references show the engineering ecosystems that informed the three demo lines: agentic SDLC remediation, Kubernetes validation, and electric haul-truck route planning.

## AegisOps Agent

Local demo: [`aegisops-agent`](aegisops-agent)

| reference | useful pattern | how this repo uses the idea |
| --- | --- | --- |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | GitHub issue to attempted code fix | A local CI/CD incident becomes evidence, RCA, patch preview, validation, and report. |
| [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | Compact agent loop | The demo keeps the workflow small enough to inspect in an interview. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Larger agentic software-engineering platform | AegisOps stays deterministic and local instead of claiming full autonomous development. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Graph-style agent workflows | The demo compares single-agent and multi-agent runs over fixed scenarios. |

Roadmap:

- Add a small issue-style fixture that starts from a failing CI log and produces a human-reviewable PR note.
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

Roadmap:

- Expand policy checks around security context, non-root execution, privileged containers, probes, resource requests, and image tags.
- Keep checks readable and deterministic rather than trying to replace production scanners.
- Add fixture manifests for safe, risky, and partially remediated cases.

## Haul Truck Planner

Local demo: [`haul-truck-planner`](haul-truck-planner)

| reference | useful pattern | how this repo uses the idea |
| --- | --- | --- |
| [PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics) | Robotics path-planning examples | The route planner is framed as a small, inspectable planning algorithm. |
| [PathPlanning](https://github.com/zhm-real/PathPlanning) | A*, D*, RRT, and related planners | The next algorithm upgrade is an A*/Dijkstra comparison over the same mine map. |
| [python_motion_planning](https://github.com/ai-winter/python_motion_planning) | AGV/AMR planning and tracking | The demo connects path planning to vehicle constraints. |
| [EVRPTW-PR-ALNS](https://github.com/wornSweater/EVRPTW-PR-ALNS) | Electric-vehicle routing with partial charging | The report uses charging and reserve constraints as the central feasibility question. |
| [evrp-python](https://github.com/NeiH4207/evrp-python) | Compact EV routing problem implementation | The demo borrows the EV routing vocabulary without claiming production dispatch coverage. |

Roadmap:

- Add A* as a second planner while keeping the current battery-state Dijkstra baseline.
- Add richer EV routing constraints such as charge time, queueing, payload mass, and route windows.
- Keep the mining context explicit: this is not a production haul-road optimizer or fleet dispatcher.

## Public Boundary

- No private Canvas, SONIA, CV, transcript, WAM, mailbox, or application-form data belongs in this public repository.
- The demos use synthetic fixtures and local reports.
- External references are learning and positioning references, not dependencies or copied implementations.
