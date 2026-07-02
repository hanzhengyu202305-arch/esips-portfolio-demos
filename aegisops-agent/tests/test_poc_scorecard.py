from __future__ import annotations

import json
from pathlib import Path

from agent.poc import (
    create_reproducibility_report,
    create_scorecard,
    score_eval_results,
)


def _sample_results() -> list[dict]:
    return [
        {
            "scenario_id": "S1",
            "mode": "single",
            "root_cause_correct": True,
            "fix_successful": True,
            "latency_seconds": 0.42,
            "prompt_tokens": 120,
            "completion_tokens": 60,
            "estimated_cost_usd": 0.00020,
            "tool_calls": 3,
        },
        {
            "scenario_id": "S1",
            "mode": "multi",
            "root_cause_correct": True,
            "fix_successful": True,
            "latency_seconds": 0.47,
            "prompt_tokens": 180,
            "completion_tokens": 80,
            "estimated_cost_usd": 0.00033,
            "tool_calls": 5,
        },
        {
            "scenario_id": "S2",
            "mode": "single",
            "root_cause_correct": True,
            "fix_successful": True,
            "latency_seconds": 0.50,
            "prompt_tokens": 120,
            "completion_tokens": 60,
            "estimated_cost_usd": 0.00021,
            "tool_calls": 3,
        },
        {
            "scenario_id": "S2",
            "mode": "multi",
            "root_cause_correct": True,
            "fix_successful": True,
            "latency_seconds": 0.55,
            "prompt_tokens": 180,
            "completion_tokens": 80,
            "estimated_cost_usd": 0.00034,
            "tool_calls": 5,
        },
    ]


def test_score_eval_results_builds_weighted_poc_metrics() -> None:
    scored = score_eval_results(
        _sample_results(),
        config={
            "weights": {
                "functional": 0.35,
                "performance": 0.20,
                "quality": 0.30,
                "cost_ops": 0.15,
            },
            "thresholds": {
                "diagnosis_accuracy_min": 0.90,
                "fix_success_rate_min": 0.85,
                "avg_latency_seconds_max": 1.00,
                "max_cost_per_run_usd": 0.001,
                "evaluated_runs_min": 4,
            },
        },
    )

    assert scored["status"] == "PASS"
    assert scored["score"] == 100.0
    assert scored["metrics"]["functional"]["evaluated_runs"] == 4
    assert scored["metrics"]["functional"]["scenarios"] == ["S1", "S2"]
    assert scored["metrics"]["quality"]["diagnosis_accuracy"] == 1.0
    assert scored["metrics"]["performance"]["avg_latency_seconds"] == 0.485
    assert scored["metrics"]["cost_ops"]["max_cost_per_run_usd"] == 0.00034
    assert scored["breakdown"]["quality"]["weighted_points"] == 30.0


def test_create_scorecard_writes_reviewer_artifacts(tmp_path: Path) -> None:
    (tmp_path / "eval-results.json").write_text(
        json.dumps(_sample_results(), indent=2),
        encoding="utf-8",
    )

    result = create_scorecard(
        reports_dir=tmp_path,
        config={
            "weights": {
                "functional": 0.35,
                "performance": 0.20,
                "quality": 0.30,
                "cost_ops": 0.15,
            },
            "thresholds": {
                "diagnosis_accuracy_min": 0.90,
                "fix_success_rate_min": 0.85,
                "avg_latency_seconds_max": 1.00,
                "max_cost_per_run_usd": 0.001,
                "evaluated_runs_min": 4,
            },
        },
    )

    scorecard = result.scorecard_path.read_text(encoding="utf-8")
    metrics = json.loads(result.metrics_path.read_text(encoding="utf-8"))

    assert "导师评分: 100.0/100" in scorecard
    assert "结论: PASS" in scorecard
    assert "diagnosis_accuracy" in scorecard
    assert metrics["status"] == "PASS"
    assert metrics["score"] == 100.0
    assert metrics["metrics"]["functional"]["evaluated_runs"] == 4


def test_reproducibility_report_summarizes_run_variance(tmp_path: Path) -> None:
    run_a = score_eval_results(_sample_results())["metrics"]
    run_b = score_eval_results(
        [{**item, "latency_seconds": item["latency_seconds"] + 0.1} for item in _sample_results()]
    )["metrics"]

    path = create_reproducibility_report(tmp_path, [run_a, run_b])
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["runs_count"] == 2
    assert payload["diagnosis_accuracy_min"] == 1.0
    assert payload["fix_success_rate_min"] == 1.0
    assert payload["avg_latency_seconds_mean"] == 0.535
    assert payload["avg_latency_seconds_stdev"] > 0
