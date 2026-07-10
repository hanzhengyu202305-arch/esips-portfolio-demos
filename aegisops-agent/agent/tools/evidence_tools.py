from __future__ import annotations

import json
from pathlib import Path

from agent.scenario_runner import run_scenario
from agent.scenarios import get_scenario


def collect_evidence(
    scenario_id: str,
    reports_dir: Path | str = Path("reports"),
) -> Path:
    scenario = get_scenario(scenario_id)
    reports_path = Path(reports_dir)
    run_scenario(scenario.scenario_id, reports_path)
    scenario_dir = reports_path / scenario.scenario_id
    payload = {
        "scenario_id": scenario.scenario_id,
        "title": scenario.title,
        "category": scenario.category,
        "failure_summary": scenario.failure_summary,
        "raw_log": scenario.raw_log,
        "signals": scenario.evidence_signals,
        "artifacts": [str(scenario_dir / "raw_failure.log")],
    }
    evidence_path = scenario_dir / "evidence.json"
    evidence_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return evidence_path
