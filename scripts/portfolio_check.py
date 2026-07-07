from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class CheckResult:
    name: str
    command: list[str]
    passed: bool
    returncode: int
    output_tail: str


def main() -> int:
    parser = argparse.ArgumentParser(description="Run portfolio validation and write status artifacts.")
    parser.add_argument("--aegisops-python", default=os.environ.get("AEGISOPS_PY", "/opt/anaconda3/bin/python3.13"))
    args = parser.parse_args()

    env = os.environ.copy()
    env["AEGISOPS_STABLE_REPORTS"] = "1"
    commands = [
        ("top-level tests", ["make", "test", f"AEGISOPS_PY={args.aegisops_python}"]),
        ("AegisOps acceptance", ["make", "-C", "aegisops-agent", "acceptance", f"PYTHON={args.aegisops_python}"]),
        (
            "AegisOps patch review queue",
            ["make", "-C", "aegisops-agent", "patch-review-queue", f"PYTHON={args.aegisops_python}"],
        ),
        ("Kube Copilot report", ["make", "-C", "kube-copilot", "report"]),
        ("Kube Policy Pack", ["make", "-C", "kube-copilot", "policy-pack"]),
        ("Haul Truck Planner report", ["make", "-C", "haul-truck-planner", "report"]),
        ("EvidenceOps scorecard", ["make", "-C", "evidenceops-scorecard", "report"]),
        ("public boundary check", [sys.executable, "scripts/public_boundary_check.py"]),
    ]

    results = [run_check(name, command, env=env) for name, command in commands]
    preliminary_passed = all(result.passed for result in results)
    write_status(results, preliminary_passed)
    results.append(
        run_check(
            "EvidenceOps release gate",
            ["make", "-C", "evidenceops-scorecard", "release-gate"],
            env=env,
        )
    )
    overall_passed = all(result.passed for result in results)
    write_status(results, overall_passed)
    print("PASS portfolio-check" if overall_passed else "FAIL portfolio-check")
    return 0 if overall_passed else 1


def run_check(name: str, command: list[str], env: dict[str, str] | None = None) -> CheckResult:
    print(f"==> {name}: {' '.join(command)}")
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    output = completed.stdout or ""
    if output:
        print(output)
    return CheckResult(
        name=name,
        command=command,
        passed=completed.returncode == 0,
        returncode=completed.returncode,
        output_tail=tail(output),
    )


def tail(output: str, max_lines: int = 12) -> str:
    lines = output.strip().splitlines()
    return "\n".join(lines[-max_lines:])


def write_status(results: list[CheckResult], overall_passed: bool) -> None:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "overall_portfolio_status": "PASS" if overall_passed else "FAIL",
        "generated_at_utc": generated_at,
        "checks": [
            {
                "name": result.name,
                "status": "PASS" if result.passed else "FAIL",
                "returncode": result.returncode,
                "command": result.command,
                "output_tail": result.output_tail,
            }
            for result in results
        ],
    }
    (ROOT / "PORTFOLIO_STATUS.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (ROOT / "PORTFOLIO_STATUS.md").write_text(status_markdown(payload), encoding="utf-8")


def status_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Portfolio Status",
        "",
        f"Overall status: **{payload['overall_portfolio_status']}**",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "| check | status | command |",
        "| --- | --- | --- |",
    ]
    for check in payload["checks"]:
        command = " ".join(check["command"])
        lines.append(f"| {check['name']} | {check['status']} | `{command}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This status file is generated from local deterministic checks. It does not prove production readiness and does not include private application material.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
