# Optional Extension Projects

These are optional extensions, not new primary portfolio lines. The current portfolio stays centered on three technical demos plus EvidenceOps. Use these ideas to show a credible next-build backlog without diluting the main story.

## Extension Backlog

| extension | plain purpose | strongest parent line | small demo output | why it helps |
| --- | --- | --- | --- | --- |
| AegisOps Triage Queue | Take several synthetic incidents and rank what should be fixed first. | AegisOps Agent | [`aegisops-agent/reports/triage-queue.md`](../aegisops-agent/reports/triage-queue.md) | Shows the agent workflow can move from one incident to a queue of engineering work. |
| Patch Risk Diff | Compare a proposed patch against risk checks before review. | AegisOps Agent and Kube Copilot | [`aegisops-agent/reports/S4/multi/patch-risk-diff.md`](../aegisops-agent/reports/S4/multi/patch-risk-diff.md) | Makes the human-review boundary stronger and easier to inspect. |
| Kube Policy Pack Exporter | Export the current Kubernetes checks as a small policy pack. | Kube Copilot | JSON or YAML policy table plus generated policy matrix | Makes the validator easier to compare with mature policy-as-code workflows. |
| Mine Route Sensitivity Lab | Re-run the haul route planner under different reserve, charging, and risk settings. | Haul Truck Planner | [`haul-truck-planner/reports/sensitivity-lab.md`](../haul-truck-planner/reports/sensitivity-lab.md) | Shows planning is about constraint tradeoffs, not one hard-coded route. |
| EvidenceOps Release Gate | Turn the evidence scorecard into a release checklist. | EvidenceOps Scorecard | release gate report with pass/fail checks and reviewer links | Connects portfolio evidence to a professional release habit. |

## How To Talk About Them

Safe wording:

> The completed portfolio has three demo lines and one evidence layer. These optional extensions are the next backlog: triage more incidents, risk-check patches, export policy rules, run route sensitivity analysis, and turn EvidenceOps into a release gate.

Avoid wording:

- Do not present these backlog items as completed production systems.
- Do not say they replace existing mature tools.
- Do not make them equal to the three current evidence lines.

## Best Next Build Order

1. **Mine Route Sensitivity Lab**: implemented as a small extension; keep improving it if the EE and planning angle needs more depth.
2. **AegisOps Triage Queue**: implemented as a small extension; deepen it next if the SDLC agent line needs more realism.
3. **Patch Risk Diff**: implemented as a small extension; deepen it next if patch review needs richer policy checks.
4. **Kube Policy Pack Exporter**: good if the reviewer cares about platform engineering.
5. **EvidenceOps Release Gate**: good polish after the technical extensions are stable.

## Minimal Acceptance Criteria

Each extension should have:

- one deterministic fixture,
- one generated markdown report,
- one unit test,
- one boundary note,
- one link from the reviewer evidence path.

If an extension does not meet those criteria, keep it as roadmap language rather than a completed project claim.
