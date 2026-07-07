from __future__ import annotations

import json
from pathlib import Path

from agent.evaluation.evaluator import run_eval
from agent.scenarios import list_scenarios
from agent.triage_queue import write_triage_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def create_scenario_matrix(output_path: Path | str = Path("reports/scenario-matrix.md")) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# AegisOps Scenario Matrix",
        "",
        "| scenario | category | root_cause_id | allowed_files | validation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for scenario in list_scenarios():
        allowed = "<br>".join(f"`{item}`" for item in scenario.allowed_files)
        lines.append(
            f"| {scenario.scenario_id} | {scenario.category} | {scenario.root_cause_id} | "
            f"{allowed} | {scenario.validation_kind} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def create_final_report(reports_dir: Path | str = Path("reports")) -> Path:
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)
    eval_summary = reports_path / "eval-summary.md"
    eval_results_path = reports_path / "eval-results.json"
    if not eval_summary.exists() or not eval_results_path.exists():
        run_eval(reports_path)
    scenario_matrix = create_scenario_matrix(reports_path / "scenario-matrix.md")
    issue_to_pr_report = create_issue_to_pr_report(reports_path)
    triage_queue = write_triage_report(reports_path / "triage-queue.md")

    scenarios = list_scenarios()
    eval_results = json.loads(eval_results_path.read_text(encoding="utf-8"))
    expected_multi = {scenario.scenario_id for scenario in scenarios}
    observed_multi = {
        item["scenario_id"] for item in eval_results if item.get("mode") == "multi"
    }
    if observed_multi != expected_multi:
        run_eval(reports_path)
        eval_results = json.loads(eval_results_path.read_text(encoding="utf-8"))

    value_lines = []
    for scenario in scenarios:
        multi = next(
            item
            for item in eval_results
            if item["scenario_id"] == scenario.scenario_id and item["mode"] == "multi"
        )
        engineer_rate = 80
        value_saved = (
            (scenario.manual_debug_minutes - scenario.human_review_minutes)
            / 60
            * engineer_rate
            * (1 if multi["fix_successful"] else 0)
        )
        net_value = value_saved - multi["estimated_cost_usd"]
        value_lines.append(
            f"| {scenario.scenario_id} | {scenario.root_cause_id} | {scenario.manual_debug_minutes} | "
            f"{scenario.human_review_minutes} | {multi['estimated_cost_usd']:.6f} | {net_value:.2f} |"
        )

    report = [
        "# AegisOps Agent Final Portfolio Report",
        "",
        "AegisOps Agent is a reproducible agentic DevOps lab for root-cause analysis and patch remediation across CI/CD, Docker, Kubernetes, security, and latency incidents.",
        "",
        "## Portfolio Positioning",
        "",
        "This project is built for AI/software industry-placement interviews where the goal is to show more than a standalone chatbot. AegisOps puts an LLM-style agent inside a controlled engineering workflow: evidence collection, runbook retrieval, root-cause analysis, patch preview generation, validation, and metric reporting.",
        "",
        "Primary ESIPS fit: `Accenture_02 SDLC_Agents.pdf`.",
        "",
        "Secondary ESIPS fit: `Accenture_01 Kubernetes_DevOps.pdf`, `Accenture_03 AgentMemory.pdf`, `Accenture_04 SustainableGenAI.pdf`, and `Accenture_05 SingleVMultiAgent.pdf`.",
        "",
        "## Demo Path",
        "",
        "```bash",
        "make test",
        "make demo SCENARIO=S4 MODE=multi",
        "make eval-mock",
        "make report",
        "```",
        "",
        "Key demo artifacts:",
        "",
        "- `reports/S4/multi/demo-report.md`",
        "- `reports/S4/multi/issue-to-pr-report.md`",
        "- `reports/S4/multi/pr-summary.md`",
        "- `reports/S4/multi/patch-risk-diff.md`",
        "- `reports/S4/multi/patch.diff`",
        "- `reports/S4/multi/validation.log`",
        "- `reports/eval-summary.md`",
        "",
        _demote_markdown_headings(eval_summary.read_text(encoding="utf-8")),
        "",
        "## Technical Differentiators",
        "",
        "- Deterministic local demo: runs with `MockLLM`, so reviewers can reproduce it without API keys.",
        "- Agentic workflow: evidence -> retrieval -> diagnosis -> patch preview -> validation -> metrics.",
        "- Safety guardrails: the agent cannot patch CI workflows, tests, or gold labels.",
        "- Architecture comparison: single-agent and multi-agent modes run against the same scenarios.",
        "- Engineering metrics: accuracy, fix success, latency, cost proxy, tool calls, and ROI proxy are reported.",
        "",
        "## ROI Proxy",
        "",
        "| scenario | root_cause_id | manual_debug_minutes | human_review_minutes | estimated_cost_usd | net_value_usd |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
        *value_lines,
        "",
        "## Deliverables",
        "",
        "- GitHub-ready repository scaffold",
        "- Incident triage queue with deterministic priority scoring",
        "- FastAPI demo service",
        "- 8 reproducible failure scenarios",
        "- RAG runbooks and incident memory",
        "- Single-agent and multi-agent workflows",
        "- Patch safety guardrails",
        "- Patch risk diff report before human review",
        "- Deterministic MockLLM evaluation",
        "- Accenture/ESIPS application narrative",
        "",
        "## Supporting Artifacts",
        "",
        "- Newcomer guide: `docs/NEWCOMER_GUIDE.zh-CN.md`",
        f"- Scenario matrix: `{scenario_matrix}`",
        f"- Triage queue: `reports/triage-queue.md` (generated at `{triage_queue}`)",
        "- Evaluation summary: `reports/eval-summary.md`",
        "- Demo script: `docs/demo-script.md`",
        "- ESIPS mapping: `docs/esips-accenture-mapping.md`",
        "- Application pack: `docs/application-pack.md`",
        "- Acceptance checklist: `reports/acceptance-checklist.md`",
        f"- S4 issue-to-PR report: `{issue_to_pr_report}`",
    ]
    final_path = reports_path / "final-portfolio-report.md"
    final_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    return final_path


