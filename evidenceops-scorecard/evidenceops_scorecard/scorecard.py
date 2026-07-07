from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

PROJECTS = [
    {
        "id": "aegisops-agent",
        "name": "AegisOps Agent",
        "role": "Main SDLC agent evidence",
        "evidence": [
            "aegisops-agent/reports/final-portfolio-report.md",
            "aegisops-agent/reports/S4/multi/pr-summary.md",
        ],
    },
    {
        "id": "kube-copilot",
        "name": "Kube Copilot",
        "role": "Kubernetes validation support",
        "evidence": [
            "kube-copilot/reports/risk-comparison.md",
            "kube-copilot/reports/policy-matrix.md",
            "kube-copilot/reports/policy-pack.json",
            "kube-copilot/reports/policy-pack.md",
        ],
    },
    {
        "id": "haul-truck-planner",
        "name": "Haul Truck Planner",
        "role": "EE and mining planning support",
        "evidence": [
            "haul-truck-planner/reports/route-experiment.md",
            "haul-truck-planner/reports/algorithm-comparison.md",
        ],
    },
]

PORTFOLIO_EVIDENCE = [
    "README.md",
    "CLAIMS_MATRIX.md",
    "PORTFOLIO_STATUS.md",
    "PORTFOLIO_STATUS.json",
]

QUALITY_RULES = {
    "README.md": {"min_bytes": 120, "keywords": ["validation", "EvidenceOps"]},
    "CLAIMS_MATRIX.md": {"min_bytes": 120, "keywords": ["Claim", "Boundary"]},
    "PORTFOLIO_STATUS.md": {"min_bytes": 80, "keywords": ["Overall status", "Boundary"]},
    "PORTFOLIO_STATUS.json": {"min_bytes": 20, "keywords": ["overall_portfolio_status"]},
    "aegisops-agent/reports/final-portfolio-report.md": {"min_bytes": 120, "keywords": ["AegisOps", "validation"]},
    "aegisops-agent/reports/S4/multi/pr-summary.md": {"min_bytes": 120, "keywords": ["root cause", "validation"]},
    "kube-copilot/reports/risk-comparison.md": {"min_bytes": 120, "keywords": ["Kube Copilot", "manual review"]},
    "kube-copilot/reports/policy-matrix.md": {"min_bytes": 120, "keywords": ["policy", "validation"]},
    "kube-copilot/reports/policy-pack.json": {"min_bytes": 120, "keywords": ["kube-copilot-predeploy", "rules", "trust_boundary"]},
    "kube-copilot/reports/policy-pack.md": {"min_bytes": 120, "keywords": ["Policy Pack", "validation", "human review"]},
    "haul-truck-planner/reports/route-experiment.md": {"min_bytes": 120, "keywords": ["battery", "charging"]},
    "haul-truck-planner/reports/algorithm-comparison.md": {"min_bytes": 120, "keywords": ["Dijkstra", "A*"]},
}


def build_scorecard(root: Path | str = ROOT) -> dict[str, Any]:
    repo_root = Path(root).resolve()
    projects = [_project_status(repo_root, project) for project in PROJECTS]
    portfolio_evidence = [_evidence_status(repo_root, path) for path in PORTFOLIO_EVIDENCE]
    missing_evidence = [
        item["path"]
        for item in portfolio_evidence
        if item["status"] == "MISSING"
    ]
    for project in projects:
        missing_evidence.extend(item["path"] for item in project["evidence"] if item["status"] == "MISSING")
    all_evidence = [*portfolio_evidence, *[item for project in projects for item in project["evidence"]]]
    weak_evidence = [item["path"] for item in all_evidence if item["status"] == "WEAK"]

    status_payload = _read_portfolio_status(repo_root)
    passed_projects = sum(1 for project in projects if project["status"] == "PASS")
    if missing_evidence:
        portfolio_evidence_status = "FAIL"
    elif weak_evidence:
        portfolio_evidence_status = "WEAK"
    else:
        portfolio_evidence_status = "PASS"

    return {
        "portfolio_evidence_status": portfolio_evidence_status,
        "application_submission_status": "NEEDS_OFFICIAL_CONFIRMATION",
        "summary": {
            "passed_projects": passed_projects,
            "total_projects": len(projects),
            "portfolio_status_file": status_payload.get("overall_portfolio_status", "MISSING_OR_INVALID"),
            "quality_score": _quality_score(all_evidence),
            "passed_evidence": sum(1 for item in all_evidence if item["status"] == "PASS"),
            "weak_evidence": len(weak_evidence),
            "missing_evidence": len(missing_evidence),
        },
        "portfolio_evidence": portfolio_evidence,
        "projects": projects,
        "missing_evidence": missing_evidence,
        "weak_evidence": weak_evidence,
        "quality_fixes": _quality_fixes(all_evidence),
        "manual_review_items": [
            "current official application deadline",
            "active form fields and upload requirements",
            "full-time placement availability period",
            "whether public repository links are accepted in the active form",
        ],
    }


