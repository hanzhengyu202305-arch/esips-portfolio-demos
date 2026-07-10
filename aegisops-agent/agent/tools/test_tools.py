from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from agent.scenarios import get_scenario


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    log_path: Path
    commands_run: list[str]


def run_validation(
    scenario_id: str,
    mode: str = "single",
    reports_dir: Path | str = Path("reports"),
    patched_dir: Path | None = None,
) -> ValidationResult:
    scenario = get_scenario(scenario_id)
    run_dir = Path(reports_dir) / scenario.scenario_id / mode
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "validation.log"

    commands = [
        [sys.executable, "-m", "pytest", "apps/demo-api/tests", "-q"],
        [sys.executable, "scripts/lint.py"],
        [
            sys.executable,
            "scripts/devops_check.py",
            "--scenario",
            scenario.scenario_id,
            "--patched-dir",
            str(patched_dir or run_dir / "patched"),
        ],
    ]

    outputs: list[str] = []
    commands_run: list[str] = []
    passed = True
    for command in commands:
        display_command = _display_command(command)
        commands_run.append(display_command)
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        outputs.append(f"$ {display_command}")
        outputs.append(_stable_output(completed.stdout))
        outputs.append(_stable_output(completed.stderr))
        if completed.returncode != 0:
            passed = False

    log_path.write_text("\n".join(outputs), encoding="utf-8")
    return ValidationResult(passed=passed, log_path=log_path, commands_run=commands_run)


def _stable_output(output: str) -> str:
    if os.environ.get("AEGISOPS_STABLE_REPORTS") != "1":
        return output
    return re.sub(r"(\d+) passed in \d+\.\d+s", r"\1 passed in <stable>s", output)


def _display_command(command: list[str]) -> str:
    display = list(command)
    if os.environ.get("AEGISOPS_STABLE_REPORTS") == "1" and display:
        display[0] = "python3"
    return " ".join(display)
