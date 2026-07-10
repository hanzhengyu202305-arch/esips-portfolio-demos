# Changelog

## v1.4 Adversarial Hardening

- Removed AegisOps gold-label leakage by deriving diagnoses from observed evidence and runbook context.
- Added `ESCALATE` behavior for missing or conflicting evidence so unsafe remediation stops before patch generation.
- Replaced Kube Copilot string matching with structural multi-document and multi-container YAML validation.
- Made Haul Truck Planner energy assumptions explicit and added map, battery, and model invariant checks.
- Added a 12-case cross-project adversarial review gate and required it in portfolio validation.
- Renamed the EvidenceOps score to evidence completeness and added structured JSON integrity checks.

## v1.3 Reviewer Evidence Pack

- Added a top-level `make demo-all` command that regenerates the public demo evidence and writes a reviewer output index.
- Added reviewer-facing traceability docs: claim trace, architecture, comparison, risk register, and roadmap.
- Strengthened the public repo as one coherent portfolio narrative: AI software engineering with validation.
- Kept private application material outside the public repository boundary.

## v1.2 EvidenceOps Quality Gate

- Added EvidenceOps Scorecard as a public evidence quality layer.
- Added PASS/WEAK/MISSING evidence labels and a quality score.
- Added generated submission-readiness and evidence-scorecard reports.
- Added portfolio-level checks that refresh `PORTFOLIO_STATUS.md` and `PORTFOLIO_STATUS.json`.

## v1.1 Three-Line Portfolio Snapshot

- Consolidated AegisOps Agent, Kube Copilot, and Haul Truck Planner into one ESIPS-style portfolio repository.
- Added public references and three-line application framing.
- Added reviewer fast path and executive overview docs.

## v1.0 Initial Public Demo Set

- Added deterministic local demos for SDLC agent remediation, Kubernetes validation, and electric haul route planning.
- Added generated reports for each demo line.
- Added basic tests for the three public projects.
