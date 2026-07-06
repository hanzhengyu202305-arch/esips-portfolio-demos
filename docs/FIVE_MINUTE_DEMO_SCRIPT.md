# Five-Minute Demo Script

Use this when presenting the portfolio live. Keep the demo focused on evidence, validation, and boundaries.

## 0:00-0:30 - Positioning

Say:

> My ESIPS portfolio is built around AI software engineering with validation. AegisOps is the main SDLC agent demo, Kube Copilot supports the Kubernetes DevOps line, Haul Truck Planner keeps the EE/mining route-planning angle visible, and EvidenceOps Scorecard checks whether the public evidence is present, strong enough, and bounded.

Open:

```text
README.md
docs/EXECUTIVE_ONE_PAGE.md
```

## 0:30-2:30 - AegisOps Main Demo

Run:

```bash
make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13
```

Open:

```text
aegisops-agent/reports/S4/multi/issue-to-pr-report.md
aegisops-agent/reports/S4/multi/pr-summary.md
```

Say:

> This starts from a CrashLoopBackOff-style issue fixture. The workflow collects evidence, retrieves runbook context, diagnoses `invalid_app_mode_env`, proposes an allowlisted patch preview, runs validation, and writes a PR-style summary.

## 2:30-3:30 - Kube Copilot

Run:

```bash
make -C kube-copilot report
```

Open:

```text
kube-copilot/reports/risk-comparison.md
kube-copilot/reports/policy-matrix.md
```

Say:

> This shows that AI-generated infrastructure is only a draft. The validator separates blocking issues, warnings, and manual-review items.

## 3:30-4:30 - Haul Truck Planner

Run:

```bash
make -C haul-truck-planner report
```

Open:

```text
haul-truck-planner/reports/algorithm-comparison.md
haul-truck-planner/reports/route-experiment.md
```

Say:

> The shortest path violates reserve. Battery-state Dijkstra and A* use the charging lane and avoid risk cells. This keeps the EE/mining-system story visible without claiming production dispatch.

## 4:30-4:50 - EvidenceOps Scorecard

Run:

```bash
make -C evidenceops-scorecard report
```

Open:

```text
evidenceops-scorecard/reports/evidence-scorecard.md
evidenceops-scorecard/reports/submission-readiness.md
```

Say:

> EvidenceOps is the evidence quality gate. It checks whether the reports, claims, status files, and manual-review boundaries are present, then labels evidence as PASS, WEAK, or MISSING and gives a quality score. This means the portfolio is not only a set of demos; it is a reviewable evidence package.

## 4:50-5:00 - Boundary

Say:

> These are local, synthetic, reproducible demos. The value is workflow design, validation, reporting, and clear limitations. I do not claim production automation, production Kubernetes enforcement, production mine dispatch, or official application approval.

Final command:

```bash
make portfolio-check
```
