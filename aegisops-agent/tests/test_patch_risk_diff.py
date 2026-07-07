from __future__ import annotations

from pathlib import Path

from agent.patch_risk_diff import (
    analyze_patch_risk,
    build_patch_review_queue,
    render_patch_review_queue,
    render_patch_risk_report,
    write_patch_review_queue,
    write_patch_risk_report,
)
from agent.scenarios import ScenarioSpec


def test_patch_risk_diff_flags_s4_kubernetes_review_items() -> None:
    report = analyze_patch_risk("S4")

    assert report.scenario_id == "S4"
    assert report.overall_status == "REVIEW"
    assert report.recommended_owner == "platform reviewer"
    assert report.files_changed == ["k8s/overlays/broken-env/deployment.yaml"]
    assert any(finding.status == "PASS" and "scenario allowlist" in finding.message for finding in report.findings)
    assert any(finding.status == "REVIEW" and "image tag still uses latest" in finding.message for finding in report.findings)
    assert any(finding.status == "REVIEW" and "Kubernetes dry-run validation" in finding.message for finding in report.findings)


def test_patch_risk_diff_recognizes_security_hardening_patch() -> None:
    report = analyze_patch_risk("S7")

    assert report.scenario_id == "S7"
    assert report.recommended_owner == "platform/security reviewer"
    assert any("runAsNonRoot" in finding.message for finding in report.findings)
    assert any("allowPrivilegeEscalation=false" in finding.message for finding in report.findings)
    assert all("blocked patch target" not in finding.message for finding in report.findings)


def test_patch_risk_diff_marks_blocking_findings_as_fail(monkeypatch) -> None:
    scenario = ScenarioSpec(
        scenario_id="SX",
        slug="blocked_patch",
        title="Blocked patch target",
        category="ci",
        root_cause_id="blocked_patch_target",
        failure_summary="Patch tries to edit a blocked target.",
        raw_log="blocked target",
        evidence_signals=[],
        allowed_files=["safe/*"],
        blocked_files=["blocked/*"],
        validation_kind="ci-dry-run",
        runbook_query="blocked target",
        broken_files={},
        fixed_files={"blocked/config.yml": "value: unsafe\n"},
        manual_debug_minutes=5,
        human_review_minutes=2,
    )
    monkeypatch.setattr("agent.patch_risk_diff.get_scenario", lambda scenario_id: scenario)

    report = analyze_patch_risk("SX")

    assert report.overall_status == "FAIL"
    assert any(finding.status == "FAIL" for finding in report.findings)


def test_patch_risk_report_markdown_is_reviewer_readable() -> None:
    markdown = render_patch_risk_report(analyze_patch_risk("S4"))

    assert markdown.startswith("# Patch Risk Diff")
    assert "| status | area | message |" in markdown
    assert "k8s/overlays/broken-env/deployment.yaml" in markdown
    assert "Human review required before merge or deployment." in markdown


def test_write_patch_risk_report_writes_under_scenario_mode(tmp_path: Path) -> None:
    output_path = write_patch_risk_report(tmp_path, "S4", mode="multi")

    assert output_path == tmp_path / "S4" / "multi" / "patch-risk-diff.md"
    assert output_path.is_file()
    assert "Patch Risk Diff" in output_path.read_text(encoding="utf-8")


def test_build_patch_review_queue_prioritizes_security_and_kubernetes_patch_reviews() -> None:
    queue = build_patch_review_queue(["S3", "S4", "S7", "S8"])

    assert [item.scenario_id for item in queue] == ["S7", "S4", "S8", "S3"]
    assert queue[0].recommended_owner == "platform/security reviewer"
    assert queue[0].overall_status == "REVIEW"
    assert queue[0].risk_score > queue[-1].risk_score
    assert queue[0].blocking_count == 0
    assert queue[0].review_count >= 1
    assert queue[0].pass_count >= 2
    assert "security reviewer" in queue[0].next_action.lower()


def test_render_patch_review_queue_is_reviewer_readable() -> None:
    markdown = render_patch_review_queue(build_patch_review_queue(["S3", "S4", "S7", "S8"]))

    assert markdown.startswith("# AegisOps Patch Review Queue")
    assert "| rank | scenario | status | owner | risk_score | blocking | review | pass | next_action | report |" in markdown
    assert "| 1 | S7 | REVIEW | platform/security reviewer |" in markdown
    assert "reports/S4/multi/patch-risk-diff.md" in markdown
    assert "not a production security scanner" in markdown


def test_write_patch_review_queue_writes_markdown(tmp_path: Path) -> None:
    output_path = write_patch_review_queue(tmp_path / "patch-review-queue.md", scenario_ids=["S3", "S4"])

    assert output_path == tmp_path / "patch-review-queue.md"
    text = output_path.read_text(encoding="utf-8")
    assert "AegisOps Patch Review Queue" in text
    assert "reports/S4/multi/patch-risk-diff.md" in text
