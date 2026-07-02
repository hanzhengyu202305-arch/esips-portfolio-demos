# AegisOps PoC Validation Guide

This guide turns the project into a reproducible PoC review packet. It maps the four validation dimensions from the PoC template onto the existing AegisOps scenario and evaluation system.

## Reviewer Command

Run the full PoC loop:

```bash
make poc RUNS=3
```

This refreshes:

```text
reports/eval-results.json
reports/eval-summary.md
reports/poc-metrics.json
reports/scorecard.txt
reports/reproducibility_report.json
```

For a quicker scorecard from existing evaluation output:

```bash
make scorecard
```

## Validation Dimensions

| dimension | AegisOps evidence | output |
| --- | --- | --- |
| Functional | scenario demo, patch preview, validation result, fix success rate | `reports/*/*/validation.log`, `reports/poc-metrics.json` |
| Performance | average local mock latency and tool calls | `reports/poc-metrics.json` |
| Quality | root-cause accuracy against gold labels | `reports/eval-results.json`, `reports/eval-summary.md` |
| Cost & Ops | estimated mock cost, doctor report, reproducibility variance | `reports/scorecard.txt`, `reports/doctor.md`, `reports/reproducibility_report.json` |

## Scorecard Thresholds

Thresholds and weights are explicit in:

```text
config/poc-scorecard.json
```

Default pass gates:

- Diagnosis accuracy >= 0.90.
- Fix success rate >= 0.85.
- Average latency <= 1.00 second.
- Max cost per run <= USD 0.001.
- Evaluated runs >= 16.

## Remote Review Flow

1. Run `make setup` once.
2. Run `make poc RUNS=3`.
3. Read `reports/scorecard.txt` for the score and pass/fail result.
4. Read `reports/reproducibility_report.json` for run-to-run stability.
5. Open `reports/S4/multi/pr-summary.md` and `reports/S4/multi/patch.diff` to inspect the human-review handoff.

## Boundary

The scorecard is a PoC validation surface, not a production SLO. It uses deterministic fixtures and `MockLLM` so an ESIPS mentor or interviewer can rerun the project without API keys, cloud credentials, or a live Kubernetes cluster.
