from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from agent.scenarios import ScenarioSpec, get_scenario, list_scenarios


@dataclass(frozen=True)
class PatchRiskFinding:
    status: str
    area: str
    message: str


@dataclass(frozen=True)
class PatchRiskReport:
    scenario_id: str
    root_cause_id: str
    overall_status: str
    recommended_owner: str
    files_changed: list[str]
    findings: list[PatchRiskFinding]


@dataclass(frozen=True)
class PatchReviewItem:
    scenario_id: str
    root_cause_id: str
    category: str
    overall_status: str
    recommended_owner: str
    risk_score: int
    blocking_count: int
    review_count: int
    pass_count: int
    next_action: str
    report_path: str


OWNER_BY_CATEGORY = {
    "security": "platform/security reviewer",
    "kubernetes": "platform reviewer",
    "latency": "application performance reviewer",
    "ci": "devex reviewer",
    "docker": "platform reviewer",
    "pytest": "application reviewer",
}

CATEGORY_RISK_POINTS = {
    "security": 40,
    "kubernetes": 30,
    "latency": 20,
    "ci": 10,
    "docker": 10,
    "pytest": 5,
}

STATUS_RISK_POINTS = {
    "FAIL": 300,
    "REVIEW": 100,
    "PASS": 0,
}


def analyze_patch_risk(scenario_id: str) -> PatchRiskReport:
    scenario = get_scenario(scenario_id)
    files_changed = sorted(scenario.fixed_files)
    findings = [
        *_target_guardrail_findings(scenario, files_changed),
        *_content_findings(scenario),
        _validation_finding(scenario),
    ]
    overall_status = _overall_status(findings)
    return PatchRiskReport(
        scenario_id=scenario.scenario_id,
        root_cause_id=scenario.root_cause_id,
        overall_status=overall_status,
        recommended_owner=OWNER_BY_CATEGORY.get(scenario.category, "engineering reviewer"),
        files_changed=files_changed,
        findings=findings,
    )


def build_patch_review_queue(scenario_ids: list[str] | None = None) -> list[PatchReviewItem]:
    scenarios = [get_scenario(scenario_id) for scenario_id in scenario_ids] if scenario_ids else list_scenarios()
    items = [_patch_review_item(scenario) for scenario in scenarios]
    return sorted(
        items,
        key=lambda item: (
            -STATUS_RISK_POINTS.get(item.overall_status, 0),
            -item.risk_score,
            item.scenario_id,
        ),
    )


