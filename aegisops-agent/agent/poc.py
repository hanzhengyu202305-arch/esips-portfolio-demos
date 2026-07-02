from __future__ import annotations

import json
import statistics as stats
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent.evaluation.evaluator import run_eval


DEFAULT_POC_CONFIG = {
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
        "evaluated_runs_min": 16,
    },
}


@dataclass(frozen=True)
class ScorecardResult:
    scorecard_path: Path
    metrics_path: Path
    status: str
    score: float
    payload: dict[str, Any]


def load_poc_config(config_path: Path | str = Path("config/poc-scorecard.json")) -> dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        return DEFAULT_POC_CONFIG

    config = json.loads(path.read_text(encoding="utf-8"))
    merged = {
        "weights": {**DEFAULT_POC_CONFIG["weights"], **config.get("weights", {})},
        "thresholds": {**DEFAULT_POC_CONFIG["thresholds"], **config.get("thresholds", {})},
    }
    return merged


def score_eval_results(
    results: list[dict[str, Any]],
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not results:
        raise ValueError("eval results are empty")

    active_config = config or DEFAULT_POC_CONFIG
    weights = active_config["weights"]
    thresholds = active_config["thresholds"]

    evaluated_runs = len(results)
    scenarios = sorted({str(item["scenario_id"]) for item in results})
    modes = sorted({str(item["mode"]) for item in results})
    diagnosis_accuracy = _ratio(item["root_cause_correct"] for item in results)
    fix_success_rate = _ratio(item["fix_successful"] for item in results)
    avg_latency = _avg(float(item["latency_seconds"]) for item in results)
    max_cost = max(float(item["estimated_cost_usd"]) for item in results)
    total_cost = sum(float(item["estimated_cost_usd"]) for item in results)
    avg_tool_calls = _avg(float(item["tool_calls"]) for item in results)

    metrics = {
        "functional": {
            "evaluated_runs": evaluated_runs,
            "scenarios": scenarios,
            "modes": modes,
            "fix_success_rate": round(fix_success_rate, 3),
        },
        "performance": {
            "avg_latency_seconds": round(avg_latency, 3),
            "avg_tool_calls": round(avg_tool_calls, 3),
        },
        "quality": {
            "diagnosis_accuracy": round(diagnosis_accuracy, 3),
        },
        "cost_ops": {
            "max_cost_per_run_usd": round(max_cost, 6),
            "total_estimated_cost_usd": round(total_cost, 6),
        },
    }

    breakdown = {
        "functional": _weighted(
            _positive_score(fix_success_rate, thresholds["fix_success_rate_min"])
            * _positive_score(evaluated_runs, thresholds["evaluated_runs_min"])
            / 100,
            weights["functional"],
        ),
        "performance": _weighted(
            _inverse_threshold_score(avg_latency, thresholds["avg_latency_seconds_max"]),
            weights["performance"],
        ),
        "quality": _weighted(
            _positive_score(diagnosis_accuracy, thresholds["diagnosis_accuracy_min"]),
            weights["quality"],
        ),
        "cost_ops": _weighted(
            _inverse_threshold_score(max_cost, thresholds["max_cost_per_run_usd"]),
            weights["cost_ops"],
        ),
    }
    score = round(sum(item["weighted_points"] for item in breakdown.values()), 1)
    status = "PASS" if _passes(metrics, thresholds) else "FAIL"

    return {
        "status": status,
        "score": score,
        "metrics": metrics,
        "breakdown": breakdown,
        "thresholds": thresholds,
        "weights": weights,
    }


def create_scorecard(
    reports_dir: Path | str = Path("reports"),
    config_path: Path | str = Path("config/poc-scorecard.json"),
    config: dict[str, Any] | None = None,
) -> ScorecardResult:
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)
    eval_results_path = reports_path / "eval-results.json"
    if not eval_results_path.exists():
        run_eval(reports_path)

    results = json.loads(eval_results_path.read_text(encoding="utf-8"))
    payload = score_eval_results(results, config=config or load_poc_config(config_path))

    metrics_path = reports_path / "poc-metrics.json"
    scorecard_path = reports_path / "scorecard.txt"
    metrics_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    scorecard_path.write_text(_render_scorecard(payload), encoding="utf-8")

    return ScorecardResult(
        scorecard_path=scorecard_path,
        metrics_path=metrics_path,
        status=str(payload["status"]),
        score=float(payload["score"]),
        payload=payload,
    )


