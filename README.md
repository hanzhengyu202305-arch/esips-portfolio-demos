# ESIPS Portfolio Demos

[![portfolio-check](https://github.com/hanzhengyu202305-arch/esips-portfolio-demos/actions/workflows/portfolio-check.yml/badge.svg)](https://github.com/hanzhengyu202305-arch/esips-portfolio-demos/actions/workflows/portfolio-check.yml)

This repository contains three small, reproducible portfolio demos for ESIPS-style industry placement interviews.

Portfolio thesis: **AI software engineering with validation: turning industry briefs into reproducible, testable, reviewable engineering demos.**

The three demos share the same product story: generate or plan something, validate it, report it, and keep the human-review boundary visible.

## Reviewer Fast Path

### ESIPS Mapping

| priority | ESIPS preference | project | reviewer takeaway |
| --- | --- | --- | --- |
| 1 | `Accenture_02 SDLC_Agents` | `aegisops-agent` | Main line: RAG/runbook retrieval -> root cause -> patch preview -> validation -> report |
| 2 | `Accenture_01 Kubernetes_DevOps` | `kube-copilot` | Kubernetes and CI/CD generation is useful only after policy validation and human review |
| 3 | `RTSIH electric haul truck trajectory planning` | `haul-truck-planner` | Battery reserve, grade, charging access, perception risk, and energy-aware planning matter more than shortest path alone |

### 3-Minute Read

1. Read this section for the thesis and three-line map.
2. Open [`docs/EXECUTIVE_ONE_PAGE.md`](docs/EXECUTIVE_ONE_PAGE.md) for the one-page overview.
3. Open [`THREE_LINE_ESIPS_PLAN.md`](THREE_LINE_ESIPS_PLAN.md) for the application framing.
4. Open [`docs/REVIEWER_GUIDE.md`](docs/REVIEWER_GUIDE.md) for the interview/reviewer script.

### 10-Minute Evidence Path

| demo | what to inspect | command | report |
| --- | --- | --- | --- |
| AegisOps Agent | SDLC agent RCA workflow | `make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13` | [`aegisops-agent/reports/S4/multi/demo-report.md`](aegisops-agent/reports/S4/multi/demo-report.md), [`aegisops-agent/reports/S4/multi/pr-summary.md`](aegisops-agent/reports/S4/multi/pr-summary.md) |
| Kube Copilot | Kubernetes validation boundary | `make -C kube-copilot report` | [`kube-copilot/reports/risk-comparison.md`](kube-copilot/reports/risk-comparison.md) |
| Haul Truck Planner | Energy-aware route planning | `make -C haul-truck-planner demo` | [`haul-truck-planner/reports/route-experiment.md`](haul-truck-planner/reports/route-experiment.md) |

### Full Validation

```bash
make test
make portfolio-check
```

`make portfolio-check` refreshes [`PORTFOLIO_STATUS.md`](PORTFOLIO_STATUS.md) and [`PORTFOLIO_STATUS.json`](PORTFOLIO_STATUS.json).

Boundary: this public repository uses synthetic/local fixtures only. It is not a production system, does not mutate real infrastructure, and must not include private application data, credentials, or personal academic documents.

For claim-by-claim boundaries, read [`CLAIMS_MATRIX.md`](CLAIMS_MATRIX.md).

## Three Lines

| line | target brief | local project | evidence |
| --- | --- | --- | --- |
| Agentic SDLC remediation | `Accenture_02 SDLC_Agents.pdf` | `aegisops-agent` | `aegisops-agent/reports/final-portfolio-report.md` |
| Kubernetes DevOps validation | `Accenture_01 Kubernetes_DevOps.pdf` | `kube-copilot` | `kube-copilot/reports/risk-comparison.md` |
| Electric haul truck trajectory planning | `RTSIH - Opt-OO - Trajectory planning for electric haul trucks.pdf` | `haul-truck-planner` | `haul-truck-planner/reports/route-experiment.md` |

Read `BEGINNER_GUIDE.zh-CN.md` first if you are new to the workspace, then read `THREE_LINE_ESIPS_PLAN.md` for the short application and interview framing.

For public open-source references behind the three demo lines, read `REFERENCES.md`.

For a single-page reviewer overview, read [`docs/EXECUTIVE_ONE_PAGE.md`](docs/EXECUTIVE_ONE_PAGE.md). For a concise reviewer command path, read [`docs/REVIEWER_FAST_PATH.md`](docs/REVIEWER_FAST_PATH.md). For a live presentation script, read [`docs/FIVE_MINUTE_DEMO_SCRIPT.md`](docs/FIVE_MINUTE_DEMO_SCRIPT.md). For source-backed external references, read [`docs/EXTERNAL_REFERENCE_MAP.md`](docs/EXTERNAL_REFERENCE_MAP.md).

## Visual Evidence

```text
Portfolio status: PASS
S4 AegisOps: issue -> evidence -> RCA -> patch preview -> validation -> PR summary
Kube Copilot: safe PASS / partial PARTIAL / risky FAIL with blocking-warning-review categories
Haul Truck Planner: shortest path infeasible; Dijkstra and A* feasible with charging lane
```

## Interview Fast Path

30-second pitch:

> My ESIPS portfolio is built around AI software engineering with validation. AegisOps Agent is the main SDLC agent demo: it turns a reproducible DevOps incident into evidence, root cause, guarded patch preview, validation, and a PR-style report. Kube Copilot and Haul Truck Planner support the same story from Kubernetes validation and EE/mining route-planning angles.

60-second pitch:

> The repository contains three local, reproducible demos. AegisOps Agent maps to Accenture SDLC Agents by showing an auditable RCA workflow for CI/CD, Docker, Kubernetes, security, and latency incidents. Kube Copilot maps to Accenture Kubernetes DevOps by showing that AI can draft infrastructure files, but policy validation and human review define trust. Haul Truck Planner maps to RTSIH by comparing shortest path against energy-aware routing under battery reserve, grade, charging access, and perception-risk constraints. The common claim is not production readiness; it is that I can turn industry briefs into testable engineering evidence with clear limitations.

One-line demo explanations:

- AegisOps: incident evidence -> runbook retrieval -> root cause -> patch preview -> validation -> report.
- Kube Copilot: generated Docker/Kubernetes/CI files are blocked until policy checks pass.
- Haul Truck Planner: feasible electric haul routes depend on battery state, charging, grade, and risk, not only distance.

Limitations:

- The incidents, manifests, and mine map are synthetic fixtures.
- Default demos use deterministic local logic and do not require paid cloud services or API keys.
- Human review remains required before any real deployment, infrastructure change, or engineering decision.

Likely reviewer questions:

- Why is AegisOps the main line rather than three equal projects?
- How do the validators prevent overtrusting generated output?
- What would be the next production-grade step for each demo?

## Quick Check

```bash
make test
```

This runs:

- AegisOps pytest suite with the configured Python interpreter.
- Kube Copilot unit tests.
- Haul Truck Planner unit tests.

If your Python paths differ, override them:

```bash
make test AEGISOPS_PY=/path/to/python3
```

## Project Summary

### AegisOps Agent

An agentic DevOps root-cause-analysis and remediation demo. It uses synthetic CI/CD, Docker, Kubernetes, security, and latency incidents to show a controlled workflow:

1. Collect evidence.
2. Retrieve runbook context.
3. Diagnose the root cause.
4. Generate a guarded patch preview.
5. Run validation.
6. Export auditable metrics and reports.

Useful commands:

```bash
make -C aegisops-agent test PYTHON=/opt/anaconda3/bin/python3.13
make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13
make -C aegisops-agent acceptance PYTHON=/opt/anaconda3/bin/python3.13
```

### Kube Copilot

A Kubernetes and CI/CD generation plus validation demo. It drafts Docker, Kubernetes, and GitHub Actions artifacts from structured requirements, then validates risky output such as `latest` image tags and missing resource limits.

Useful commands:

```bash
make -C kube-copilot test
make -C kube-copilot report
```

### Haul Truck Planner

An electric haul truck route-planning demo for mining operations. It compares geometric shortest paths with an energy-aware route that considers battery reserve, grade, charging access, and an ELEC5308-style perception risk layer.

Useful commands:

```bash
make -C haul-truck-planner test
make -C haul-truck-planner report
make -C haul-truck-planner demo
```

## Boundaries

- These are portfolio demos, not production systems.
- Data and incidents are synthetic or local fixtures.
- No real customer, employer, university, cloud, broker, or credential data is included.
- Generated Kubernetes manifests and patch previews require validation and human review.
- The ELEC5308-style route-planning language is used as technical inspiration, not as an official course submission.
