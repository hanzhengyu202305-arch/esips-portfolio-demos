# AegisOps Agent SPEC

## Objective

Build a GitHub-ready portfolio project that demonstrates an agentic DevOps remediation loop:

```text
observe signals -> retrieve context -> diagnose root cause -> generate patch -> validate -> report metrics
```

## MVP Definition of Done

Functional:

- At least 6 failure scenarios run through the Makefile
- Each scenario has a gold label `root_cause_id`
- Agent outputs structured `diagnosis.json`
- Agent generates `patch.diff`
- Patch generation enforces `allowed_files` and `blocked_files`
- Validation includes pytest and one DevOps validation
- `reports/eval-summary.md` is generated

Quality:

- `make test` passes
- `make lint` passes
- CI and eval-mock workflows exist
- MockLLM runs without API keys

Evaluation:

- Compare single-agent and multi-agent modes
- Report diagnosis accuracy, fix success, latency, estimated cost, and tool calls

Documentation:

- README includes an architecture diagram
- `docs/NEWCOMER_GUIDE.zh-CN.md` gives a beginner-first Chinese path through the project
- `docs/demo-script.md` supports a 5-minute demo
- `docs/esips-accenture-mapping.md` maps the project to ESIPS and Accenture themes
- `reports/scenario-matrix.md` lists every scenario, allowed patch target, and validation type
- `reports/doctor.json` records local environment readiness without requiring Docker or kind
- `reports/acceptance-checklist.md` verifies portfolio readiness before sharing

Safety:

- The agent must not patch CI workflows, gold labels, or tests
- The agent must generate a readable diff before materializing a patch preview
