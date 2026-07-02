# AegisOps Agent Operations Manual

## Operating Boundary

AegisOps is a local portfolio demo, not a production remediation bot. The default workflow produces patch previews and validation artifacts for human review. It must not auto-merge pull requests, mutate a live Kubernetes cluster, or use real secrets.

## Environment Setup

Requirements:

- Python 3.11+
- `pip`
- Optional: Docker, `kubectl`, and kind for extended DevOps checks

Setup:

```bash
make setup
```

Quick health check:

```bash
make doctor
make test
```

The doctor report is written to:

```text
reports/doctor.md
reports/doctor.json
```

## Core Demo Runbook

Run the recommended Accenture/ESIPS demo:

```bash
make demo SCENARIO=S4 MODE=multi
```

Inspect:

```text
reports/S4/multi/diagnosis.json
reports/S4/multi/patch.diff
reports/S4/multi/validation.log
reports/S4/multi/metrics.json
reports/S4/multi/pr-summary.md
```

Refresh the complete reviewer packet:

```bash
make acceptance
```

## Evaluation Runbook

Run the deterministic single-agent versus multi-agent benchmark:

```bash
make eval-mock
```

Inspect:

```text
reports/eval-summary.md
reports/eval-results.json
```

Pass thresholds for SOW scoring:

- Diagnosis accuracy >= 0.90.
- Fix success rate >= 0.85.
- Average mock latency <= 1.0 second per run.
- Per-scenario mock estimated cost <= USD 0.001.

## Local Service Runbook

Start the demo API:

```bash
make serve-app
```

Useful endpoints:

```text
GET /health
GET /metrics
POST /predict
GET /orders/{id}
```

If `make serve-app` fails, confirm dependencies were installed with `make setup` and that port `8000` is free.

## CI/CD Runbook

Local CI equivalent:

```bash
make test
make lint
make eval-mock
```

GitHub workflows:

- `.github/workflows/ci.yml`: install, test, lint.
- `.github/workflows/eval-mock.yml`: refresh deterministic evaluation evidence.

Before formal submission, publish the repository to GitHub and enable branch protection on `main` so failed checks block merges.

## Kubernetes And DevOps Checks

Static Kubernetes artifacts:

```text
k8s/base/deployment.yaml
k8s/base/service.yaml
```

Run the project DevOps check:

```bash
make docker-build
make kind-setup
```

Docker and kind are optional for the core reviewer demo. If unavailable, `reports/doctor.md` records that limitation while the mock workflow remains runnable.

## Troubleshooting

| symptom | likely cause | action |
| --- | --- | --- |
| `ModuleNotFoundError` | package not installed | run `make setup` from the repository root |
| test failure in demo API | app dependency or path issue | run `make test-app` and inspect the failing test |
| missing `reports/S4/multi/*` | demo has not been run | run `make demo SCENARIO=S4 MODE=multi` |
| acceptance fails on final report | reports are stale | run `make acceptance` again |
| Docker/kind unavailable | optional local tooling missing | keep core demo local and note the doctor report status |

## Release Checklist

Before sharing with a mentor, ESIPS reviewer, or interviewer:

1. Run `make acceptance`.
2. Confirm `reports/acceptance-checklist.md` says `Overall status: PASS`.
3. Open `SOW.md` and confirm scoring thresholds match the current report.
4. Open `DATACARD.md` and confirm no real or sensitive data was introduced.
5. Open `reports/final-portfolio-report.md` and rehearse the demo path.
6. If publishing to GitHub, verify branch protection and record the final commit SHA in the rubric.
