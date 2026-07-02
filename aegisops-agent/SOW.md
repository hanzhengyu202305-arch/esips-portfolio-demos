# AegisOps Agent Statement of Work

Date: 2026-05-31

Project: `AegisOps Agent`

Target: ESIPS / Accenture AI software placement preparation, led by `Accenture_02 SDLC_Agents.pdf` with secondary fit to `Accenture_01 Kubernetes_DevOps.pdf`.

## 1. Purpose

AegisOps Agent demonstrates an AI-assisted DevOps remediation loop for reproducible CI/CD, Docker, Kubernetes, security, and latency incidents: collect evidence, retrieve runbook context, diagnose root cause, generate a guarded patch preview, validate the fix, and report metrics.

Success is measured by:

- Diagnosis accuracy >= 0.90 across the scenario suite.
- Fix success rate >= 0.85 with validation logs present.
- Per-scenario mock-agent estimated cost <= USD 0.001.
- Average local mock latency <= 1.0 second per run.
- A reviewer can reproduce the core demo with `make demo SCENARIO=S4 MODE=multi` and refresh score evidence with `make acceptance`.

Current local evidence from `reports/final-portfolio-report.md`: diagnosis accuracy `1.00`, fix success rate `1.00`, 8 scenarios, 16 evaluated single/multi runs.

## 2. Scope

Included:

- 8 deterministic failure scenarios across application logic, dependency, CI/CD, Docker, Kubernetes, container security, and latency regression cases.
- Evidence collection, Markdown runbook retrieval, single-agent and multi-agent RCA workflows, patch safety guardrails, validation, and final reporting.
- FastAPI demo service, Makefile command surface, GitHub Actions workflows, Kubernetes manifests, application pack, demo script, Data Card, and operations manual.

Excluded:

- Production auto-merge or live cluster mutation.
- Real customer, Accenture, broker, university, or employer data.
- Real secrets, live cloud credentials, or proprietary runbooks.
- Agent edits to CI workflows, tests, gold labels, or evaluation fixtures.

Dependencies:

- Python 3.11+, `pytest`, `fastapi`, and `uvicorn`.
- Optional local tooling for extended checks: Docker, `kubectl`, and kind.
- Local ESIPS brief files under `/Users/hanzhengyu/Documents/industry/S2_2026_June_December` for positioning only.

## 3. Timeboxed Plan

This SOW uses a 12-week scoring plan even though the current local MVP is already runnable.

| milestone | outcome | evidence |
| --- | --- | --- |
| Wk 2 | Requirements freeze and architecture review | `SPEC.md`, `SOW.md`, `docs/architecture.md`, `docs/esips-accenture-mapping.md` |
| Wk 4 | PoC metrics achieved | `make demo SCENARIO=S4 MODE=multi`, `reports/S4/multi/*`, `reports/eval-summary.md` |
| Wk 8 | Beta readiness | `make acceptance`, `.github/workflows/ci.yml`, `.github/workflows/eval-mock.yml`, `k8s/`, `DATACARD.md`, `OPERATIONS.md` |
| Wk 12 | Final demo and scoring | `docs/demo-script.md`, `docs/application-pack.md`, `reports/final-portfolio-report.md`, signed rubric with commit SHA |

## 4. Deliverables, Acceptance, And Weighting

