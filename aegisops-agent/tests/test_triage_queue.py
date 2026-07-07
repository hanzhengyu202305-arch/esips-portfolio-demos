from __future__ import annotations

from pathlib import Path

from agent.triage_queue import build_triage_queue, render_triage_report, write_triage_report


def test_build_triage_queue_prioritizes_high_severity_security_and_kubernetes_work() -> None:
    queue = build_triage_queue(["S3", "S4", "S7", "S8"])

    assert [item.scenario_id for item in queue] == ["S7", "S4", "S8", "S3"]
    assert queue[0].category == "security"
    assert queue[0].severity == "high"
    assert queue[0].recommended_owner == "platform/security reviewer"
    assert queue[0].priority_score > queue[-1].priority_score
    assert "securityContext" in queue[0].next_action


def test_render_triage_report_is_reviewer_readable() -> None:
    markdown = render_triage_report(build_triage_queue(["S3", "S4", "S7", "S8"]))

    assert markdown.startswith("# AegisOps Triage Queue")
    assert "| rank | scenario | severity | category | priority_score | owner | next_action | evidence |" in markdown
    assert "| 1 | S7 | high | security |" in markdown
    assert "platform/security reviewer" in markdown
    assert "k8s:S4:invalid-env" in markdown
    assert "Human review remains required before patching or deployment." in markdown


def test_write_triage_report_writes_markdown(tmp_path: Path) -> None:
    output_path = write_triage_report(tmp_path / "triage-queue.md", scenario_ids=["S3", "S4", "S7", "S8"])

    assert output_path == tmp_path / "triage-queue.md"
    text = output_path.read_text(encoding="utf-8")
    assert "AegisOps Triage Queue" in text
    assert "S7" in text