def render_patch_risk_report(report: PatchRiskReport) -> str:
    files = "\n".join(f"- `{path}`" for path in report.files_changed)
    lines = [
        "# Patch Risk Diff",
        "",
        f"- scenario: `{report.scenario_id}`",
        f"- root_cause_id: `{report.root_cause_id}`",
        f"- overall_status: `{report.overall_status}`",
        f"- recommended_owner: `{report.recommended_owner}`",
        "",
        "## Files Changed",
        "",
        files,
        "",
        "## Findings",
        "",
        "| status | area | message |",
        "| --- | --- | --- |",
    ]
    for finding in report.findings:
        lines.append(f"| {finding.status} | {finding.area} | {finding.message} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Human review required before merge or deployment.",
            "This report uses deterministic scenario fixtures and static patch heuristics; it is not a production security scanner.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_patch_review_queue(queue: list[PatchReviewItem]) -> str:
    lines = [
        "# AegisOps Patch Review Queue",
        "",
        "This report ranks proposed patch reviews across synthetic scenarios so a reviewer can inspect blocking findings, review findings, ownership, and next action before merge.",
        "",
        "| rank | scenario | status | owner | risk_score | blocking | review | pass | next_action | report |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for rank, item in enumerate(queue, start=1):
        lines.append(
            f"| {rank} | {item.scenario_id} | {item.overall_status} | {item.recommended_owner} | "
            f"{item.risk_score} | {item.blocking_count} | {item.review_count} | {item.pass_count} | "
            f"{item.next_action} | [`{item.report_path}`](../{item.report_path}) |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Human review remains required before merge or deployment.",
            "The queue uses deterministic fixtures and static patch heuristics; it is not a production security scanner or a replacement for code review.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_patch_risk_report(
    reports_dir: Path | str = Path("reports"),
    scenario_id: str = "S4",
    mode: str = "multi",
) -> Path:
    output_path = Path(reports_dir) / scenario_id / mode / "patch-risk-diff.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_patch_risk_report(analyze_patch_risk(scenario_id)), encoding="utf-8")
    return output_path


def write_patch_review_queue(
    output_path: Path | str = Path("reports/patch-review-queue.md"),
    scenario_ids: list[str] | None = None,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_patch_review_queue(build_patch_review_queue(scenario_ids)), encoding="utf-8")
    return path


def _target_guardrail_findings(scenario: ScenarioSpec, files_changed: list[str]) -> list[PatchRiskFinding]:
    findings: list[PatchRiskFinding] = []
    for path in files_changed:
        if any(fnmatch(path, pattern) for pattern in scenario.blocked_files):
            findings.append(PatchRiskFinding("FAIL", "target guardrail", f"{path} is a blocked patch target"))
        elif any(fnmatch(path, pattern) for pattern in scenario.allowed_files):
            findings.append(PatchRiskFinding("PASS", "target guardrail", f"{path} matches the scenario allowlist"))
        else:
            findings.append(PatchRiskFinding("FAIL", "target guardrail", f"{path} is outside the scenario allowlist"))
    return findings


def _content_findings(scenario: ScenarioSpec) -> list[PatchRiskFinding]:
    findings: list[PatchRiskFinding] = []
    combined = "\n".join(scenario.fixed_files.values())
    if "image: aegisops/demo-api:latest" in combined or "tag: latest" in combined:
        findings.append(PatchRiskFinding("REVIEW", "kubernetes image", "image tag still uses latest and needs reviewer confirmation"))
    if "securityContext:" in combined:
        if "runAsNonRoot: true" in combined:
            findings.append(PatchRiskFinding("PASS", "container security", "runAsNonRoot is enabled in the proposed patch"))
        if "allowPrivilegeEscalation: false" in combined:
            findings.append(PatchRiskFinding("PASS", "container security", "allowPrivilegeEscalation=false is present in the proposed patch"))
    if scenario.category == "latency":
        findings.append(PatchRiskFinding("REVIEW", "performance", "benchmark dry-run evidence should be reviewed before merge"))
    return findings


def _validation_finding(scenario: ScenarioSpec) -> PatchRiskFinding:
    label = {
        "k8s-dry-run": "Kubernetes dry-run validation",
        "security-dry-run": "security dry-run validation",
        "latency-dry-run": "benchmark dry-run validation",
        "ci-dry-run": "CI dry-run validation",
        "docker-dry-run": "Docker dry-run validation",
        "pytest": "pytest validation",
    }.get(scenario.validation_kind, f"{scenario.validation_kind} validation")
    return PatchRiskFinding("REVIEW", "validation", f"{label} must pass and be reviewed")


def _overall_status(findings: list[PatchRiskFinding]) -> str:
    if any(finding.status == "FAIL" for finding in findings):
        return "FAIL"
    if any(finding.status == "REVIEW" for finding in findings):
        return "REVIEW"
    return "PASS"


def _patch_review_item(scenario: ScenarioSpec) -> PatchReviewItem:
    report = analyze_patch_risk(scenario.scenario_id)
    blocking_count = _count_findings(report, "FAIL")
    review_count = _count_findings(report, "REVIEW")
    pass_count = _count_findings(report, "PASS")
    return PatchReviewItem(
        scenario_id=report.scenario_id,
        root_cause_id=report.root_cause_id,
        category=scenario.category,
        overall_status=report.overall_status,
        recommended_owner=report.recommended_owner,
        risk_score=_risk_score(scenario, report.overall_status, blocking_count, review_count),
        blocking_count=blocking_count,
        review_count=review_count,
        pass_count=pass_count,
        next_action=_next_patch_review_action(scenario, blocking_count),
        report_path=f"reports/{report.scenario_id}/multi/patch-risk-diff.md",
    )


def _count_findings(report: PatchRiskReport, status: str) -> int:
    return sum(1 for finding in report.findings if finding.status == status)


def _risk_score(scenario: ScenarioSpec, overall_status: str, blocking_count: int, review_count: int) -> int:
    return (
        STATUS_RISK_POINTS.get(overall_status, 0)
        + CATEGORY_RISK_POINTS.get(scenario.category, 0)
        + blocking_count * 50
        + review_count * 5
    )


def _next_patch_review_action(scenario: ScenarioSpec, blocking_count: int) -> str:
    if blocking_count:
        return "Block merge; remove blocked or out-of-scope patch targets before review."
    if scenario.category == "security":
        return "Security reviewer checks hardening controls, then runs security dry-run validation."
    if scenario.category == "kubernetes":
        return "Platform reviewer checks manifest risk, then runs Kubernetes dry-run validation."
    if scenario.category == "latency":
        return "Performance reviewer checks algorithm change, then runs benchmark dry-run validation."
    if scenario.category == "ci":
        return "DevEx reviewer checks CI config, then runs CI dry-run validation."
    if scenario.category == "docker":
        return "Platform reviewer checks image dependency change, then runs Docker dry-run validation."
    return "Application reviewer checks patch intent, then runs pytest validation."
