# EvidenceOps Scorecard

EvidenceOps Scorecard is the fourth portfolio demo layer. It checks whether the public ESIPS portfolio has reviewable evidence for the three project lines and whether the public repository remains inside a safe evidence boundary.

It does not replace official application checks. It reports whether public portfolio artifacts are present, structurally consistent, and separated from items that still need official confirmation.

## What It Checks

| area | examples |
| --- | --- |
| AegisOps Agent evidence | final report, S4 PR summary, and structured ranked diagnosis |
| Kube Copilot evidence | risk comparison, policy pack, and adversarial YAML report |
| Haul Truck Planner evidence | route experiment with explicit assumptions and algorithm comparison |
| Whole portfolio evidence | README, claims matrix, portfolio status, and adversarial review results |

Each evidence item is classified as:

| status | meaning |
| --- | --- |
| `PASS` | artifact exists and meets minimum quality checks |
| `WEAK` | artifact exists but is too thin or missing expected keywords |
| `MISSING` | artifact is absent |

The generated report includes a `0-100` evidence completeness score, weak evidence list, missing evidence list, and specific fixes. It validates structured JSON fields for diagnoses, policy rules, and adversarial challenges so keyword stuffing alone does not pass.

The release gate turns the same evidence into a public release/share decision. It checks whether scorecard evidence is PASS, portfolio status is PASS, adversarial controls passed, demo outputs were regenerated, claim trace exists, and public boundary checks passed.

## Commands

```bash
make -C evidenceops-scorecard test
make -C evidenceops-scorecard report
make -C evidenceops-scorecard release-gate
```

Generated reports:

```text
evidenceops-scorecard/reports/evidence-scorecard.md
evidenceops-scorecard/reports/evidence-scorecard.json
evidenceops-scorecard/reports/submission-readiness.md
evidenceops-scorecard/reports/release-gate.md
evidenceops-scorecard/reports/release-gate.json
```

## Boundary

The public repository uses synthetic fixtures only. EvidenceOps measures evidence completeness and structural consistency; it does not independently certify engineering quality, prove production readiness, or replace official application checks.
