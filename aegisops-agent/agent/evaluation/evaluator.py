from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from agent.graph.multi_agent import run_multi_agent
from agent.graph.single_agent import run_single_agent
from agent.scenarios import get_scenario, list_scenarios


def run_eval(
    reports_dir: Path | str = Path("reports"),
    scenarios: list[str] | None = None,
) -> Path:
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    scenario_ids = scenarios or [scenario.scenario_id for scenario in list_scenarios()]
    results = []
    for scenario_id in scenario_ids:
        for runner in (run_single_agent, run_multi_agent):
            result = runner(scenario_id, reports_dir=reports_path)
            results.append(result.metrics.to_dict())

    results_path = reports_path / "eval-results.json"
    results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    summary_path = reports_path / "eval-summary.md"
    summary_path.write_text(_render_summary(results), encoding="utf-8")
    return summary_path


def _render_summary(results: list[dict]) -> str:
    by_mode: dict[str, list[dict]] = defaultdict(list)
    for result in results:
        by_mode[result["mode"]].append(result)

    lines = [
        "# AegisOps Evaluation Summary",
        "",
        "| mode | diagnosis_accuracy | fix_success_rate | avg_latency_seconds | estimated_cost_usd | tool_calls |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for mode in sorted(by_mode):
        items = by_mode[mode]
        count = len(items)
        accuracy = sum(1 for item in items if item["root_cause_correct"]) / count
        fix_rate = sum(1 for item in items if item["fix_successful"]) / count
        avg_latency = sum(item["latency_seconds"] for item in items) / count
        cost = sum(item["estimated_cost_usd"] for item in items)
        tool_calls = sum(item["tool_calls"] for item in items)
        lines.append(
            f"| {mode} | {accuracy:.2f} | {fix_rate:.2f} | {avg_latency:.3f} | {cost:.6f} | {tool_calls} |"
        )

    lines.extend(
        [
            "",
            "## Per-Scenario Results",
            "",
            "| scenario | mode | root_cause_id | root_cause_correct | fix_successful | latency_seconds | estimated_cost_usd |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for result in sorted(results, key=lambda item: (item["scenario_id"], item["mode"])):
        root_cause_id = get_scenario(result["scenario_id"]).root_cause_id
        lines.append(
            f"| {result['scenario_id']} | {result['mode']} | {root_cause_id} | "
            f"{str(result['root_cause_correct']).lower()} | "
            f"{str(result['fix_successful']).lower()} | "
            f"{result['latency_seconds']:.3f} | {result['estimated_cost_usd']:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Architecture Comparison",
            "",
            "Single-agent mode is the cheaper baseline. Multi-agent mode uses the same tools but adds explicit triage, RCA, fix, and review stages for auditability.",
            "",
            "## Metrics",
            "",
            "- `diagnosis_accuracy`: fraction of runs where `root_cause_id` matched the gold label.",
            "- `fix_success_rate`: fraction of runs with a safe patch preview and passing validation.",
            "- `estimated_cost_usd`: deterministic proxy using MockLLM token estimates.",
            "- `tool_calls`: comparable proxy for orchestration complexity.",
        ]
    )
    return "\n".join(lines) + "\n"
