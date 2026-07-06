# EvidenceOps Scorecard

EvidenceOps Scorecard is the fourth portfolio demo layer. It checks whether the public ESIPS portfolio has reviewable evidence for the three project lines and whether the public repository remains inside a safe evidence boundary.

It does not replace official application checks. It only reports whether public portfolio artifacts are present, generated, and ready for reviewer inspection.

## What It Checks

| area | examples |
| --- | --- |
| AegisOps Agent evidence | final portfolio report and S4 PR-style summary |
| Kube Copilot evidence | risk comparison and policy matrix |
| Haul Truck Planner evidence | route experiment and algorithm comparison |
| Whole portfolio evidence | README, claims matrix, portfolio status files |

## Commands

```bash
make -C evidenceops-scorecard test
make -C evidenceops-scorecard report
```

Generated reports:

```text
evidenceops-scorecard/reports/evidence-scorecard.md
evidenceops-scorecard/reports/evidence-scorecard.json
evidenceops-scorecard/reports/submission-readiness.md
```

## Boundary

The public repository uses synthetic fixtures only. EvidenceOps checks public artifacts and review readiness; it does not prove production readiness or replace official application checks.
