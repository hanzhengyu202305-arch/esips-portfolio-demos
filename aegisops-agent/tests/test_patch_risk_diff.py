from __future__ import annotations

from pathlib import Path

from agent.patch_risk_diff import analyze_patch_risk, render_patch_risk_report, write_patch_risk_report


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
