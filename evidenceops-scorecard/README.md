# EvidenceOps Scorecard

EvidenceOps Scorecard is the fourth portfolio demo layer. It checks whether the public ESIPS portfolio has reviewable evidence for the three project lines and whether the public repository remains inside a safe evidence boundary.

It does not replace official application checks. It reports whether public portfolio artifacts are present, generated, strong enough for reviewer inspection, and separated from items that still need official confirmation.

## What It Checks

| area | examples |
| --- | --- |
| AegisOps Agent evidence | final portfolio report and S4 PR-style summary |
| Kube Copilot evidence | risk comparison and policy matrix |
| Haul Truck Planner evidence | route experiment and algorithm comparison |
| Whole portfolio evidence | README, claims matrix, portfolio status files |

Each evidence item is classified as:

| status | meaning |
| --- | --- |
| `PASS` | artifact exists and meets minimum quality checks |
| `WEAK` | artifact exists but is too thin or missing expected keywords |
| `MISSING` | artifact is absent |

The generated report includes a `0-100` quality score, weak evidence list, missing evidence list, and specific quality-fix hints.

The release gate turns the same evidence into a public release/share decision. It checks whether scorecard evidence is PASS, portfolio status is PASS, demo outputs were regenerated, claim trace exists, and public boundary checks passed.

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

The public repository uses synthetic fixtures only. EvidenceOps checks public artifacts and review readiness; it does not prove production readiness or replace official application checks.
