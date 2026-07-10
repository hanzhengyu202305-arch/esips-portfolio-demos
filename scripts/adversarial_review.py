from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Callable
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "aegisops-agent"))
sys.path.insert(0, str(ROOT / "kube-copilot"))
sys.path.insert(0, str(ROOT / "haul-truck-planner"))

from agent.diagnosis_engine import infer_root_cause  # noqa: E402
from agent.llm.mock_client import MockLLM  # noqa: E402
from agent.graph.single_agent import run_single_agent  # noqa: E402
from agent.scenarios import get_scenario  # noqa: E402
from agent.schemas import Diagnosis  # noqa: E402
from haul_truck_planner.planner import (  # noqa: E402
    EnergyModel,
    MineMap,
    Truck,
    plan_route,
    plan_route_astar,
)
from kube_copilot.risk_report import adversarial_workspaces  # noqa: E402
from kube_copilot.validator import validate_workspace  # noqa: E402


@dataclass(frozen=True)
class ChallengeResult:
    challenge_id: str
    project: str
    attack: str
    expected: str
    observed: str
    passed: bool
    evidence: str


def run_adversarial_review() -> dict:
    challenges = [
        *_aegisops_challenges(),
        *_kube_challenges(),
        *_haul_challenges(),
    ]
    passed = sum(1 for challenge in challenges if challenge.passed)
    return {
        "overall_status": "PASS" if passed == len(challenges) else "FAIL",
        "summary": {
            "passed": passed,
            "total": len(challenges),
            "failed": len(challenges) - passed,
        },
        "challenges": [asdict(challenge) for challenge in challenges],
        "boundary": (
            "These deterministic negative controls test portfolio failure handling. "
            "They do not prove production robustness or formal security assurance."
        ),
    }


