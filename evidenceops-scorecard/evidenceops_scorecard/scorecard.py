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


def build_scorecard(root: Path | str = ROOT) -> dict[str, Any]:
    repo_root = Path(root).resolve()
    projects = [_project_status(repo_root, project) for project in PROJECTS]
    portfolio_evidence = [_evidence_status(repo_root, path) for path in PORTFOLIO_EVIDENCE]
    missing_evidence = [
        item["path"]
        for item in portfolio_evidence
        if not item["exists"]
    ]
    for project in projects:
        missing_evidence.extend(item["path"] for item in project["evidence"] if not item["exists"])

    status_payload = _read_portfolio_status(repo_root)
    passed_projects = sum(1 for project in projects if project["status"] == "PASS")
    portfolio_evidence_status = "PASS" if not missing_evidence else "FAIL"

    return {
        "portfolio_evidence_status": portfolio_evidence_status,
        "application_submission_status": "NEEDS_OFFICIAL_CONFIRMATION",
        "summary": {
            "passed_projects": passed_projects,
            "total_projects": len(projects),
            "portfolio_status_file": status_payload.get("overall_portfolio_status", "MISSING_OR_INVALID"),
        },
        "portfolio_evidence": portfolio_evidence,
        "projects": projects,
        "missing_evidence": missing_evidence,
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
        f"Application submission status: **{scorecard['application_submission_status']}**",
        "",
        "EvidenceOps is the fourth demo layer: it checks whether the public portfolio has reviewable evidence for each project line.",
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
        lines.append(f"| `{item['path']}` | {'PASS' if item['exists'] else 'MISSING'} |")
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
            f"- Application submission: `{scorecard['application_submission_status']}`",
            f"- Projects with evidence: `{scorecard['summary']['passed_projects']}/{scorecard['summary']['total_projects']}`",
            "",
            "## Next Manual Checks",
            "",
            *[f"- {item}" for item in scorecard["manual_review_items"]],
            "",
            "Do not treat this file as final application approval. It is a public evidence readiness report only.",
            "",
        ]
    )


def write_reports(root: Path | str = ROOT, out_dir: Path | str | None = None) -> dict[str, Path]:
    repo_root = Path(root).resolve()
    output_dir = Path(out_dir) if out_dir is not None else repo_root / "evidenceops-scorecard" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    scorecard = build_scorecard(repo_root)
    paths = {
        "json": output_dir / "evidence-scorecard.json",
        "markdown": output_dir / "evidence-scorecard.md",
        "submission": output_dir / "submission-readiness.md",
    }
    paths["json"].write_text(json.dumps(scorecard, indent=2) + "\n", encoding="utf-8")
    paths["markdown"].write_text(render_markdown(scorecard), encoding="utf-8")
    paths["submission"].write_text(render_submission_readiness(scorecard), encoding="utf-8")
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate EvidenceOps portfolio evidence scorecards.")
    parser.add_argument("--root", default=str(ROOT), help="Repository root to inspect.")
    parser.add_argument("--out-dir", default=None, help="Directory where reports should be written.")
    args = parser.parse_args()

    paths = write_reports(args.root, args.out_dir)
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
    status = "PASS" if all(item["exists"] for item in evidence) else "FAIL"
    return {
        "id": project["id"],
        "name": project["name"],
        "role": project["role"],
        "status": status,
        "evidence": evidence,
    }


def _evidence_status(repo_root: Path, relative_path: str) -> dict[str, Any]:
    path = repo_root / relative_path
    return {
        "path": relative_path,
        "exists": path.is_file(),
        "bytes": path.stat().st_size if path.is_file() else 0,
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
    return "<br>".join(f"`{item['path']}`: {'PASS' if item['exists'] else 'MISSING'}" for item in evidence)


if __name__ == "__main__":
    sys.exit(main())
