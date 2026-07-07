# AegisOps Triage Queue

This report ranks synthetic incidents before remediation so the reviewer can inspect severity, evidence, ownership, and next action before any patch preview.

| rank | scenario | severity | category | priority_score | owner | next_action | evidence |
| ---: | --- | --- | --- | ---: | --- | --- | --- |
| 1 | S7 | high | security | 133 | platform/security reviewer | Review securityContext patch, then run security dry-run validation. | `security:S7:root-container` |
| 2 | S4 | high | kubernetes | 128 | platform reviewer | Review invalid_app_mode_env, then run Kubernetes dry-run validation. | `k8s:S4:invalid-env` |
| 3 | S6 | high | kubernetes | 125 | platform reviewer | Review image_tag_mismatch, then run Kubernetes dry-run validation. | `k8s:S6:image-tag` |
| 4 | S2 | high | docker | 116 | platform reviewer | Review image dependency evidence, then run Docker dry-run validation. | `docker:S2:missing-module` |
| 5 | S1 | high | pytest | 114 | application reviewer | Review application patch and run pytest validation. | `pytest:S1:assertion` |
| 6 | S8 | medium | latency | 89 | application performance reviewer | Review latency evidence, then run benchmark dry-run validation. | `latency:S8:nested-loop` |
| 7 | S5 | medium | kubernetes | 86 | platform reviewer | Review wrong_readiness_probe_path, then run Kubernetes dry-run validation. | `k8s:S5:probe-404` |
| 8 | S3 | medium | ci | 78 | devex reviewer | Review CI environment variables, then run CI dry-run validation. | `gha:S3:empty-env` |

## Boundary

Human review remains required before patching or deployment.
The queue uses synthetic fixtures and deterministic scoring; it is not an incident-management system.