| item | deliverable | pass/fail acceptance | evidence path | weight |
| --- | --- | --- | --- | ---: |
| 1 | Code repository and branch strategy | GitHub repo is published; `main` is protected; PR template exists; submitted score sheet references one commit SHA. | `.github/pull_request_template.md`, `README.md` | 10% |
| 2 | CI/CD automation | Pull requests run lint/test; evaluation workflow can refresh benchmark evidence; failed checks block merge once GitHub branch protection is enabled. | `.github/workflows/ci.yml`, `.github/workflows/eval-mock.yml` | 10% |
| 3 | Kubernetes deployment manifests | Kubernetes service and deployment manifests exist and pass the project dry-run validation path. | `k8s/base/`, `scripts/devops_check.py` | 8% |
| 4 | Reproducible PoC script | New reviewer can run setup, demo, evaluation, and report commands from README without API keys. | `Makefile`, `README.md` | 8% |
| 5 | Automated tests | Unit and integration tests pass locally and in CI; key acceptance path is tested. | `tests/`, `apps/demo-api/tests/` | 10% |
| 6 | Data Card and data compliance | Data sources are synthetic or generated; no secrets or real user data; limits and field dictionary documented. | `DATACARD.md`, `reports/*/scenario.json` | 7% |
| 7 | Metrics and thresholds | Diagnosis accuracy, fix success, latency, cost, and tool-call metrics are defined and meet threshold. | `reports/eval-summary.md`, `reports/eval-results.json` | 15% |
| 8 | Security and compliance basics | Patch guard blocks tests, CI workflows, and gold labels; container security scenario exists; secrets remain absent from examples. | `agent/acceptance.py`, `agent/tools/security_tools.py`, `reports/S7/` | 7% |
| 9 | Operations and observability | Health/metrics endpoints and operating procedures exist; scenario reports expose validation status and failure evidence. | `OPERATIONS.md`, `apps/demo-api/app/main.py`, `reports/doctor.md` | 5% |
| 10 | User documentation and runbook | Beginner and reviewer documentation allow one-day onboarding. | `docs/NEWCOMER_GUIDE.zh-CN.md`, `docs/runbooks/`, `README.md` | 5% |
| 11 | Final demo | 5-minute demo script and generated report cover problem, workflow, metrics, and Q&A evidence. | `docs/demo-script.md`, `reports/final-portfolio-report.md` | 10% |
| 12 | Mentor rubric | Rubric can be scored against evidence paths and tied to a commit SHA. | this file, `reports/acceptance-checklist.md` | 5% |

Total: 100%.

Critical fail gates: metrics threshold, CI/CD evidence, PoC reproducibility, and data compliance. Any critical gate failing should fail the overall submission even if the weighted score is otherwise high. For PoC scoring, run `make poc RUNS=3` and review `reports/scorecard.txt` plus `reports/reproducibility_report.json`.

## 5. Risks And Mitigations

| risk | mitigation |
| --- | --- |
| Scope grows into a full production DevOps platform | Keep MVP scenario-based; no live auto-merge or real cluster mutation in the scored version. |
| Reviewer cannot reproduce the result | Use `MockLLM`, deterministic fixtures, Makefile commands, and `make acceptance`. |
| Metrics look inflated because scenarios are synthetic | State the synthetic boundary clearly in `DATACARD.md`; evaluate single and multi modes on identical scenarios. |
| Unsafe patch behavior | Enforce allowed-file patch targets and block CI, tests, and gold labels. |
| Kubernetes tooling is unavailable on a review machine | Keep the main demo local; make Docker/kind optional and record availability in `reports/doctor.md`. |

## 6. Resources And Roles

Minimum resources:

- Local Python environment.
- Optional Docker/kind for extended Kubernetes checks.
- GitHub repository with branch protection before formal submission.

Suggested roles for reviewer framing:

- Technical lead: scope, architecture, and SOW ownership.
- Dev/MLOps: agent workflow, CI/CD, Kubernetes, and Makefile automation.
- QA: scenario matrix, test coverage, validation, and acceptance gate.
- Mentor/industry reviewer: final rubric score and commit-SHA sign-off.

## Rubric

| module | pass/fail standard | scoring focus | weight | score |
| --- | --- | --- | ---: | --- |
| Repository and branch strategy | Protected branch, PR template, commit SHA | Traceability and review hygiene | 10% |  |
| CI/CD | Main/PR checks and eval workflow | Build/test/evaluation loop | 10% |  |
| Kubernetes manifests | Deployable manifests and dry-run path | Resource shape and config separation | 8% |  |
| PoC script | Reproduces in <= 60 minutes | Minimal manual steps | 8% |  |
| Test suite | Key tests and acceptance gate pass | Critical path coverage | 10% |  |
| Data and Data Card | Legal synthetic data and documented limits | Compliance and field clarity | 7% |  |
| Metrics matrix | Thresholds met | Accuracy, fix, latency, cost | 15% |  |
| Security and compliance | Guardrails and no secrets | Unsafe edit prevention | 7% |  |
| Observability and operations | Health/metrics and doctor report | Run and diagnose readiness | 5% |  |
| Documentation | New reviewer can onboard in one day | README, runbooks, operations | 5% |  |
| Final Demo | Script and evidence match repo | Narrative, stability, metrics | 10% |  |
| Mentor rubric | Complete with commit SHA | Traceable scoring | 5% |  |
| Total | Critical gates pass |  | 100% |  |
