# Reviewer Fast Path

## 2-Minute Path

1. Read the thesis in [`docs/EXECUTIVE_ONE_PAGE.md`](EXECUTIVE_ONE_PAGE.md).
2. Confirm the three project mapping in [`THREE_LINE_ESIPS_PLAN.md`](../THREE_LINE_ESIPS_PLAN.md).
3. Open the claim trace: [`docs/REVIEWER_CLAIM_TRACE.md`](REVIEWER_CLAIM_TRACE.md).
4. Open the main evidence artifact: [`aegisops-agent/reports/S4/multi/pr-summary.md`](../aegisops-agent/reports/S4/multi/pr-summary.md).
5. Open the evidence quality layer: [`evidenceops-scorecard/reports/evidence-scorecard.md`](../evidenceops-scorecard/reports/evidence-scorecard.md).
6. Check the negative controls: [`docs/ADVERSARIAL_REVIEW.md`](ADVERSARIAL_REVIEW.md).
7. Open the release/share gate: [`evidenceops-scorecard/reports/release-gate.md`](../evidenceops-scorecard/reports/release-gate.md).

## 10-Minute Evidence Path

| project | inspect first | why |
| --- | --- | --- |
| AegisOps Agent | [`aegisops-agent/reports/S4/multi/issue-to-pr-report.md`](../aegisops-agent/reports/S4/multi/issue-to-pr-report.md) | Shows issue -> evidence -> RCA -> patch -> validation -> PR summary. |
| AegisOps Patch Review Queue | [`aegisops-agent/reports/patch-review-queue.md`](../aegisops-agent/reports/patch-review-queue.md) | Shows how patch reviews are ranked across scenarios before human review. |
| Kube Copilot | [`kube-copilot/reports/adversarial-validation.md`](../kube-copilot/reports/adversarial-validation.md) | Shows structural YAML checks rejecting comments, unsafe sidecars, and later documents. |
| Haul Truck Planner | [`haul-truck-planner/reports/algorithm-comparison.md`](../haul-truck-planner/reports/algorithm-comparison.md) | Shows shortest path vs Dijkstra vs A* under explicit energy constraints. |
| Portfolio Adversarial Review | [`docs/ADVERSARIAL_REVIEW.md`](ADVERSARIAL_REVIEW.md) | Shows expected failures, rejection behavior, and 12 cross-project negative controls. |
| EvidenceOps Scorecard | [`evidenceops-scorecard/reports/evidence-scorecard.md`](../evidenceops-scorecard/reports/evidence-scorecard.md) | Shows PASS/WEAK/MISSING evidence, completeness score, and manual-review boundary. |
| EvidenceOps Release Gate | [`evidenceops-scorecard/reports/release-gate.md`](../evidenceops-scorecard/reports/release-gate.md) | Shows whether public evidence is ready to share or blocked. |
| Whole repo | [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md) | Shows the latest local verification gate. |

## 30-Minute Local Validation

```bash
make demo-all
make test
make adversarial-review
make portfolio-check
```

`make demo-all` writes [`docs/DEMO_OUTPUT_INDEX.md`](DEMO_OUTPUT_INDEX.md), which links the refreshed outputs for all four public demo layers.

If the local AegisOps Python path differs:

```bash
make portfolio-check AEGISOPS_PY=python3
```

## Reviewer Boundary

The useful evidence is the reproducible workflow, not a production claim. The demos use local fixtures, deterministic checks, and generated reports so they can be inspected without external accounts, cloud credentials, or private data.
