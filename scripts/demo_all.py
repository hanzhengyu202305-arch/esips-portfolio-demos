from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "docs" / "DEMO_OUTPUT_INDEX.md"


@dataclass(frozen=True)
class DemoRun:
    name: str
    command: list[str]
    display_command: str
    purpose: str
    reports: tuple[str, ...]


@dataclass(frozen=True)
class DemoResult:
    name: str
    display_command: str
    purpose: str
    reports: tuple[str, ...]
    returncode: int

    @property
    def status(self) -> str:
        return "PASS" if self.returncode == 0 else "FAIL"


def build_demo_runs(aegisops_python: str) -> list[DemoRun]:
    return [
        DemoRun(
            name="AegisOps Agent",
            command=[
                "make",
                "-C",
                "aegisops-agent",
                "demo",
                "SCENARIO=S4",
                "MODE=multi",
                f"PYTHON={aegisops_python}",
            ],
            display_command="make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=<python>",
            purpose="issue evidence -> RCA -> patch preview -> validation -> PR-style report",
            reports=(
                "aegisops-agent/reports/S4/multi/issue-to-pr-report.md",
                "aegisops-agent/reports/S4/multi/pr-summary.md",
                "aegisops-agent/reports/S4/multi/demo-report.md",
            ),
        ),
        DemoRun(
            name="AegisOps Triage Queue",
            command=[
                "make",
                "-C",
                "aegisops-agent",
                "triage",
                f"PYTHON={aegisops_python}",
            ],
            display_command="make -C aegisops-agent triage PYTHON=<python>",
            purpose="multiple synthetic incidents -> severity/evidence ranking -> owner and next action",
            reports=("aegisops-agent/reports/triage-queue.md",),
        ),
        DemoRun(
            name="Patch Risk Diff",
            command=[
                "make",
                "-C",
                "aegisops-agent",
                "patch-risk",
                "SCENARIO=S4",
                "MODE=multi",
                f"PYTHON={aegisops_python}",
            ],
            display_command="make -C aegisops-agent patch-risk SCENARIO=S4 MODE=multi PYTHON=<python>",
            purpose="proposed patch -> target guardrails -> Kubernetes/security review findings",
            reports=("aegisops-agent/reports/S4/multi/patch-risk-diff.md",),
        ),
        DemoRun(
            name="AegisOps Patch Review Queue",
            command=[
                "make",
                "-C",
                "aegisops-agent",
                "patch-review-queue",
                f"PYTHON={aegisops_python}",
            ],
            display_command="make -C aegisops-agent patch-review-queue PYTHON=<python>",
            purpose="multiple patch previews -> risk ranking -> reviewer owner and next action",
            reports=("aegisops-agent/reports/patch-review-queue.md",),
        ),
        DemoRun(
            name="Kube Copilot",
            command=["make", "-C", "kube-copilot", "report"],
            display_command="make -C kube-copilot report",
            purpose="generated Kubernetes/CI artifacts -> deterministic policy findings",
            reports=(
                "kube-copilot/reports/risk-comparison.md",
                "kube-copilot/reports/policy-matrix.md",
            ),
        ),
        DemoRun(
            name="Kube Policy Pack",
            command=["make", "-C", "kube-copilot", "policy-pack"],
            display_command="make -C kube-copilot policy-pack",
            purpose="Kubernetes validation rules -> reusable reviewer policy pack",
            reports=(
                "kube-copilot/reports/policy-pack.json",
                "kube-copilot/reports/policy-pack.md",
            ),
        ),
        DemoRun(
            name="Haul Truck Planner",
            command=["make", "-C", "haul-truck-planner", "report"],
            display_command="make -C haul-truck-planner report",
            purpose="shortest path vs energy-aware planning under battery, grade, charging, and risk constraints",
            reports=(
                "haul-truck-planner/reports/route-experiment.md",
                "haul-truck-planner/reports/algorithm-comparison.md",
                "haul-truck-planner/reports/sensitivity-lab.md",
            ),
        ),
        DemoRun(
            name="Portfolio Adversarial Review",
            command=[sys.executable, "scripts/adversarial_review.py"],
            display_command="make adversarial-review",
            purpose="negative controls -> expected rejection or escalation -> machine-readable gate",
            reports=(
                "docs/ADVERSARIAL_REVIEW.md",
                "docs/ADVERSARIAL_REVIEW.json",
            ),
        ),
        DemoRun(
            name="EvidenceOps Scorecard",
            command=["make", "-C", "evidenceops-scorecard", "report"],
            display_command="make -C evidenceops-scorecard report",
            purpose="portfolio evidence inventory -> PASS/WEAK/MISSING scorecard",
            reports=(
                "evidenceops-scorecard/reports/evidence-scorecard.md",
                "evidenceops-scorecard/reports/submission-readiness.md",
            ),
        ),
        DemoRun(
            name="EvidenceOps Release Gate",
            command=["make", "-C", "evidenceops-scorecard", "release-gate"],
            display_command="make -C evidenceops-scorecard release-gate",
            purpose="public evidence status -> release/share gate with blockers",
            reports=(
                "evidenceops-scorecard/reports/release-gate.md",
                "evidenceops-scorecard/reports/release-gate.json",
            ),
        ),
    ]