def create_issue_to_pr_report(reports_dir: Path | str = Path("reports")) -> Path:
    reports_path = Path(reports_dir)
    output_path = reports_path / "S4" / "multi" / "issue-to-pr-report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    issue_path = PROJECT_ROOT / "fixtures" / "issues" / "S4_crashloopbackoff_issue.md"
    issue_excerpt = issue_path.read_text(encoding="utf-8").split("## Reviewer Boundary")[0].strip()
    lines = [
        "# S4 Issue-To-PR Report",
        "",
        "## Source Issue Fixture",
        "",
        issue_excerpt,
        "",
        "## Workflow Evidence",
        "",
        "| step | artifact | reviewer check |",
        "| --- | --- | --- |",
        "| issue / failing symptom | `fixtures/issues/S4_crashloopbackoff_issue.md` | GitHub-style issue fixture describes expected and observed behavior. |",
        "| evidence collection | `reports/S4/evidence.json` | Failure evidence is structured before diagnosis. |",
        "| runbook retrieval | `reports/S4/multi/diagnosis.json` | Retrieved context includes Kubernetes CrashLoopBackOff runbooks. |",
        "| root-cause diagnosis | `reports/S4/multi/diagnosis.json` | Expected root cause is `invalid_app_mode_env`. |",
        "| guarded patch preview | `reports/S4/multi/patch.diff` | Patch changes only the scenario allowlisted deployment file. |",
        "| validation | `reports/S4/multi/validation.log` | Tests, lint, and DevOps dry-run validation are recorded. |",
        "| PR summary | `reports/S4/multi/pr-summary.md` | Human reviewer gets incident, root cause, files changed, validation, and risk notes. |",
        "",
        "## Expected Root Cause",
        "",
        "`invalid_app_mode_env`",
        "",
        "## Boundary",
        "",
        "This report does not create a real pull request and does not require a GitHub token or live cluster. It is a deterministic portfolio artifact that shows how the AegisOps workflow can turn a failure issue into a human-reviewable patch preview.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def _demote_markdown_headings(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        if line.startswith("#"):
            lines.append("#" + line)
        else:
            lines.append(line)
    return "\n".join(lines)
