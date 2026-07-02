# AegisOps Demo Script

## 90-Second Pitch

My background is Electrical Engineering, but I am focusing on AI software engineering and platform automation. AegisOps Agent is my portfolio project for that direction.

The project demonstrates an AI-assisted DevOps remediation loop. Given a reproducible CI/CD, Docker, Kubernetes, security, or latency failure, it collects evidence, retrieves relevant runbooks, diagnoses the root cause, generates a guarded patch preview, runs validation, and exports metrics. I compare single-agent and multi-agent modes on the same scenarios so the architecture choice is measurable rather than just a preference.

This maps directly to Accenture's ESIPS themes: SDLC agents, Kubernetes DevOps automation, agent memory, sustainable GenAI metrics, and single-vs-multi-agent evaluation.

## 5-Minute Demo Flow

## 1. Show The Problem

```bash
make scenario SCENARIO=S4
cat reports/S4/raw_failure.log
```

Explain:

- The pod is in `CrashLoopBackOff`.
- The app log points to an invalid `APP_MODE`.
- The goal is not only to name the issue, but to produce a safe patch preview and validate it.

## 2. Run The Multi-Agent Demo

```bash
make demo SCENARIO=S4 MODE=multi
```

Open:

```text
reports/S4/multi/diagnosis.json
reports/S4/multi/patch.diff
reports/S4/multi/validation.log
reports/S4/multi/metrics.json
reports/S4/multi/pr-summary.md
reports/S4/multi/pr-summary.md
```

Narration:

1. Evidence collection turns raw logs and scenario metadata into structured input.
2. Retrieval pulls the closest runbook context.
3. The agent workflow diagnoses `invalid_app_mode_env`.
4. The patch guard only allows changes to the scenario's approved deployment file.
5. Validation checks the patched output before the workflow is considered successful.
6. The PR summary converts the run into a concise handoff for human review.
6. The PR summary converts the run into a concise handoff for human review.

## 3. Explain The Guardrails

Show that the scenario only allows:

```text
k8s/overlays/broken-env/deployment.yaml
```

Then mention that CI workflows, gold labels, and tests are blocked. This keeps the demo honest: the agent cannot "fix" the benchmark by modifying tests or evaluation labels.

## 4. Compare Architectures

```bash
make eval-mock
cat reports/eval-summary.md
```

Explain the trade-off:

- Single-agent mode is cheaper and simpler.
- Multi-agent mode adds explicit triage, RCA, fix, and review stages.
- The value is auditability and role separation, but the cost is more orchestration and tool calls.

## 5. Close With The ESIPS Link

Close with:

> This is why I am interested in Accenture's SDLC agents and Kubernetes DevOps briefs. I want to work on AI systems that sit inside real engineering workflows, with validation, cost awareness, and human review rather than one-off model output.

## If Asked For More Detail

- For Kubernetes config generation, show `/Users/hanzhengyu/Documents/industry/kube-copilot`.
- For memory, cost, energy proxy, and single-vs-multi-agent research, show `/Users/hanzhengyu/Documents/industry/accenture-agent-research-lab`.
- For Accenture mapping, show `docs/esips-accenture-mapping.md`.
