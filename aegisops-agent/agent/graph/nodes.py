from __future__ import annotations

import json
import time
from pathlib import Path

from agent.llm.mock_client import MockLLM
from agent.memory.retriever import build_index, retrieve
from agent.scenario_runner import run_scenario
from agent.scenarios import get_scenario
from agent.schemas import AgentRunResult, Diagnosis, EvalResult, PatchResult
from agent.tools.evidence_tools import collect_evidence
from agent.tools.file_tools import write_patch_preview
from agent.tools.test_tools import run_validation


def run_agent_flow(
    scenario_id: str,
    mode: str,
    reports_dir: Path | str = Path("reports"),
) -> AgentRunResult:
    start = time.perf_counter()
    if mode not in {"single", "multi"}:
        raise ValueError("mode must be 'single' or 'multi'")

    scenario = get_scenario(scenario_id)
    reports_path = Path(reports_dir)
    run_dir = reports_path / scenario.scenario_id / mode
    run_dir.mkdir(parents=True, exist_ok=True)

    run_scenario(scenario.scenario_id, reports_path)
    evidence_path = collect_evidence(scenario.scenario_id, reports_path)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))

    index_path = build_index()
    contexts = retrieve(scenario.runbook_query, index_path=index_path, limit=3)

    mock_llm = MockLLM()
    diagnosis = mock_llm.diagnose(scenario, evidence, contexts, mode)
    _write_json(run_dir / "diagnosis.json", diagnosis.to_dict())

    trace = _stage_trace(mode, scenario.scenario_id, diagnosis.root_cause_id)
    if mode == "multi":
        _write_json(run_dir / "agent-trace.json", trace)

    diff_path, patched_dir, files_changed = write_patch_preview(
        run_dir=run_dir,
        broken_files=scenario.broken_files,
        fixed_files=scenario.fixed_files,
        allowed_files=scenario.allowed_files,
        blocked_files=scenario.blocked_files,
    )

    validation = run_validation(
        scenario.scenario_id,
        mode=mode,
        reports_dir=reports_path,
        patched_dir=patched_dir,
    )
    patch = PatchResult(
        scenario_id=scenario.scenario_id,
        files_changed=files_changed,
        diff_path=str(diff_path),
        patch_applied=True,
        validation_passed=validation.passed,
        commands_run=validation.commands_run,
    )

    prompt_tokens, completion_tokens = mock_llm.estimate_tokens(scenario, mode)
    elapsed = round(max(time.perf_counter() - start, 0.001), 3)
    tool_calls = 6 if mode == "single" else 10
    metrics = EvalResult(
        scenario_id=scenario.scenario_id,
        mode=mode,  # type: ignore[arg-type]
        root_cause_correct=diagnosis.root_cause_id == scenario.root_cause_id,
        fix_successful=patch.patch_applied and patch.validation_passed,
        latency_seconds=elapsed,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        estimated_cost_usd=round(
            (prompt_tokens * 0.00000015) + (completion_tokens * 0.0000006),
            6,
        ),
        tool_calls=tool_calls,
    )
    _write_json(run_dir / "patch-result.json", patch.to_dict())
    _write_json(run_dir / "metrics.json", metrics.to_dict())
    _write_demo_report(run_dir, scenario.title, diagnosis.root_cause_id, metrics)
    _write_pr_summary(run_dir, scenario.title, diagnosis, patch, metrics)

    return AgentRunResult(
        diagnosis=diagnosis,
        patch=patch,
        metrics=metrics,
        run_dir=str(run_dir),
    )


def _stage_trace(mode: str, scenario_id: str, root_cause_id: str) -> list[dict]:
    if mode == "single":
        return [
            {
                "agent": "SingleAgent",
                "action": "diagnose_patch_validate",
                "scenario_id": scenario_id,
                "root_cause_id": root_cause_id,
            }
        ]
    return [
        {"agent": "TriageAgent", "action": "group evidence by source"},
        {"agent": "RCAAgent", "action": f"select root_cause_id={root_cause_id}"},
        {"agent": "FixAgent", "action": "generate whitelisted patch preview"},
        {"agent": "ReviewAgent", "action": "check validation and guardrails"},
    ]


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_demo_report(
    run_dir: Path,
    title: str,
    root_cause_id: str,
    metrics: EvalResult,
) -> None:
    report = f"""# Demo Report: {title}

- root_cause_id: `{root_cause_id}`
- mode: `{metrics.mode}`
- root_cause_correct: `{metrics.root_cause_correct}`
- fix_successful: `{metrics.fix_successful}`
- latency_seconds: `{metrics.latency_seconds}`
- estimated_cost_usd: `{metrics.estimated_cost_usd}`
- tool_calls: `{metrics.tool_calls}`
"""
    (run_dir / "demo-report.md").write_text(report, encoding="utf-8")


def _write_pr_summary(
    run_dir: Path,
    title: str,
    diagnosis: Diagnosis,
    patch: PatchResult,
    metrics: EvalResult,
) -> None:
    files_changed = "\n".join(f"- `{path}`" for path in patch.files_changed)
    commands_run = "\n".join(f"- `{command}`" for command in patch.commands_run)
    validation_status = "passed" if patch.validation_passed else "failed"
    report = f"""# PR Summary

## Incident

{title}

## Root Cause

`{diagnosis.root_cause_id}` with confidence `{diagnosis.confidence}`.

{diagnosis.impact}

## Files Changed

{files_changed}

## Validation

Validation: {validation_status}

Commands run:

{commands_run}

## Risk And Review

- Human review required before merge.
- Patch targets were checked against the scenario allowlist.
- CI workflows, tests, and gold labels remain blocked patch targets.

## Metrics

- mode: `{metrics.mode}`
- root_cause_correct: `{metrics.root_cause_correct}`
- fix_successful: `{metrics.fix_successful}`
- latency_seconds: `{metrics.latency_seconds}`
- estimated_cost_usd: `{metrics.estimated_cost_usd}`
- tool_calls: `{metrics.tool_calls}`
"""
    (run_dir / "pr-summary.md").write_text(report, encoding="utf-8")
