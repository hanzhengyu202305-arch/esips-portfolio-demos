# ESIPS Portfolio Demos

This repository contains three small, reproducible portfolio demos for ESIPS-style industry placement interviews.

The theme is AI/software engineering with validation: use agents or automation to generate recommendations, infrastructure, or routes, then make the result reviewable through tests, reports, and explicit boundaries.

## Three Lines

| line | target brief | local project | evidence |
| --- | --- | --- | --- |
| Agentic SDLC remediation | `Accenture_02 SDLC_Agents.pdf` | `aegisops-agent` | `aegisops-agent/reports/final-portfolio-report.md` |
| Kubernetes DevOps validation | `Accenture_01 Kubernetes_DevOps.pdf` | `kube-copilot` | `kube-copilot/reports/risk-comparison.md` |
| Electric haul truck trajectory planning | `RTSIH - Opt-OO - Trajectory planning for electric haul trucks.pdf` | `haul-truck-planner` | `haul-truck-planner/reports/route-experiment.md` |

Read `BEGINNER_GUIDE.zh-CN.md` first if you are new to the workspace, then read `THREE_LINE_ESIPS_PLAN.md` for the short application and interview framing.

For public open-source references behind the three demo lines, read `REFERENCES.md`.

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
