# Incident To PR Walkthrough

This walkthrough shows the reviewer path for the S4 Kubernetes CrashLoopBackOff scenario.

The point is not to claim autonomous production repair. The point is to show an AI-assisted SDLC workflow where evidence, diagnosis, patch preview, validation, and reporting are all inspectable.

## External Anchors

This workflow is positioned near public agentic software-engineering references such as SWE-agent, SWE-bench, OpenHands, and LangGraph:

- issue or failure context becomes structured evidence;
- the system proposes a software action rather than only a chat answer;
- validation and review artifacts decide whether the action is trustworthy.

AegisOps is intentionally smaller. It uses deterministic local fixtures and does not create real pull requests, use a GitHub token, or mutate a live cluster.

## Command

```bash
make demo SCENARIO=S4 MODE=multi
```

If running from the repository root with the local configured interpreter:

```bash
make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13
```

## Expected Root Cause

```text
invalid_app_mode_env
```

S4 simulates a Kubernetes CrashLoopBackOff where `APP_MODE` is set to an unsupported value. The agent should diagnose the bad environment configuration and propose a patch only for the scenario allowlisted file.

## Evidence Chain

| step | artifact | reviewer check |
| --- | --- | --- |
| Incident / failing symptom | [`reports/S4/raw_failure.log`](../reports/S4/raw_failure.log) | The symptom is a reproducible CrashLoopBackOff-style failure. |
| Evidence collection | [`reports/S4/evidence.json`](../reports/S4/evidence.json) | Evidence is structured before diagnosis. |
| Runbook retrieval | [`reports/S4/multi/diagnosis.json`](../reports/S4/multi/diagnosis.json) | Retrieved context includes Kubernetes CrashLoopBackOff guidance. |
| Root-cause diagnosis | [`reports/S4/multi/diagnosis.json`](../reports/S4/multi/diagnosis.json) | Root cause is `invalid_app_mode_env` with confidence. |
| Guarded patch preview | [`reports/S4/multi/patch.diff`](../reports/S4/multi/patch.diff) | The patch changes only `k8s/overlays/broken-env/deployment.yaml`. |
| Validation log | [`reports/S4/multi/validation.log`](../reports/S4/multi/validation.log) | Tests, lint, and DevOps dry-run checks are recorded. |
| PR-style summary | [`reports/S4/multi/pr-summary.md`](../reports/S4/multi/pr-summary.md) | The result is written as a human-reviewable PR note. |
| Demo report | [`reports/S4/multi/demo-report.md`](../reports/S4/multi/demo-report.md) | Root-cause correctness, fix success, latency, cost, and tool calls are summarized. |

## Why The Patch Is Reviewable

AegisOps does not apply uncontrolled production changes. For each scenario, the proposed patch is checked against `allowed_files` before validation. S4 allows only:

```text
k8s/overlays/broken-env/deployment.yaml
```

The safety guard blocks patches to tests, gold labels, and CI workflows so the agent cannot fake success by editing the evaluator. The output remains a patch preview plus validation evidence for human review.

## Interview Explanation

Use this short version:

> S4 starts from a Kubernetes CrashLoopBackOff symptom. AegisOps collects evidence, retrieves the Kubernetes runbook context, diagnoses `invalid_app_mode_env`, proposes a patch only to the allowlisted deployment file, runs validation, and exports a PR-style summary. The important boundary is that this is a local deterministic demo with guarded patch preview, not a production cluster mutator.
