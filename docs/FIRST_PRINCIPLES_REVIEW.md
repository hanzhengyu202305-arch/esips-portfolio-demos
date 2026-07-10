# First-Principles And Adversarial Review

## Objective

The portfolio is useful only if a time-constrained reviewer can verify three claims:

1. The candidate can turn an industry brief into a scoped engineering problem.
2. The implementation handles failure cases, not only a prepared happy path.
3. Every claim is inspectable and bounded by what the demo actually proves.

A practical model is:

```text
portfolio value = relevance x credibility x inspectability
```

More files do not compensate for a zero in any one factor. The optimization therefore prioritizes negative controls, independent evidence, and short reviewer paths over adding more mini-projects.

## Adversarial Findings And Fixes

| attack | original weakness | implemented control | evidence |
| --- | --- | --- | --- |
| Tamper the AegisOps gold label | The old deterministic client returned `ScenarioSpec.root_cause_id` directly. | Diagnosis now ranks evidence patterns independently of the fixture label. | [`docs/ADVERSARIAL_REVIEW.md`](ADVERSARIAL_REVIEW.md), [`aegisops-agent/reports/S4/multi/diagnosis.json`](../aegisops-agent/reports/S4/multi/diagnosis.json) |
| Remove or conflict AegisOps evidence | A prepared scenario always produced a patch. | Insufficient or tied evidence returns `ESCALATE`; patch generation is stopped. | [`docs/ADVERSARIAL_REVIEW.md`](ADVERSARIAL_REVIEW.md) |
| Hide unsafe Kubernetes settings in comments, sidecars, or later YAML documents | String matching could confuse text presence with effective configuration. | PyYAML parses every document and validates every application and init container. | [`kube-copilot/reports/adversarial-validation.md`](../kube-copilot/reports/adversarial-validation.md) |
| Feed impossible map or battery states to the route planner | Hidden numeric assumptions and unchecked inputs reduced model credibility. | The planner validates topology and battery invariants; energy parameters are explicit and configurable. | [`haul-truck-planner/reports/route-experiment.md`](../haul-truck-planner/reports/route-experiment.md) |
| Stuff EvidenceOps files with expected words | File-size and keyword checks could overstate evidence quality. | Structured JSON checks now validate diagnosis decisions, policy rules, and adversarial challenge results. | [`evidenceops-scorecard/reports/evidence-scorecard.md`](../evidenceops-scorecard/reports/evidence-scorecard.md) |

## One-Command Challenge Gate

```bash
make adversarial-review
```

The command runs deterministic negative controls across all three technical lines and writes:

```text
docs/ADVERSARIAL_REVIEW.md
docs/ADVERSARIAL_REVIEW.json
```

`make portfolio-check` and the EvidenceOps release gate require this suite to pass.

## Residual Limits

- AegisOps uses a deterministic evidence-rule harness and pre-authored synthetic patch fixtures. It is not a live LLM software-engineering agent.
- Kube Copilot checks a focused policy subset. It is not Kubernetes schema validation, an API-server dry run, or admission control.
- Haul Truck Planner is grid route planning with synthetic parameters, not continuous trajectory control, calibrated vehicle dynamics, or fleet dispatch.
- EvidenceOps measures evidence completeness and structural consistency. It does not independently certify engineering quality or application success.

These limits are part of the evidence, not footnotes to hide. They show exactly what the next industry-data, benchmark, or production-integration step would need to replace.
