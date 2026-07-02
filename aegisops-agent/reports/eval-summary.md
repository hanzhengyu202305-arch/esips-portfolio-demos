# AegisOps Evaluation Summary

| mode | diagnosis_accuracy | fix_success_rate | avg_latency_seconds | estimated_cost_usd | tool_calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| multi | 1.00 | 1.00 | 0.409 | 0.002608 | 80 |
| single | 1.00 | 1.00 | 0.405 | 0.001720 | 48 |

## Per-Scenario Results

| scenario | mode | root_cause_id | root_cause_correct | fix_successful | latency_seconds | estimated_cost_usd |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| S1 | multi | wrong_discount_logic | true | true | 0.401 | 0.000325 |
| S1 | single | wrong_discount_logic | true | true | 0.397 | 0.000214 |
| S2 | multi | missing_python_dependency | true | true | 0.405 | 0.000329 |
| S2 | single | missing_python_dependency | true | true | 0.386 | 0.000218 |
| S3 | multi | missing_app_mode_env | true | true | 0.405 | 0.000327 |
| S3 | single | missing_app_mode_env | true | true | 0.407 | 0.000216 |
| S4 | multi | invalid_app_mode_env | true | true | 0.404 | 0.000328 |
| S4 | single | invalid_app_mode_env | true | true | 0.401 | 0.000217 |
| S5 | multi | wrong_readiness_probe_path | true | true | 0.398 | 0.000326 |
| S5 | single | wrong_readiness_probe_path | true | true | 0.404 | 0.000215 |
| S6 | multi | image_tag_mismatch | true | true | 0.426 | 0.000324 |
| S6 | single | image_tag_mismatch | true | true | 0.407 | 0.000213 |
| S7 | multi | container_runs_as_root | true | true | 0.426 | 0.000324 |
| S7 | single | container_runs_as_root | true | true | 0.427 | 0.000213 |
| S8 | multi | nested_loop_latency_regression | true | true | 0.409 | 0.000325 |
| S8 | single | nested_loop_latency_regression | true | true | 0.411 | 0.000214 |

## Architecture Comparison

Single-agent mode is the cheaper baseline. Multi-agent mode uses the same tools but adds explicit triage, RCA, fix, and review stages for auditability.

## Metrics

- `diagnosis_accuracy`: fraction of runs where `root_cause_id` matched the gold label.
- `fix_success_rate`: fraction of runs with a safe patch preview and passing validation.
- `estimated_cost_usd`: deterministic proxy using MockLLM token estimates.
- `tool_calls`: comparable proxy for orchestration complexity.