def create_reproducibility_report(
    reports_dir: Path | str,
    run_metrics: list[dict[str, Any]],
) -> Path:
    if not run_metrics:
        raise ValueError("run_metrics must contain at least one run")

    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    latencies = [
        float(run["performance"]["avg_latency_seconds"])
        for run in run_metrics
    ]
    diagnosis = [
        float(run["quality"]["diagnosis_accuracy"])
        for run in run_metrics
    ]
    fix_rates = [
        float(run["functional"]["fix_success_rate"])
        for run in run_metrics
    ]
    costs = [
        float(run["cost_ops"]["max_cost_per_run_usd"])
        for run in run_metrics
    ]

    payload = {
        "runs_count": len(run_metrics),
        "runs": run_metrics,
        "diagnosis_accuracy_min": round(min(diagnosis), 3),
        "fix_success_rate_min": round(min(fix_rates), 3),
        "avg_latency_seconds_mean": round(stats.mean(latencies), 3),
        "avg_latency_seconds_stdev": round(stats.pstdev(latencies), 6),
        "max_cost_per_run_usd_max": round(max(costs), 6),
    }
    path = reports_path / "reproducibility_report.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def run_poc_repro(
    reports_dir: Path | str = Path("reports"),
    runs: int = 3,
    config_path: Path | str = Path("config/poc-scorecard.json"),
) -> Path:
    if runs < 1:
        raise ValueError("runs must be >= 1")

    reports_path = Path(reports_dir)
    metrics_by_run: list[dict[str, Any]] = []
    for run_id in range(1, runs + 1):
        run_eval(reports_path)
        result = create_scorecard(reports_path, config_path=config_path)
        metrics = dict(result.payload["metrics"])
        metrics["run_id"] = run_id
        metrics["score"] = result.score
        metrics["status"] = result.status
        metrics_by_run.append(metrics)

    return create_reproducibility_report(reports_path, metrics_by_run)


def _render_scorecard(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    lines = [
        f"导师评分: {payload['score']}/100",
        f"结论: {payload['status']}",
        "",
        "关键指标:",
        f"- diagnosis_accuracy: {metrics['quality']['diagnosis_accuracy']}",
        f"- fix_success_rate: {metrics['functional']['fix_success_rate']}",
        f"- avg_latency_seconds: {metrics['performance']['avg_latency_seconds']}",
        f"- max_cost_per_run_usd: {metrics['cost_ops']['max_cost_per_run_usd']}",
        f"- evaluated_runs: {metrics['functional']['evaluated_runs']}",
        "",
        "明细:",
        json.dumps(payload["breakdown"], ensure_ascii=False, indent=2),
    ]
    return "\n".join(lines) + "\n"


def _passes(metrics: dict[str, Any], thresholds: dict[str, Any]) -> bool:
    return (
        metrics["quality"]["diagnosis_accuracy"] >= thresholds["diagnosis_accuracy_min"]
        and metrics["functional"]["fix_success_rate"] >= thresholds["fix_success_rate_min"]
        and metrics["performance"]["avg_latency_seconds"] <= thresholds["avg_latency_seconds_max"]
        and metrics["cost_ops"]["max_cost_per_run_usd"] <= thresholds["max_cost_per_run_usd"]
        and metrics["functional"]["evaluated_runs"] >= thresholds["evaluated_runs_min"]
    )


def _ratio(values) -> float:
    items = list(values)
    return sum(1 for item in items if item) / len(items)


def _avg(values) -> float:
    items = list(values)
    return sum(items) / len(items)


def _positive_score(value: float, threshold: float) -> float:
    if threshold <= 0:
        return 100.0
    return round(min(value / threshold, 1.0) * 100, 3)


def _inverse_threshold_score(value: float, threshold: float) -> float:
    if threshold <= 0:
        return 0.0
    if value <= threshold:
        return 100.0
    return round(max(0.0, (2 * threshold - value) / threshold) * 100, 3)


def _weighted(score: float, weight: float) -> dict[str, float]:
    return {
        "raw_score": round(score, 3),
        "weight": weight,
        "weighted_points": round(score * weight, 3),
    }
