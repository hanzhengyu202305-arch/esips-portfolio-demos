from __future__ import annotations

import json
from pathlib import Path

from agent.evaluation.evaluator import run_eval
from agent.graph.multi_agent import run_multi_agent
from agent.graph.single_agent import run_single_agent
from agent.scenarios import get_scenario
from agent.tools.file_tools import PatchSafetyError, validate_patch_targets


def test_patch_safety_rejects_blocked_targets() -> None:
    scenario = get_scenario("S1")

    try:
        validate_patch_targets(
            ["apps/demo-api/tests/test_demo_api.py"],
            allowed_files=scenario.allowed_files,
            blocked_files=scenario.blocked_files,
        )
    except PatchSafetyError as exc:
        assert "blocked" in str(exc)
    else:
        raise AssertionError("blocked patch target should raise PatchSafetyError")


def test_single_agent_demo_generates_expected_reports(tmp_path: Path) -> None:
    result = run_single_agent("S1", reports_dir=tmp_path)

    assert result.diagnosis.root_cause_id == "wrong_discount_logic"
    assert result.patch.patch_applied is True
    assert result.patch.validation_passed is True
    assert (tmp_path / "S1" / "single" / "diagnosis.json").exists()
    assert (tmp_path / "S1" / "single" / "patch.diff").exists()
    assert (tmp_path / "S1" / "single" / "metrics.json").exists()


def test_multi_agent_demo_writes_stage_trace_and_s4_root_cause(tmp_path: Path) -> None:
    result = run_multi_agent("S4", reports_dir=tmp_path)

    trace_path = tmp_path / "S4" / "multi" / "agent-trace.json"
    trace = json.loads(trace_path.read_text())

    assert result.diagnosis.root_cause_id == "invalid_app_mode_env"
    assert [stage["agent"] for stage in trace] == [
        "TriageAgent",
        "RCAAgent",
        "FixAgent",
        "ReviewAgent",
    ]


def test_demo_writes_pr_summary_for_validated_fix(tmp_path: Path) -> None:
    run_multi_agent("S4", reports_dir=tmp_path)

    summary_path = tmp_path / "S4" / "multi" / "pr-summary.md"
    summary = summary_path.read_text()

    assert summary.startswith("# PR Summary")
    assert "invalid_app_mode_env" in summary
    assert "k8s/overlays/broken-env/deployment.yaml" in summary
    assert "Validation: passed" in summary
    assert "Human review required before merge" in summary


def test_eval_mock_generates_summary_and_metrics(tmp_path: Path) -> None:
    summary_path = run_eval(reports_dir=tmp_path, scenarios=["S1", "S4", "S7"])

    summary = summary_path.read_text()
    results = json.loads((tmp_path / "eval-results.json").read_text())

    assert "diagnosis_accuracy" in summary
    assert "fix_success_rate" in summary
    assert "estimated_cost_usd" in summary
    assert len(results) == 6
    assert all(item["root_cause_correct"] for item in results)
