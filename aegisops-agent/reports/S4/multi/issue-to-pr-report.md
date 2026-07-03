# S4 Issue-To-PR Report

## Source Issue Fixture

# Issue: Kubernetes deployment CrashLoopBackOff after config change

## Symptoms

- Pod enters CrashLoopBackOff.
- CI deploy validation fails for the Kubernetes overlay.
- Logs show invalid APP_MODE for the demo service.

## Expected

The service starts with a supported `APP_MODE` value and the deployment passes validation.

## Observed

The container exits during startup because the environment configuration is not accepted by the application.

## Candidate Evidence

- `reports/S4/evidence.json`
- `k8s/overlays/broken-env/deployment.yaml`
- `reports/S4/raw_failure.log`
- `reports/S4/multi/validation.log`

## Workflow Evidence

| step | artifact | reviewer check |
| --- | --- | --- |
| issue / failing symptom | `fixtures/issues/S4_crashloopbackoff_issue.md` | GitHub-style issue fixture describes expected and observed behavior. |
| evidence collection | `reports/S4/evidence.json` | Failure evidence is structured before diagnosis. |
| runbook retrieval | `reports/S4/multi/diagnosis.json` | Retrieved context includes Kubernetes CrashLoopBackOff runbooks. |
| root-cause diagnosis | `reports/S4/multi/diagnosis.json` | Expected root cause is `invalid_app_mode_env`. |
| guarded patch preview | `reports/S4/multi/patch.diff` | Patch changes only the scenario allowlisted deployment file. |
| validation | `reports/S4/multi/validation.log` | Tests, lint, and DevOps dry-run validation are recorded. |
| PR summary | `reports/S4/multi/pr-summary.md` | Human reviewer gets incident, root cause, files changed, validation, and risk notes. |

## Expected Root Cause

`invalid_app_mode_env`

## Boundary

This report does not create a real pull request and does not require a GitHub token or live cluster. It is a deterministic portfolio artifact that shows how the AegisOps workflow can turn a failure issue into a human-reviewable patch preview.