def render_markdown(review: dict) -> str:
    lines = [
        "# Portfolio Adversarial Review",
        "",
        f"Overall status: **{review['overall_status']}**",
        "",
        f"Challenges passed: **{review['summary']['passed']}/{review['summary']['total']}**",
        "",
        "The suite attacks assumptions behind the three demos instead of only replaying happy paths.",
        "",
        "| id | project | attack | expected | observed | result | evidence |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for challenge in review["challenges"]:
        result = "PASS" if challenge["passed"] else "FAIL"
        lines.append(
            f"| {challenge['challenge_id']} | {challenge['project']} | {challenge['attack']} | "
            f"{challenge['expected']} | {challenge['observed']} | {result} | {challenge['evidence']} |"
        )
    lines.extend(
        [
            "",
            "## First-Principles Interpretation",
            "",
            "- AegisOps must derive a diagnosis from evidence and abstain when evidence is missing or contradictory.",
            "- Kube Copilot must inspect parsed structure across documents and containers, not trust matching words.",
            "- Haul Truck Planner must reject impossible states and keep A* consistent with the Dijkstra baseline.",
            "",
            "## Boundary",
            "",
            review["boundary"],
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(output_dir: Path | str = ROOT / "docs") -> tuple[Path, Path]:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    review = run_adversarial_review()
    json_path = target / "ADVERSARIAL_REVIEW.json"
    markdown_path = target / "ADVERSARIAL_REVIEW.md"
    json_path.write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(review), encoding="utf-8")
    return json_path, markdown_path


def _aegisops_challenges() -> list[ChallengeResult]:
    scenario = get_scenario("S4")
    evidence = {
        "raw_log": scenario.raw_log,
        "signals": scenario.evidence_signals,
    }
    contexts = [
        {
            "title": "Kubernetes CrashLoopBackOff",
            "text": "Inspect environment variables when a container restarts.",
            "score": 2,
        }
    ]
    tampered = replace(scenario, root_cause_id="tampered_gold_label")
    diagnosis = MockLLM().diagnose(tampered, evidence, contexts, mode="multi")
    missing = infer_root_cause({"raw_log": "", "signals": []}, [], mode="single")
    conflict = infer_root_cause(
        {
            "raw_log": "APP_MODE is empty; got ''. APP_MODE has unsupported value 'broken'.",
            "signals": [
                {"kind": "ci", "message": "empty APP_MODE"},
                {"kind": "kubernetes", "message": "APP_MODE got 'broken' and is unsupported"},
            ],
        },
        [],
        mode="multi",
    )
    escalation = Diagnosis(
        scenario_id="S4",
        root_cause_id="undetermined",
        confidence=0.0,
        decision="ESCALATE",
        decision_reason="adversarial evidence conflict",
        ranked_hypotheses=[],
        evidence_refs=[],
        retrieved_context_refs=[],
        impact="root cause is unresolved",
        fix_plan=["Stop automated remediation and request human evidence review."],
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("agent.graph.nodes.MockLLM.diagnose", return_value=escalation):
            escalated_run = run_single_agent("S4", reports_dir=Path(temp_dir))
    return [
        ChallengeResult(
            "AEG-01",
            "AegisOps",
            "tamper fixture gold label",
            "infer invalid_app_mode_env from evidence",
            diagnosis.root_cause_id,
            diagnosis.root_cause_id == "invalid_app_mode_env",
            "diagnosis is independent of ScenarioSpec.root_cause_id",
        ),
        ChallengeResult(
            "AEG-02",
            "AegisOps",
            "remove all diagnostic evidence",
            "ESCALATE",
            missing.decision,
            missing.decision == "ESCALATE",
            missing.reason,
        ),
        ChallengeResult(
            "AEG-03",
            "AegisOps",
            "inject equally supported conflicting causes",
            "ESCALATE",
            conflict.decision,
            conflict.decision == "ESCALATE",
            conflict.reason,
        ),
        ChallengeResult(
            "AEG-04",
            "AegisOps",
            "force an escalation decision before remediation",
            "no patch and no validation commands",
            (
                f"patch_applied={escalated_run.patch.patch_applied}, "
                f"commands={len(escalated_run.patch.commands_run)}"
            ),
            not escalated_run.patch.patch_applied and not escalated_run.patch.commands_run,
            "agent flow stops before patch preview and validation",
        ),
    ]


def _kube_challenges() -> list[ChallengeResult]:
    results: list[ChallengeResult] = []
    for index, (name, workspace) in enumerate(adversarial_workspaces().items(), start=1):
        report = validate_workspace(workspace)
        expected_pass = name == "safe baseline"
        observed = "PASS" if report.passed else "FAIL"
        expected = "PASS" if expected_pass else "FAIL"
        results.append(
            ChallengeResult(
                f"KUBE-{index:02d}",
                "Kube Copilot",
                name,
                expected,
                observed,
                report.passed == expected_pass,
                "; ".join(report.findings[:3]) if report.findings else "no blocking findings",
            )
        )
    return results


def _haul_challenges() -> list[ChallengeResult]:
    baseline_mine = MineMap(
        width=5,
        height=4,
        blocked={(1, 1), (1, 2), (3, 1)},
        charging={(2, 2)},
        grades={(2, 1): 0.16, (2, 2): -0.05},
        risk_zones={(4, 1): 2.5, (4, 2): 2.5},
    )
    truck = Truck(capacity_kwh=10.0, initial_kwh=6.2, reserve_kwh=1.0)
    dijkstra = plan_route(baseline_mine, (0, 0), (4, 3), truck)
    astar = plan_route_astar(baseline_mine, (0, 0), (4, 3), truck)

    invalid_battery_error = _captured_value_error(
        lambda: plan_route(
            MineMap(3, 1, set(), set(), {}),
            (0, 0),
            (2, 0),
            Truck(capacity_kwh=5.0, initial_kwh=6.0, reserve_kwh=1.0),
        )
    )
    blocked_charger_error = _captured_value_error(
        lambda: plan_route(
            MineMap(3, 1, {(1, 0)}, {(1, 0)}, {}),
            (0, 0),
            (2, 0),
            Truck(capacity_kwh=5.0, initial_kwh=4.0, reserve_kwh=1.0),
        )
    )
    harsh_error = _captured_value_error(
        lambda: plan_route(
            MineMap(
                3,
                1,
                set(),
                set(),
                {},
                energy_model=EnergyModel(base_kwh_per_cell=1.0, minimum_step_kwh=1.0),
            ),
            (0, 0),
            (2, 0),
            Truck(capacity_kwh=3.0, initial_kwh=2.0, reserve_kwh=0.5),
        )
    )
    same_cost = dijkstra.total_cost == astar.total_cost
    return [
        ChallengeResult(
            "HAUL-01",
            "Haul Truck Planner",
            "compare A* against Dijkstra correctness baseline",
            f"same optimal cost ({dijkstra.total_cost})",
            f"A* cost {astar.total_cost}",
            same_cost,
            f"expanded states: Dijkstra={dijkstra.expanded_states}, A*={astar.expanded_states}",
        ),
        ChallengeResult(
            "HAUL-02",
            "Haul Truck Planner",
            "initial energy exceeds battery capacity",
            "reject input",
            invalid_battery_error or "accepted",
            "reserve <= initial <= capacity" in invalid_battery_error,
            "battery-state invariant",
        ),
        ChallengeResult(
            "HAUL-03",
            "Haul Truck Planner",
            "charging point overlaps blocked road",
            "reject input",
            blocked_charger_error or "accepted",
            "cannot also be blocked" in blocked_charger_error,
            "map topology invariant",
        ),
        ChallengeResult(
            "HAUL-04",
            "Haul Truck Planner",
            "raise per-cell energy consumption above available margin",
            "no feasible route",
            harsh_error or "route returned",
            "no energy-feasible route" in harsh_error,
            "explicit EnergyModel sensitivity",
        ),
    ]


def _captured_value_error(operation: Callable[[], object]) -> str:
    try:
        operation()
    except ValueError as exc:
        return str(exc)
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run portfolio adversarial negative controls.")
    parser.add_argument("--out-dir", default=str(ROOT / "docs"))
    args = parser.parse_args()
    json_path, markdown_path = write_reports(args.out_dir)
    review = json.loads(json_path.read_text(encoding="utf-8"))
    print(markdown_path.relative_to(ROOT).as_posix())
    return 0 if review["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