def render_markdown(scorecard: dict[str, Any]) -> str:
    lines = [
        "# EvidenceOps Scorecard",
        "",
        f"Portfolio evidence status: **{scorecard['portfolio_evidence_status']}**",
        "",
        f"Quality score: **{scorecard['summary']['quality_score']}/100**",
        "",
        f"Application submission status: **{scorecard['application_submission_status']}**",
        "",
        "EvidenceOps is the fourth demo layer: it checks whether public portfolio evidence is present, strong enough for review, and safely bounded.",
        "",
        "## Project Evidence",
        "",
        "| project | status | role | evidence |",
        "| --- | --- | --- | --- |",
    ]
    for project in scorecard["projects"]:
        evidence_summary = _format_evidence(project["evidence"])
        lines.append(f"| {project['name']} | {project['status']} | {project['role']} | {evidence_summary} |")
    lines.extend(
        [
            "",
            "## Portfolio Evidence",
            "",
            "| artifact | status |",
            "| --- | --- |",
        ]
    )
    for item in scorecard["portfolio_evidence"]:
        lines.append(f"| `{item['path']}` | {item['status']} |")
    lines.extend(
        [
            "",
            "## Missing Evidence",
            "",
        ]
    )
    if scorecard["missing_evidence"]:
        lines.extend(f"- `{path}`" for path in scorecard["missing_evidence"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Weak Evidence",
            "",
        ]
    )
    if scorecard["weak_evidence"]:
        lines.extend(f"- `{path}`" for path in scorecard["weak_evidence"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Quality Fixes",
            "",
        ]
    )
    if scorecard["quality_fixes"]:
        lines.extend(f"- {item}" for item in scorecard["quality_fixes"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Manual Review Before Submission",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in scorecard["manual_review_items"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "The public repository uses synthetic fixtures only. EvidenceOps checks public artifacts and review readiness; it does not prove production readiness or replace official application checks.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_submission_readiness(scorecard: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Submission Readiness",
            "",
            f"- Public evidence: `{scorecard['portfolio_evidence_status']}`",
            f"- Evidence quality score: `{scorecard['summary']['quality_score']}/100`",
            f"- Application submission: `{scorecard['application_submission_status']}`",
            f"- Projects with evidence: `{scorecard['summary']['passed_projects']}/{scorecard['summary']['total_projects']}`",
            f"- Weak evidence items: `{scorecard['summary']['weak_evidence']}`",
            f"- Missing evidence items: `{scorecard['summary']['missing_evidence']}`",
            "",
            "## Next Manual Checks",
            "",
            *[f"- {item}" for item in scorecard["manual_review_items"]],
            "",
            "Do not treat this file as final application approval. It is a public evidence quality report only.",
            "",
        ]
    )


def build_release_gate(root: Path | str = ROOT) -> dict[str, Any]:
    repo_root = Path(root).resolve()
    scorecard = build_scorecard(repo_root)
    status_payload = _read_portfolio_status(repo_root)
    checks = [
        _release_check(
            "portfolio evidence scorecard",
            scorecard["portfolio_evidence_status"] == "PASS",
            "evidenceops-scorecard/reports/evidence-scorecard.md",
            f"portfolio evidence status is {scorecard['portfolio_evidence_status']}",
            "portfolio evidence scorecard is not PASS",
        ),
        _release_check(
            "portfolio status file",
            status_payload.get("overall_portfolio_status") == "PASS",
            "PORTFOLIO_STATUS.json",
            f"portfolio status file is {status_payload.get('overall_portfolio_status', 'MISSING_OR_INVALID')}",
            f"portfolio status file is {status_payload.get('overall_portfolio_status', 'MISSING_OR_INVALID')}",
        ),
        _demo_index_check(repo_root),
        _claim_trace_check(repo_root),
        _portfolio_named_check(status_payload, "public boundary check", "public boundary check did not pass"),
        _validation_suite_check(status_payload),
    ]
    blockers = [check["blocker"] for check in checks if check["status"] != "PASS"]
    return {
        "release_gate_status": "PASS" if not blockers else "BLOCKED",
        "required_checks_passed": sum(1 for check in checks if check["status"] == "PASS"),
        "required_checks_total": len(checks),
        "checks": checks,
        "blockers": blockers,
        "boundary": "Release gate checks public portfolio evidence only; it is not official application approval.",
    }


def render_release_gate_markdown(gate: dict[str, Any]) -> str:
    lines = [
        "# EvidenceOps Release Gate",
        "",
        f"Release gate status: **{gate['release_gate_status']}**",
        "",
        f"Required checks: **{gate['required_checks_passed']}/{gate['required_checks_total']}**",
        "",
        "## Checks",
        "",
        "| check | status | evidence |",
        "| --- | --- | --- |",
    ]
    for check in gate["checks"]:
        lines.append(f"| {check['name']} | {check['status']} | `{check['evidence']}` |")
    lines.extend(["", "## Blockers", ""])
    if gate["blockers"]:
        lines.extend(f"- {blocker}" for blocker in gate["blockers"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            gate["boundary"],
            "Passing this gate means the public repo is ready for review as a portfolio artifact, not official application approval.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(root: Path | str = ROOT, out_dir: Path | str | None = None) -> dict[str, Path]:
    repo_root = Path(root).resolve()
    output_dir = Path(out_dir) if out_dir is not None else repo_root / "evidenceops-scorecard" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    scorecard = build_scorecard(repo_root)
    release_gate = build_release_gate(repo_root)
    paths = {
        "json": output_dir / "evidence-scorecard.json",
        "markdown": output_dir / "evidence-scorecard.md",
        "submission": output_dir / "submission-readiness.md",
        "release_gate_json": output_dir / "release-gate.json",
        "release_gate_markdown": output_dir / "release-gate.md",
    }
    paths["json"].write_text(json.dumps(scorecard, indent=2) + "\n", encoding="utf-8")
    paths["markdown"].write_text(render_markdown(scorecard), encoding="utf-8")
    paths["submission"].write_text(render_submission_readiness(scorecard), encoding="utf-8")
    paths["release_gate_json"].write_text(json.dumps(release_gate, indent=2) + "\n", encoding="utf-8")
    paths["release_gate_markdown"].write_text(render_release_gate_markdown(release_gate), encoding="utf-8")
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate EvidenceOps portfolio evidence scorecards.")
    parser.add_argument("--root", default=str(ROOT), help="Repository root to inspect.")
    parser.add_argument("--out-dir", default=None, help="Directory where reports should be written.")
    parser.add_argument("--release-gate", action="store_true", help="Exit based on release gate status instead of scorecard status.")
    args = parser.parse_args()

    paths = write_reports(args.root, args.out_dir)
    if args.release_gate:
        print(display_report_path(Path(args.root).resolve(), paths["release_gate_markdown"]))
        release_gate = json.loads(paths["release_gate_json"].read_text(encoding="utf-8"))
        return 0 if release_gate["release_gate_status"] == "PASS" else 1
    print(display_report_path(Path(args.root).resolve(), paths["markdown"]))
    scorecard = json.loads(paths["json"].read_text(encoding="utf-8"))
    return 0 if scorecard["portfolio_evidence_status"] == "PASS" else 1


def display_report_path(root: Path | str, report_path: Path | str) -> str:
    repo_root = Path(root).resolve()
    path = Path(report_path).resolve()
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.name


def _project_status(repo_root: Path, project: dict[str, Any]) -> dict[str, Any]:
    evidence = [_evidence_status(repo_root, path) for path in project["evidence"]]
    if any(item["status"] == "MISSING" for item in evidence):
        status = "FAIL"
    elif any(item["status"] == "WEAK" for item in evidence):
        status = "WEAK"
    else:
        status = "PASS"
    return {
        "id": project["id"],
        "name": project["name"],
        "role": project["role"],
        "status": status,
        "evidence": evidence,
    }


def _evidence_status(repo_root: Path, relative_path: str) -> dict[str, Any]:
    path = repo_root / relative_path
    exists = path.is_file()
    quality_issues = _quality_issues(path, relative_path) if exists else ["missing file"]
    if not exists:
        status = "MISSING"
    elif quality_issues:
        status = "WEAK"
    else:
        status = "PASS"
    return {
        "path": relative_path,
        "exists": exists,
        "status": status,
        "bytes": path.stat().st_size if exists else 0,
        "quality_issues": quality_issues,
    }


def _read_portfolio_status(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "PORTFOLIO_STATUS.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _format_evidence(evidence: list[dict[str, Any]]) -> str:
    return "<br>".join(f"`{item['path']}`: {item['status']}" for item in evidence)


def _quality_issues(path: Path, relative_path: str) -> list[str]:
    rule = QUALITY_RULES.get(relative_path, {"min_bytes": 1, "keywords": []})
    issues: list[str] = []
    size = path.stat().st_size
    min_bytes = int(rule["min_bytes"])
    if size < min_bytes:
        issues.append(f"below minimum size: {size} < {min_bytes} bytes")
    text = _read_text(path).lower()
    for keyword in rule["keywords"]:
        if keyword.lower() not in text:
            issues.append(f"missing keyword: {keyword}")
    return issues


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def _quality_score(evidence: list[dict[str, Any]]) -> int:
    if not evidence:
        return 0
    points = 0.0
    for item in evidence:
        if item["status"] == "PASS":
            points += 1
        elif item["status"] == "WEAK":
            points += 0.5
    return round((points / len(evidence)) * 100)


def _quality_fixes(evidence: list[dict[str, Any]]) -> list[str]:
    fixes: list[str] = []
    for item in evidence:
        if item["status"] == "PASS":
            continue
        issues = "; ".join(item["quality_issues"])
        fixes.append(f"`{item['path']}`: {issues}")
    return fixes


def _release_check(name: str, passed: bool, evidence: str, detail: str, blocker: str) -> dict[str, str]:
    return {
        "name": name,
        "status": "PASS" if passed else "BLOCKED",
        "evidence": evidence,
        "detail": detail,
        "blocker": "" if passed else blocker,
    }


def _demo_index_check(repo_root: Path) -> dict[str, str]:
    path = repo_root / "docs/DEMO_OUTPUT_INDEX.md"
    if not path.is_file():
        return _release_check(
            "demo output index",
            False,
            "docs/DEMO_OUTPUT_INDEX.md",
            "missing demo output index",
            "docs/DEMO_OUTPUT_INDEX.md is missing",
        )
    text = path.read_text(encoding="utf-8")
    passed = "Overall demo status: **PASS**" in text
    return _release_check(
        "demo output index",
        passed,
        "docs/DEMO_OUTPUT_INDEX.md",
        "demo output index reports PASS" if passed else "demo output index does not report PASS",
        "demo output index is not PASS",
    )


def _claim_trace_check(repo_root: Path) -> dict[str, str]:
    path = repo_root / "docs/REVIEWER_CLAIM_TRACE.md"
    if not path.is_file():
        return _release_check(
            "claim trace",
            False,
            "docs/REVIEWER_CLAIM_TRACE.md",
            "missing reviewer claim trace",
            "docs/REVIEWER_CLAIM_TRACE.md is missing",
        )
    text = path.read_text(encoding="utf-8")
    lower_text = text.lower()
    passed = "reviewer claim trace" in lower_text and "boundary" in lower_text
    return _release_check(
        "claim trace",
        passed,
        "docs/REVIEWER_CLAIM_TRACE.md",
        "claim trace includes boundaries" if passed else "claim trace is missing boundary language",
        "claim trace is incomplete",
    )


def _portfolio_named_check(status_payload: dict[str, Any], name: str, blocker: str) -> dict[str, str]:
    named = _portfolio_check_status(status_payload, name)
    return _release_check(
        name,
        named == "PASS",
        "PORTFOLIO_STATUS.json",
        f"{name} is {named}",
        blocker,
    )


def _validation_suite_check(status_payload: dict[str, Any]) -> dict[str, str]:
    required = [
        "top-level tests",
        "AegisOps acceptance",
        "Kube Copilot report",
        "Kube Policy Pack",
        "Haul Truck Planner report",
        "EvidenceOps scorecard",
    ]
    missing_or_failed = [name for name in required if _portfolio_check_status(status_payload, name) != "PASS"]
    return _release_check(
        "required validation suite",
        not missing_or_failed,
        "PORTFOLIO_STATUS.json",
        "required validation suite passed"
        if not missing_or_failed
        else f"missing or failed checks: {', '.join(missing_or_failed)}",
        f"required validation suite did not pass: {', '.join(missing_or_failed)}",
    )


def _portfolio_check_status(status_payload: dict[str, Any], name: str) -> str:
    for check in status_payload.get("checks", []):
        if check.get("name") == name:
            return str(check.get("status", "MISSING"))
    return "MISSING"


if __name__ == "__main__":
    sys.exit(main())
