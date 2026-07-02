from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from agent.diagnostics import render_doctor_markdown, run_doctor
from agent.evaluation.evaluator import run_eval
from agent.graph.multi_agent import run_multi_agent
from agent.poc import create_scorecard
from agent.reporting import create_final_report, create_scenario_matrix
from agent.scenarios import list_scenarios


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AcceptanceResult:
    passed: bool
    markdown_path: Path
    json_path: Path
    checked_items: int
    failed_items: int


def run_acceptance(
    reports_dir: Path | str = Path("reports"),
    refresh: bool = True,
) -> AcceptanceResult:
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    if refresh:
        doctor_json = run_doctor(reports_path)
        render_doctor_markdown(doctor_json)
        create_scenario_matrix(reports_path / "scenario-matrix.md")
        run_multi_agent("S4", reports_dir=reports_path)
        run_eval(reports_dir=reports_path)
        create_scorecard(reports_path, PROJECT_ROOT / "config" / "poc-scorecard.json")
        create_final_report(reports_dir=reports_path)

    checks = _build_checks(reports_path)
    failed = [check for check in checks if not check["ok"]]
    passed = not failed

    json_path = reports_path / "acceptance-checklist.json"
    markdown_path = reports_path / "acceptance-checklist.md"
    payload = {
        "passed": passed,
        "checked_items": len(checks),
        "failed_items": len(failed),
        "checks": checks,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    markdown_path.write_text(_render_acceptance_markdown(payload), encoding="utf-8")
    return AcceptanceResult(
        passed=passed,
        markdown_path=markdown_path,
        json_path=json_path,
        checked_items=len(checks),
        failed_items=len(failed),
    )


def _build_checks(reports_path: Path) -> list[dict]:
    checks = [
        _file_check("README.md", PROJECT_ROOT / "README.md", "main project entrypoint"),
        _file_check("SPEC.md", PROJECT_ROOT / "SPEC.md", "scope and definition of done"),
        _file_check(
            "SOW contract",
            PROJECT_ROOT / "SOW.md",
            "scope, milestones, pass/fail thresholds, weights, and rubric",
        ),
        _file_check(
            "Data Card",
            PROJECT_ROOT / "DATACARD.md",
            "synthetic data provenance and compliance boundary",
        ),
        _file_check(
            "Operations manual",
            PROJECT_ROOT / "OPERATIONS.md",
            "setup, demo, CI/CD, Kubernetes checks, and release runbook",
        ),
        _file_check(
            "PR template",
            PROJECT_ROOT / ".github" / "pull_request_template.md",
            "review checklist tied to SOW evidence",
        ),
        _file_check(
            "PoC validation guide",
            PROJECT_ROOT / "POC_VALIDATION.md",
            "functional, performance, quality, and cost/ops review guide",
        ),
        _file_check(
            "PoC scorecard config",
            PROJECT_ROOT / "config" / "poc-scorecard.json",
            "explicit PoC thresholds and weights",
        ),
        _file_check(
            "newcomer guide",
            PROJECT_ROOT / "docs" / "NEWCOMER_GUIDE.zh-CN.md",
            "beginner onboarding path",
        ),
        _file_check(
            "demo script",
            PROJECT_ROOT / "docs" / "demo-script.md",
            "5-minute reviewer walkthrough",
        ),
        _file_check(
            "ESIPS mapping",
            PROJECT_ROOT / "docs" / "esips-accenture-mapping.md",
            "industry-placement positioning",
        ),
        _file_check(
            "scenario matrix",
            reports_path / "scenario-matrix.md",
            "scenario coverage table",
        ),
        _file_check("doctor report", reports_path / "doctor.md", "local environment readiness"),
        _file_check(
            "PoC scorecard",
            reports_path / "scorecard.txt",
            "weighted PoC PASS/FAIL result",
        ),
        _file_check(
            "PoC metrics",
            reports_path / "poc-metrics.json",
            "normalized PoC metrics and scoring breakdown",
        ),
        _json_bool_check(
            "S4 multi diagnosis",
            reports_path / "S4" / "multi" / "diagnosis.json",
            ["root_cause_id"],
            "invalid_app_mode_env",
        ),
        _json_bool_check(
            "S4 multi demo validation",
            reports_path / "S4" / "multi" / "metrics.json",
            ["fix_successful"],
            True,
        ),
        _file_check(
            "S4 patch diff",
            reports_path / "S4" / "multi" / "patch.diff",
            "reviewable remediation patch preview",
        ),
        _file_check(
            "S4 PR summary",
            reports_path / "S4" / "multi" / "pr-summary.md",
            "human-reviewable remediation handoff",
        ),
        _eval_coverage_check(reports_path / "eval-results.json"),
        _file_check(
            "final portfolio report",
            reports_path / "final-portfolio-report.md",
            "reviewer-facing final report",
        ),
    ]
    return checks


def _file_check(name: str, path: Path, detail: str) -> dict:
    ok = path.exists() and path.stat().st_size > 0
    return {
        "name": name,
        "ok": ok,
        "path": _display_path(path),
        "detail": detail if ok else f"missing or empty: {_display_path(path)}",
    }


def _json_bool_check(name: str, path: Path, key_path: list[str], expected: object) -> dict:
    if not path.exists():
        return {
            "name": name,
            "ok": False,
            "path": _display_path(path),
            "detail": f"missing JSON artifact: {_display_path(path)}",
        }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "name": name,
            "ok": False,
            "path": _display_path(path),
            "detail": f"invalid JSON: {exc}",
        }

    value: object = payload
    for key in key_path:
        if not isinstance(value, dict) or key not in value:
            return {
                "name": name,
                "ok": False,
                "path": _display_path(path),
                "detail": f"missing key: {'.'.join(key_path)}",
            }
        value = value[key]
    ok = value == expected
    return {
        "name": name,
        "ok": ok,
        "path": _display_path(path),
        "detail": f"expected {'.'.join(key_path)}={expected!r}, observed {value!r}",
    }


