# AegisOps Patch Review Queue

This report ranks proposed patch reviews across synthetic scenarios so a reviewer can inspect blocking findings, review findings, ownership, and next action before merge.

| rank | scenario | status | owner | risk_score | blocking | review | pass | next_action | report |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | S7 | REVIEW | platform/security reviewer | 145 | 0 | 1 | 3 | Security reviewer checks hardening controls, then runs security dry-run validation. | [`reports/S7/multi/patch-risk-diff.md`](../reports/S7/multi/patch-risk-diff.md) |
| 2 | S4 | REVIEW | platform reviewer | 140 | 0 | 2 | 1 | Platform reviewer checks manifest risk, then runs Kubernetes dry-run validation. | [`reports/S4/multi/patch-risk-diff.md`](../reports/S4/multi/patch-risk-diff.md) |
| 3 | S5 | REVIEW | platform reviewer | 135 | 0 | 1 | 1 | Platform reviewer checks manifest risk, then runs Kubernetes dry-run validation. | [`reports/S5/multi/patch-risk-diff.md`](../reports/S5/multi/patch-risk-diff.md) |
| 4 | S6 | REVIEW | platform reviewer | 135 | 0 | 1 | 1 | Platform reviewer checks manifest risk, then runs Kubernetes dry-run validation. | [`reports/S6/multi/patch-risk-diff.md`](../reports/S6/multi/patch-risk-diff.md) |
| 5 | S8 | REVIEW | application performance reviewer | 130 | 0 | 2 | 1 | Performance reviewer checks algorithm change, then runs benchmark dry-run validation. | [`reports/S8/multi/patch-risk-diff.md`](../reports/S8/multi/patch-risk-diff.md) |
| 6 | S2 | REVIEW | platform reviewer | 115 | 0 | 1 | 1 | Platform reviewer checks image dependency change, then runs Docker dry-run validation. | [`reports/S2/multi/patch-risk-diff.md`](../reports/S2/multi/patch-risk-diff.md) |
| 7 | S3 | REVIEW | devex reviewer | 115 | 0 | 1 | 1 | DevEx reviewer checks CI config, then runs CI dry-run validation. | [`reports/S3/multi/patch-risk-diff.md`](../reports/S3/multi/patch-risk-diff.md) |
| 8 | S1 | REVIEW | application reviewer | 110 | 0 | 1 | 1 | Application reviewer checks patch intent, then runs pytest validation. | [`reports/S1/multi/patch-risk-diff.md`](../reports/S1/multi/patch-risk-diff.md) |

## Boundary

Human review remains required before merge or deployment.
The queue uses deterministic fixtures and static patch heuristics; it is not a production security scanner or a replacement for code review.
