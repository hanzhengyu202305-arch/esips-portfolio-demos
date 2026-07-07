from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from agent.scenarios import ScenarioSpec, get_scenario


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


OWNER_BY_CATEGORY = {
    "security": "platform/security reviewer",
    "kubernetes": "platform reviewer",
    "latency": "application performance reviewer",
    "ci": "devex reviewer",
    "docker": "platform reviewer",
    "pytest": "application reviewer",
}


def analyze_patch_risk(scenario_id: str) -> PatchRiskReport:
    scenario = get_scenario(scenario_id)
    files_changed = sorted(scenario.fixed_files)
    findings = [
        *_target_guardrail_findings(scenario, files_changed),
        *_content_findings(scenario),
        _validation_finding(scenario),
    ]
    overall_status = "REVIEW" if any(finding.status == "REVIEW" for finding in findings) else "PASS"
    return PatchRiskReport(
        scenario_id=scenario.scenario_id,
        root_cause_id=scenario.root_cause_id,
        overall_status=overall_status,
        recommended_owner=OWNER_BY_CATEGORY.get(scenario.category, "engineering reviewer"),
        files_changed=files_changed,
        findings=findings,
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


def write_patch_risk_report(
    reports_dir: Path | str = Path("reports"),
    scenario_id: str = "S4",
    mode: str = "multi",
) -> Path:
    output_path = Path(reports_dir) / scenario_id / mode / "patch-risk-diff.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_patch_risk_report(analyze_patch_risk(scenario_id)), encoding="utf-8")
    return output_path


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
