# Risk Register

This register tracks portfolio risks that matter to a reviewer or interviewer. It is intentionally practical: each risk has a mitigation and an evidence check.

| risk | why it matters | mitigation | evidence check |
| --- | --- | --- | --- |
| Official requirements drift | Public pages and active forms can change after the repo is prepared. | Re-check the current official source before final submission. | Mark changing submission details as needs official confirmation. |
| Portfolio looks like three unrelated demos | Reviewers may miss the unified thesis. | Lead with "AI software engineering with validation" and show the architecture page. | [`docs/ARCHITECTURE.md`](ARCHITECTURE.md), [`docs/PROJECT_COMPARISON.md`](PROJECT_COMPARISON.md) |
| AegisOps overclaim | Agent demos can be mistaken for production automation. | State that the workflow is deterministic, local, and human-reviewed. | [`CLAIMS_MATRIX.md`](../CLAIMS_MATRIX.md), [`docs/REVIEWER_CLAIM_TRACE.md`](REVIEWER_CLAIM_TRACE.md) |
| Kubernetes overtrust | Generated manifests can look correct while carrying deployment risk. | Keep policy checks and human review as the trust boundary. | [`kube-copilot/reports/policy-matrix.md`](../kube-copilot/reports/policy-matrix.md) |
| Planning overclaim | A small graph planner can be mistaken for industrial dispatch. | Present it as a route-planning prototype with explicit constraints. | [`haul-truck-planner/reports/algorithm-comparison.md`](../haul-truck-planner/reports/algorithm-comparison.md) |
| Evidence staleness | Reports can drift from code behavior. | Regenerate evidence with `make demo-all` and run `make portfolio-check`. | [`docs/DEMO_OUTPUT_INDEX.md`](DEMO_OUTPUT_INDEX.md), [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md) |
| Public boundary leak | Public repos should not include private application data, credentials, or personal academic documents. | Run the boundary checker before every push. | `make public-boundary-check` |
| Reviewer overload | Too many files can hide the strongest story. | Point reviewers to the fast path first. | [`docs/REVIEWER_FAST_PATH.md`](REVIEWER_FAST_PATH.md) |

## Go/No-Go Gate

Before sharing the repo, run:

```bash
make demo-all
make portfolio-check
make public-boundary-check
```

Share only if the generated status is PASS and the public boundary check is clean.

