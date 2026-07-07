# Roadmap

The roadmap keeps future work aligned with the same thesis: AI software engineering with validation.

## Near Term

| item | value | evidence target |
| --- | --- | --- |
| Keep `make demo-all` stable | one command regenerates reviewer-facing evidence | [`docs/DEMO_OUTPUT_INDEX.md`](DEMO_OUTPUT_INDEX.md) |
| Add more AegisOps scenarios | broaden SDLC coverage beyond the current strongest S4 path | scenario matrix and PR-style reports |
| Deepen AegisOps patch review queue | make multi-scenario patch risk easier to inspect before review | [`aegisops-agent/reports/patch-review-queue.md`](../aegisops-agent/reports/patch-review-queue.md) |
| Expand Kube Copilot policy fixtures | show clearer safe, partial, and risky manifest differences | risk comparison and policy matrix |
| Extend route sensitivity analysis | show how reserve threshold, risk cost, and charging access change route choice | [`haul-truck-planner/reports/sensitivity-lab.md`](../haul-truck-planner/reports/sensitivity-lab.md) |
| Extend EvidenceOps release gate | add changelog and release-note checks after the current gate | [`evidenceops-scorecard/reports/release-gate.md`](../evidenceops-scorecard/reports/release-gate.md) |

## Medium Term

| item | value | evidence target |
| --- | --- | --- |
| Extend AegisOps triage queue | closer to GitHub issue triage without requiring live accounts | [`aegisops-agent/reports/triage-queue.md`](../aegisops-agent/reports/triage-queue.md) |
| Extend Patch Risk Diff | add richer policy checks over proposed patch previews and queue-level review labels | [`aegisops-agent/reports/patch-review-queue.md`](../aegisops-agent/reports/patch-review-queue.md) |
| Extend Kube policy pack | add richer mapping from validator findings to policy-as-code concepts | [`kube-copilot/reports/policy-pack.md`](../kube-copilot/reports/policy-pack.md) |
| Haul Planner EV routing extension | add charge time, queueing, payload mass, and time-window constraints | algorithm-comparison report |
| Release checklist automation | make reviewer packages reproducible across releases | release gate plus future changelog artifacts |

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
