# AegisOps Agent Final Portfolio Report

AegisOps Agent is a reproducible agentic DevOps lab for root-cause analysis and patch remediation across CI/CD, Docker, Kubernetes, security, and latency incidents.

## Portfolio Positioning

This project is built for AI/software industry-placement interviews where the goal is to show more than a standalone chatbot. AegisOps puts an LLM-style agent inside a controlled engineering workflow: evidence collection, runbook retrieval, root-cause analysis, patch preview generation, validation, and metric reporting.

Primary ESIPS fit: `Accenture_02 SDLC_Agents.pdf`.

Secondary ESIPS fit: `Accenture_01 Kubernetes_DevOps.pdf`, `Accenture_03 AgentMemory.pdf`, `Accenture_04 SustainableGenAI.pdf`, and `Accenture_05 SingleVMultiAgent.pdf`.

## Demo Path

```bash
make test
make demo SCENARIO=S4 MODE=multi
make eval-mock
make report
```

Key demo artifacts:

- `reports/S4/multi/demo-report.md`
- `reports/S4/multi/issue-to-pr-report.md`
- `reports/S4/multi/pr-summary.md`
- `reports/S4/multi/patch-risk-diff.md`
- `reports/S4/multi/patch.diff`
- `reports/S4/multi/validation.log`
- `reports/eval-summary.md`

## AegisOps Evaluation Summary

| mode | diagnosis_accuracy | fix_success_rate | avg_latency_seconds | estimated_cost_usd | tool_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| multi | 1.00 | 1.00 | 0.395 | 0.002608 | 80 |
| single | 1.00 | 1.00 | 0.345 | 0.001720 | 48 |

### Per-Scenario Results

| scenario | mode | root_cause_id | root_cause_correct | fix_successful | latency_seconds | estimated_cost_usd |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| S1 | multi | wrong_discount_logic | true | true | 0.360 | 0.000325 |
| S1 | single | wrong_discount_logic | true | true | 0.310 | 0.000214 |
| S2 | multi | missing_python_dependency | true | true | 0.370 | 0.000329 |
| S2 | single | missing_python_dependency | true | true | 0.320 | 0.000218 |
| S3 | multi | missing_app_mode_env | true | true | 0.380 | 0.000327 |
| S3 | single | missing_app_mode_env | true | true | 0.330 | 0.000216 |
| S4 | multi | invalid_app_mode_env | true | true | 0.390 | 0.000328 |
| S4 | single | invalid_app_mode_env | true | true | 0.340 | 0.000217 |
| S5 | multi | wrong_readiness_probe_path | true | true | 0.400 | 0.000326 |
| S5 | single | wrong_readiness_probe_path | true | true | 0.350 | 0.000215 |
| S6 | multi | image_tag_mismatch | true | true | 0.410 | 0.000324 |
| S6 | single | image_tag_mismatch | true | true | 0.360 | 0.000213 |
| S7 | multi | container_runs_as_root | true | true | 0.420 | 0.000324 |
| S7 | single | container_runs_as_root | true | true | 0.370 | 0.000213 |
| S8 | multi | nested_loop_latency_regression | true | true | 0.430 | 0.000325 |
| S8 | single | nested_loop_latency_regression | true | true | 0.380 | 0.000214 |

### Architecture Comparison

Single-agent mode is the cheaper baseline. Multi-agent mode uses the same tools but adds explicit triage, RCA, fix, and review stages for auditability.

### Metrics

- `diagnosis_accuracy`: fraction of runs where `root_cause_id` matched the gold label.
- `fix_success_rate`: fraction of runs with a safe patch preview and passing validation.
- `estimated_cost_usd`: deterministic proxy using MockLLM token estimates.
- `tool_calls`: comparable proxy for orchestration complexity.

## Technical Differentiators

- Deterministic local demo: runs with `MockLLM`, so reviewers can reproduce it without API keys.
- Agentic workflow: evidence -> retrieval -> diagnosis -> patch preview -> validation -> metrics.
- Safety guardrails: the agent cannot patch CI workflows, tests, or gold labels.
- Architecture comparison: single-agent and multi-agent modes run against the same scenarios.
- Engineering metrics: accuracy, fix success, latency, cost proxy, tool calls, and ROI proxy are reported.

## ROI Proxy

| scenario | root_cause_id | manual_debug_minutes | human_review_minutes | estimated_cost_usd | net_value_usd |
| --- | --- | ---: | ---: | ---: | ---: |
| S1 | wrong_discount_logic | 18 | 5 | 0.000325 | 17.33 |
| S2 | missing_python_dependency | 20 | 6 | 0.000329 | 18.67 |
| S3 | missing_app_mode_env | 22 | 6 | 0.000327 | 21.33 |
| S4 | invalid_app_mode_env | 28 | 8 | 0.000328 | 26.67 |
| S5 | wrong_readiness_probe_path | 25 | 7 | 0.000326 | 24.00 |
| S6 | image_tag_mismatch | 24 | 7 | 0.000324 | 22.67 |
| S7 | container_runs_as_root | 30 | 9 | 0.000324 | 28.00 |
| S8 | nested_loop_latency_regression | 35 | 10 | 0.000325 | 33.33 |

## Deliverables

- GitHub-ready repository scaffold
- Incident triage queue with deterministic priority scoring
- FastAPI demo service
- 8 reproducible failure scenarios
- RAG runbooks and incident memory
- Single-agent and multi-agent workflows
- Patch safety guardrails
- Patch risk diff report before human review
- Deterministic MockLLM evaluation
- Accenture/ESIPS application narrative

## Supporting Artifacts

- Newcomer guide: `docs/NEWCOMER_GUIDE.zh-CN.md`
- Scenario matrix: `reports/scenario-matrix.md`
- Triage queue: `reports/triage-queue.md` (generated at `reports/triage-queue.md`)
- Evaluation summary: `reports/eval-summary.md`
- Demo script: `docs/demo-script.md`
- ESIPS mapping: `docs/esips-accenture-mapping.md`
- Application pack: `docs/application-pack.md`
- Acceptance checklist: `reports/acceptance-checklist.md`
- S4 issue-to-PR report: `reports/S4/multi/issue-to-pr-report.md`
