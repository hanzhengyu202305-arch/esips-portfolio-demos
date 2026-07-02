from __future__ import annotations

import json
from pathlib import Path

from agent.scenarios import get_scenario


def run_scenario(
    scenario_id: str,
    reports_dir: Path | str = Path("reports"),
) -> Path:
    scenario = get_scenario(scenario_id)
    scenario_dir = Path(reports_dir) / scenario.scenario_id
    scenario_dir.mkdir(parents=True, exist_ok=True)

    raw_log_path = scenario_dir / "raw_failure.log"
    raw_log_path.write_text(scenario.raw_log, encoding="utf-8")

    scenario_path = scenario_dir / "scenario.json"
    scenario_path.write_text(json.dumps(scenario.to_dict(), indent=2), encoding="utf-8")
    return scenario_path
