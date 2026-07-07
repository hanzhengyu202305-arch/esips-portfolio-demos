from __future__ import annotations

import json
from pathlib import Path

from agent.diagnostics import run_doctor
from agent.evaluation.evaluator import run_eval
from agent.reporting import create_final_report, create_scenario_matrix


def test_scenario_matrix_documents_all_scenarios(tmp_path: Path) -> None:
    matrix_path = create_scenario_matrix(tmp_path / "scenario-matrix.md")
    text = matrix_path.read_text(encoding="utf-8")

    assert "| S1 | pytest | wrong_discount_logic |" in text
    assert "| S4 | kubernetes | invalid_app_mode_env |" in text
    assert "| S7 | security | container_runs_as_root |" in text
    assert text.count("| S") >= 8


def test_eval_summary_includes_per_scenario_results(tmp_path: Path) -> None:
    summary_path = run_eval(reports_dir=tmp_path, scenarios=["S1", "S4"])
    summary = summary_path.read_text(encoding="utf-8")

    assert "## Per-Scenario Results" in summary
    assert "| S1 | single | wrong_discount_logic | true | true |" in summary
    assert "| S4 | multi | invalid_app_mode_env | true | true |" in summary
    assert "## Architecture Comparison" in summary


def test_doctor_writes_nonblocking_environment_report(tmp_path: Path) -> None:
    doctor_path = run_doctor(reports_dir=tmp_path)
    payload = json.loads(doctor_path.read_text(encoding="utf-8"))

    assert payload["project"] == "aegisops-agent"
    assert payload["python_version"]
    assert payload["checks"]["project_root"]["ok"] is True
    assert "docker" in payload["checks"]
    assert "kind" in payload["checks"]


def test_final_report_has_single_top_level_heading(tmp_path: Path) -> None:
    run_eval(reports_dir=tmp_path, scenarios=["S1"])
    report_path = create_final_report(reports_dir=tmp_path)
    report = report_path.read_text(encoding="utf-8")

    assert report.count("\n# ") == 0
    assert report.startswith("# AegisOps Agent Final Portfolio Report\n")
    assert "## AegisOps Evaluation Summary" in report
    assert "reports/S4/multi/pr-summary.md" in report
    assert "## Evaluation\n\n## AegisOps Evaluation Summary" not in report


def test_final_report_writes_and_links_triage_queue(tmp_path: Path) -> None:
    run_eval(reports_dir=tmp_path, scenarios=["S1"])
    report_path = create_final_report(reports_dir=tmp_path)
    report = report_path.read_text(encoding="utf-8")
    triage_path = tmp_path / "triage-queue.md"

    assert triage_path.exists()
    assert "reports/triage-queue.md" in report
    assert "AegisOps Triage Queue" in triage_path.read_text(encoding="utf-8")


def test_final_report_links_patch_risk_diff(tmp_path: Path) -> None:
    run_eval(reports_dir=tmp_path, scenarios=["S1"])
    report_path = create_final_report(reports_dir=tmp_path)
    report = report_path.read_text(encoding="utf-8")

    assert "reports/S4/multi/patch-risk-diff.md" in report