def _eval_coverage_check(path: Path) -> dict:
    if not path.exists():
        return {
            "name": "evaluation coverage",
            "ok": False,
            "path": _display_path(path),
            "detail": "missing eval-results.json",
        }
    results = json.loads(path.read_text(encoding="utf-8"))
    expected = {(scenario.scenario_id, mode) for scenario in list_scenarios() for mode in ("single", "multi")}
    observed = {(item.get("scenario_id"), item.get("mode")) for item in results}
    missing = sorted(expected - observed)
    return {
        "name": "evaluation coverage",
        "ok": not missing,
        "path": _display_path(path),
        "detail": "all scenarios include single and multi results"
        if not missing
        else f"missing results: {missing}",
    }


def _render_acceptance_markdown(payload: dict) -> str:
    status = "PASS" if payload["passed"] else "FAIL"
    lines = [
        "# AegisOps Portfolio Acceptance Checklist",
        "",
        f"Overall status: `{status}`",
        "",
        f"Checked items: `{payload['checked_items']}`",
        f"Failed items: `{payload['failed_items']}`",
        "",
        "| status | item | artifact | detail |",
        "| --- | --- | --- | --- |",
    ]
    for check in payload["checks"]:
        check_status = "PASS" if check["ok"] else "FAIL"
        lines.append(
            f"| {check_status} | {check['name']} | `{check['path']}` | {check['detail']} |"
        )

    lines.extend(
        [
            "",
            "## Next Review Actions",
            "",
            "1. Open `SOW.md` and confirm the scoring thresholds match the latest report.",
            "2. Open `DATACARD.md` and confirm no real or sensitive data was introduced.",
            "3. Open `reports/scorecard.txt` and confirm the PoC score is PASS.",
            "4. Open `reports/S4/multi/patch.diff` and `reports/S4/multi/pr-summary.md` together.",
            "5. Open `reports/final-portfolio-report.md` and rehearse the 30-second interview summary.",
        ]
    )
    return "\n".join(lines) + "\n"


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)
