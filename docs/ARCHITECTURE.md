# Architecture

The repository uses one product story across four local components:

```text
industry brief -> scoped demo -> tests -> generated reports -> evidence scorecard -> reviewer package
```

## System View

```mermaid
flowchart TD
  Brief["Industry brief"] --> Scope["Scoped portfolio demo"]
  Scope --> Aegis["AegisOps Agent"]
  Scope --> Kube["Kube Copilot"]
  Scope --> Haul["Haul Truck Planner"]
  Aegis --> Reports["Generated public reports"]
  Kube --> Reports
  Haul --> Reports
  Reports --> Evidence["EvidenceOps Scorecard"]
  Evidence --> Reviewer["Reviewer evidence package"]
  Current["Current official source"] --> Manual["Manual confirmation before submission"]
  Manual --> Reviewer
```

## Components

| component | input | processing | output | trust boundary |
| --- | --- | --- | --- | --- |
| AegisOps Agent | synthetic incident fixture and runbook context | evidence collection, retrieval, RCA, patch preview, validation | PR-style report, diagnosis, metrics | human review before any real change |
| Kube Copilot | structured app requirements and manifest fixtures | deterministic policy checks for image tags, resources, probes, and security context | risk comparison and policy matrix | validation and review before deployment |
| Haul Truck Planner | small mine-map graph with battery, grade, charging, and risk attributes | shortest path, battery-state Dijkstra, and A* comparison | route experiment and algorithm comparison | simplified planning evidence only |
| EvidenceOps Scorecard | public reports and claim files | evidence inventory, quality scoring, PASS/WEAK/MISSING labels | evidence scorecard and submission-readiness report | public evidence check only |
| Reviewer package | generated reports and summary docs | claim tracing and guided reading order | fast-path docs and demo index | does not replace current official checks |

## Data Flow

```mermaid
sequenceDiagram
  participant Reviewer
  participant Make as make demo-all
  participant Demos as Local demos
  participant Reports as Reports
  participant Scorecard as EvidenceOps

  Reviewer->>Make: run public demo path
  Make->>Demos: regenerate AegisOps, Kube, Haul, EvidenceOps outputs
  Demos->>Reports: write markdown and JSON evidence
  Reports->>Scorecard: score public evidence coverage
  Scorecard->>Reviewer: produce reviewer index and status artifacts
```

## Why This Architecture Works

- It keeps the strongest project, AegisOps Agent, as the main SDLC evidence.
- It uses Kube Copilot and Haul Truck Planner as supporting engineering proof, not disconnected side projects.
- It separates evidence generation from application submission, so public artifacts stay reviewable and bounded.
- It makes the reviewer path command-driven: `make demo-all`, then `make portfolio-check`.

