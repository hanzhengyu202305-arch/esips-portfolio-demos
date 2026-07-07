# Roadmap

The roadmap keeps future work aligned with the same thesis: AI software engineering with validation.

## Near Term

| item | value | evidence target |
| --- | --- | --- |
| Keep `make demo-all` stable | one command regenerates reviewer-facing evidence | [`docs/DEMO_OUTPUT_INDEX.md`](DEMO_OUTPUT_INDEX.md) |
| Add more AegisOps scenarios | broaden SDLC coverage beyond the current strongest S4 path | scenario matrix and PR-style reports |
| Expand Kube Copilot policy fixtures | show clearer safe, partial, and risky manifest differences | risk comparison and policy matrix |
| Add route sensitivity analysis | show how reserve threshold, grade, risk cost, and charging access change route choice | route experiment report |
| Tighten EvidenceOps scoring rules | make weak evidence more visible before sharing | scorecard JSON and markdown reports |

## Medium Term

| item | value | evidence target |
| --- | --- | --- |
| AegisOps issue queue demo | closer to GitHub issue triage without requiring live accounts | synthetic issue queue fixture and report |
| Kube policy pack export | make validation rules easier to compare with policy-as-code tools | generated policy matrix |
| Haul Planner EV routing extension | add charge time, queueing, payload mass, and time-window constraints | algorithm-comparison report |
| Release checklist automation | make reviewer packages reproducible across releases | changelog and portfolio status artifacts |

For a fuller optional backlog, read [`docs/OPTIONAL_EXTENSION_PROJECTS.md`](OPTIONAL_EXTENSION_PROJECTS.md).

## Not In Scope For This Portfolio

- Live production remediation.
- Real cluster mutation.
- Full mine fleet dispatch optimisation.
- Formal compliance or certification.
- Storing private application material in the public repository.

## Release Discipline

Every public release should include:

1. Passing `make test`.
2. Passing `make demo-all`.
3. Passing `make portfolio-check`.
4. Passing `make public-boundary-check`.
5. A short release note that states what improved and what remains bounded.
