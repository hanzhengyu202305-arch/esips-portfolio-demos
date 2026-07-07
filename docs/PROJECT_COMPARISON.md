# Project Comparison

This file explains why the portfolio is one coherent product story rather than three isolated projects.

## Comparison Matrix

| dimension | AegisOps Agent | Kube Copilot | Haul Truck Planner | EvidenceOps Scorecard |
| --- | --- | --- | --- | --- |
| role | main evidence line | DevOps/platform support | EE/mining support | evidence quality layer |
| core question | Can an agentic workflow turn an incident into reviewable engineering evidence? | Can generated infrastructure be checked before trust? | Can route planning include energy and risk constraints? | Is the public evidence complete and reviewable? |
| primary output | issue-to-PR report and diagnosis | policy and risk reports | route and algorithm reports | scorecard and release gate reports |
| validation style | tests, acceptance gates, scenario metrics | deterministic policy checks | algorithm comparison and feasibility metrics | artifact inventory, quality scoring, and release/share gate |
| reviewer takeaway | strongest fit for AI software engineering and SDLC agent work | shows infrastructure trust boundaries | keeps EE and industrial systems visible | proves the portfolio is auditable |

## Why AegisOps Is The Main Line

AegisOps has the strongest match to the portfolio thesis because it combines:

- AI agent workflow design.
- Software delivery lifecycle thinking.
- DevOps incident evidence.
- Root-cause analysis.
- Patch preview.
- Validation and report generation.

Kube Copilot and Haul Truck Planner are still useful, but they support the main story from different technical angles. Kube Copilot adds infrastructure validation. Haul Truck Planner adds constrained planning and EE/mining language.

## External Reference Fit

| reference family | mature ecosystem pattern | portfolio use |
| --- | --- | --- |
| SWE-agent, OpenHands, LangGraph, SWE-bench | issue-to-patch and agentic software-engineering workflows | AegisOps uses a smaller local issue-to-evidence-to-validation path |
| kube-linter, kubeconform, kube-score, Polaris, Kyverno, Gatekeeper | Kubernetes validation, policy, and admission-control thinking | Kube Copilot implements deterministic pre-deployment checks |
| PythonRobotics, PathPlanning, EV routing examples, OR-Tools routing | path planning and constrained vehicle routing language | Haul Truck Planner compares energy-aware route choices on a small map |
| OpenSSF Scorecard, SLSA, OpenTelemetry, SRE monitoring | evidence, quality gates, and operational signal vocabulary | EvidenceOps checks public portfolio artifacts, reviewer readiness, and release/share gating |

## What Not To Overclaim

- AegisOps is not equivalent to a full autonomous software-engineering platform.
- Kube Copilot is not a production scanner or admission controller.
- Haul Truck Planner is not a full mine fleet dispatch optimiser.
- EvidenceOps is not a formal compliance tool or application approval system.
