# AegisOps Agent Data Card

## Dataset Summary

AegisOps uses synthetic, deterministic incident fixtures for portfolio and interview demonstration. The project does not use real customer data, employer data, university records, production logs, credentials, or proprietary Accenture material.

Primary data artifacts:

- `scenarios/*/scenario.json`: source scenario definitions.
- `reports/*/scenario.json`: copied scenario evidence for reviewer inspection.
- `reports/*/raw_failure.log`: generated failure logs for each scenario.
- `reports/*/evidence.json`: structured evidence generated from scenario metadata and logs.
- `docs/runbooks/*.md`: local runbook documents used by the retrieval layer.
- `docs/incidents/previous_incidents.json`: synthetic previous-incident memory.
- `agent/evaluation/gold_labels.json`: expected root-cause labels for deterministic scoring.

## Intended Use

The fixtures are intended to test an agentic DevOps workflow under controlled conditions:

1. Read operational signals.
2. Retrieve relevant runbook context.
3. Diagnose root cause.
4. Generate a safe patch preview.
5. Validate the fix.
6. Report metrics for single-agent and multi-agent modes.

They are not intended to represent production incident distributions or real Kubernetes fleet behavior.

## Field Dictionary

Typical scenario fields:

| field | meaning |
| --- | --- |
| `scenario_id` | Stable identifier such as `S4`. |
| `slug` | Human-readable scenario key. |
| `title` | Reviewer-facing incident title. |
| `category` | Incident category such as `kubernetes`, `ci`, `docker`, `security`, or `latency`. |
| `root_cause_id` | Gold label used for accuracy scoring. |
| `signals` | Structured incident signals presented to the agent. |
| `allowed_files` | Files the patch guard allows the agent to modify. |
| `blocked_files` | Files the agent must not modify. |
| `validation_kind` | Validation route used after patch preview generation. |
| `runbook_query` | Query used to retrieve relevant Markdown runbook context. |
| `broken_files` | Minimal faulty file snippets for the scenario. |
| `fixed_files` | Expected fixed file snippets for the scenario. |

## Licensing And Access

The data is generated within this local project for demonstration and educational use. Before public GitHub release, add a repository `LICENSE` file and keep this Data Card with the release so reviewers can understand data provenance.

## Privacy And Sensitive Information

- No real secrets are required.
- `.env.example` and `ci/env.example.yml` are examples only.
- Do not add real API keys, cloud credentials, university credentials, broker data, or private logs.
- If future real incident logs are added, redact names, tokens, hostnames, account IDs, IP addresses, emails, repository URLs, and customer identifiers before committing them.

## Known Limitations

- The benchmark is small and deterministic.
- `MockLLM` makes results reproducible but does not prove performance with real LLM variance.
- The current scenario suite emphasizes workflow correctness, guardrails, and measurable trade-offs rather than broad incident diversity.
- Kubernetes validation is local/dry-run oriented unless optional Docker/kind tooling is available.

## Refresh Procedure

Run:

```bash
make matrix
make eval-mock
make acceptance
```

Review:

- `reports/scenario-matrix.md`
- `reports/eval-summary.md`
- `reports/acceptance-checklist.md`

If scenario definitions change, rerun the commands above and verify that `reports/eval-results.json` still includes both `single` and `multi` modes for every scenario.
