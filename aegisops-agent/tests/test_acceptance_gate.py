from __future__ import annotations

import json
from pathlib import Path

from agent.acceptance import run_acceptance
from agent.evaluation.evaluator import run_eval
from agent.graph.multi_agent import run_multi_agent
from agent.reporting import create_final_report, create_scenario_matrix


def test_acceptance_gate_passes_when_required_artifacts_exist(tmp_path: Path) -> None:
    run_multi_agent("S4", reports_dir=tmp_path)
    run_eval(reports_dir=tmp_path, scenarios=["S1", "S4"])
    create_scenario_matrix(tmp_path / "scenario-matrix.md")
    create_final_report(reports_dir=tmp_path)

    result = run_acceptance(reports_dir=tmp_path)
    markdown = result.markdown_path.read_text(encoding="utf-8")
    payload = json.loads(result.json_path.read_text(encoding="utf-8"))

    assert result.passed is True
    assert payload["passed"] is True
    assert payload["checked_items"] >= 10
    assert "| PASS | README.md |" in markdown
    assert "| PASS | SOW contract |" in markdown
    assert "| PASS | Data Card |" in markdown
    assert "| PASS | Operations manual |" in markdown
    assert "| PASS | PR template |" in markdown
    assert "| PASS | PoC validation guide |" in markdown
    assert "| PASS | PoC scorecard config |" in markdown
    assert "| PASS | PoC scorecard |" in markdown
    assert "| PASS | PoC metrics |" in markdown
    assert "| PASS | S4 multi demo validation |" in markdown
    assert "| PASS | S4 PR summary |" in markdown
    assert "| PASS | evaluation coverage |" in markdown
    assert "## Next Review Actions" in markdown


def test_acceptance_gate_reports_missing_demo_artifact(tmp_path: Path) -> None:
    result = run_acceptance(reports_dir=tmp_path, refresh=False)
    markdown = result.markdown_path.read_text(encoding="utf-8")

    assert result.passed is False
    assert "| FAIL | S4 multi diagnosis |" in markdown
    assert "| FAIL | final portfolio report |" in markdown
