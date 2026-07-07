from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.scenarios import ScenarioSpec, get_scenario, list_scenarios


@dataclass(frozen=True)
class TriageItem:
    scenario_id: str
    title: str
    category: str
    severity: str
    priority_score: int
    recommended_owner: str
    next_action: str
    evidence_refs: list[str]


SEVERITY_POINTS = {
    "high": 100,
    "medium": 60,
    "low": 20,
}

CATEGORY_POINTS = {
    "security": 12,
    "kubernetes": 8,
    "latency": 4,
    "ci": 2,
    "docker": 2,
    "pytest": 1,
}

OWNER_BY_CATEGORY = {
    "security": "platform/security reviewer",
    "kubernetes": "platform reviewer",
    "latency": "application performance reviewer",
    "ci": "devex reviewer",
    "docker": "platform reviewer",
    "pytest": "application reviewer",
}


def build_triage_queue(scenario_ids: list[str] | None = None) -> list[TriageItem]:
    scenarios = [get_scenario(scenario_id) for scenario_id in scenario_ids] if scenario_ids else list_scenarios()
    items = [_triage_item(scenario) for scenario in scenarios]
    return sorted(items, key=lambda item: (-item.priority_score, item.scenario_id))


def render_triage_report(queue: list[TriageItem]) -> str:
    lines = [
        "# AegisOps Triage Queue",
        "",
        "This report ranks synthetic incidents before remediation so the reviewer can inspect severity, evidence, ownership, and next action before any patch preview.",
        "",
        "| rank | scenario | severity | category | priority_score | owner | next_action | evidence |",
        "| ---: | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for rank, item in enumerate(queue, start=1):
        evidence = "<br>".join(f"`{ref}`" for ref in item.evidence_refs)
        lines.append(
            f"| {rank} | {item.scenario_id} | {item.severity} | {item.category} | "
            f"{item.priority_score} | {item.recommended_owner} | {item.next_action} | {evidence} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Human review remains required before patching or deployment.",
            "The queue uses synthetic fixtures and deterministic scoring; it is not an incident-management system.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_triage_report(
    output_path: Path | str = Path("reports/triage-queue.md"),
    scenario_ids: list[str] | None = None,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_triage_report(build_triage_queue(scenario_ids)), encoding="utf-8")
    return path


def _triage_item(scenario: ScenarioSpec) -> TriageItem:
    severity = _highest_severity(scenario)
    priority_score = _priority_score(scenario, severity)
    return TriageItem(
        scenario_id=scenario.scenario_id,
        title=scenario.title,
        category=scenario.category,
        severity=severity,
        priority_score=priority_score,
        recommended_owner=OWNER_BY_CATEGORY.get(scenario.category, "engineering reviewer"),
        next_action=_next_action(scenario),
        evidence_refs=[signal["id"] for signal in scenario.evidence_signals],
    )


def _highest_severity(scenario: ScenarioSpec) -> str:
    severities = [str(signal.get("severity", "low")).lower() for signal in scenario.evidence_signals]
    return max(severities, key=lambda severity: SEVERITY_POINTS.get(severity, 0))


def _priority_score(scenario: ScenarioSpec, severity: str) -> int:
    manual_savings = max(0, scenario.manual_debug_minutes - scenario.human_review_minutes)
    return (
        SEVERITY_POINTS.get(severity, 0)
        + CATEGORY_POINTS.get(scenario.category, 0)
        + manual_savings
    )


def _next_action(scenario: ScenarioSpec) -> str:
    if scenario.category == "security":
        return "Review securityContext patch, then run security dry-run validation."
    if scenario.category == "kubernetes":
        return f"Review {scenario.root_cause_id}, then run Kubernetes dry-run validation."
    if scenario.category == "latency":
        return "Review latency evidence, then run benchmark dry-run validation."
    if scenario.category == "ci":
        return "Review CI environment variables, then run CI dry-run validation."
    if scenario.category == "docker":
        return "Review image dependency evidence, then run Docker dry-run validation."
    return "Review application patch and run pytest validation."
