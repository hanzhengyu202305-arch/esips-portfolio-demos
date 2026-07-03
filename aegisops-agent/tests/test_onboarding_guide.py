from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_newcomer_guide_exists_and_covers_beginner_path() -> None:
    guide = PROJECT_ROOT / "docs" / "NEWCOMER_GUIDE.zh-CN.md"
    text = guide.read_text(encoding="utf-8")

    required_sections = [
        "# AegisOps Agent 新手入门必读",
        "## 先理解这个项目在干什么",
        "## 5 分钟跑通路线",
        "## 你应该看哪些输出",
        "## 新手不要先碰什么",
        "## 面试时怎么讲",
        "## 常见报错",
    ]
    for section in required_sections:
        assert section in text

    for command in [
        "make doctor",
        "make test",
        "make demo SCENARIO=S4 MODE=multi",
        "make eval-mock",
        "make report",
    ]:
        assert command in text


def test_readme_links_to_newcomer_guide_and_quickstart() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    makefile = (PROJECT_ROOT / "Makefile").read_text(encoding="utf-8")

    assert "docs/NEWCOMER_GUIDE.zh-CN.md" in readme
    assert "make quickstart" in readme
    assert "issue-to-pr-report.md" in readme
    assert "quickstart:" in makefile
    assert "issue-to-pr-report:" in makefile


def test_issue_to_pr_fixture_and_walkthrough_are_reviewable() -> None:
    issue = PROJECT_ROOT / "fixtures" / "issues" / "S4_crashloopbackoff_issue.md"
    walkthrough = PROJECT_ROOT / "docs" / "incident-to-pr-walkthrough.md"

    issue_text = issue.read_text(encoding="utf-8")
    walkthrough_text = walkthrough.read_text(encoding="utf-8")

    assert "CrashLoopBackOff" in issue_text
    assert "invalid APP_MODE" in issue_text
    assert "invalid_app_mode_env" in walkthrough_text
    assert "reports/S4/multi/pr-summary.md" in walkthrough_text
    assert "allowed_files" in walkthrough_text