def run_demo(demo: DemoRun, env: dict[str, str]) -> DemoResult:
    completed = subprocess.run(
        demo.command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=sys.stdout,
        stderr=subprocess.STDOUT,
        env=env,
    )
    return DemoResult(
        name=demo.name,
        display_command=demo.display_command,
        purpose=demo.purpose,
        reports=demo.reports,
        returncode=completed.returncode,
    )


def render_index(results: list[DemoResult]) -> str:
    overall = "PASS" if all(result.returncode == 0 for result in results) else "FAIL"
    lines = [
        "# Demo Output Index",
        "",
        "Generated by `make demo-all`.",
        "",
        f"Overall demo status: **{overall}**",
        "",
        "This file is a reviewer shortcut to the generated public evidence. It records commands, outputs, and boundaries without storing local machine paths or private application material.",
        "",
        "## Demo Runs",
        "",
        "| demo | status | purpose | command | outputs |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        outputs = "<br>".join(f"[`{path}`](../{path})" for path in result.reports)
        lines.append(
            f"| {result.name} | {result.status} | {result.purpose} | `{result.display_command}` | {outputs} |"
        )
    lines.extend(
        [
            "",
            "## Reviewer Reading Order",
            "",
            "1. Start with [`docs/EXECUTIVE_ONE_PAGE.md`](EXECUTIVE_ONE_PAGE.md).",
            "2. Use this index to open the fresh output from each demo run.",
            "3. Cross-check public claims in [`CLAIMS_MATRIX.md`](../CLAIMS_MATRIX.md).",
            "4. Check final repository status in [`PORTFOLIO_STATUS.md`](../PORTFOLIO_STATUS.md).",
            "",
            "## Boundary",
            "",
            "The demos use synthetic fixtures and deterministic local checks. Passing this index means the public evidence was regenerated successfully; it does not prove production readiness, replace human review, or approve any external application.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_index(results: list[DemoResult], path: Path = INDEX_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_index(results), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all public demos and write a reviewer output index.")
    parser.add_argument("--aegisops-python", default=os.environ.get("AEGISOPS_PY", "python3"))
    args = parser.parse_args()

    env = os.environ.copy()
    env["AEGISOPS_STABLE_REPORTS"] = "1"
    demos = build_demo_runs(args.aegisops_python)
    release_gate_runs = [demo for demo in demos if demo.name == "EvidenceOps Release Gate"]
    regular_runs = [demo for demo in demos if demo.name != "EvidenceOps Release Gate"]
    results = [run_demo(demo, env) for demo in regular_runs]
    write_index(results)
    release_gate_results = [run_demo(demo, env) for demo in release_gate_runs]
    results.extend(release_gate_results)
    write_index(results)
    print(display_path(INDEX_PATH))
    return 0 if all(result.returncode == 0 for result in results) else 1


def display_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


if __name__ == "__main__":
    sys.exit(main())
