from __future__ import annotations

import argparse
import json

from agent.acceptance import run_acceptance
from agent.diagnostics import render_doctor_markdown, run_doctor
from agent.evaluation.evaluator import run_eval
from agent.graph.multi_agent import run_multi_agent
from agent.graph.single_agent import run_single_agent
from agent.memory.retriever import build_index, retrieve
from agent.poc import create_scorecard, run_poc_repro
from agent.reporting import create_final_report, create_scenario_matrix
from agent.scenario_runner import run_scenario
from agent.scenarios import list_scenarios
from agent.tools.evidence_tools import collect_evidence
from agent.tools.test_tools import run_validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aegisops", description="AegisOps Agent CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("help")

    scenario_parser = sub.add_parser("scenario")
    scenario_parser.add_argument("--scenario", required=True)

    evidence_parser = sub.add_parser("collect-evidence")
    evidence_parser.add_argument("--scenario", required=True)

    sub.add_parser("build-index")

    retrieve_parser = sub.add_parser("retrieve")
    retrieve_parser.add_argument("--query", required=True)

    demo_parser = sub.add_parser("demo")
    demo_parser.add_argument("--scenario", required=True)
    demo_parser.add_argument("--mode", choices=["single", "multi"], default="multi")

    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--scenario", required=True)
    validate_parser.add_argument("--mode", choices=["single", "multi"], default="multi")

    sub.add_parser("eval-mock")
    sub.add_parser("matrix")
    sub.add_parser("doctor")
    sub.add_parser("acceptance")
    sub.add_parser("report")
    sub.add_parser("list-scenarios")
    sub.add_parser("scorecard")

    poc_parser = sub.add_parser("poc-repro")
    poc_parser.add_argument("--runs", type=int, default=3)

    args = parser.parse_args(argv)

    if args.command in {None, "help"}:
        _print_help()
        return 0
    if args.command == "scenario":
        print(run_scenario(args.scenario))
        return 0
    if args.command == "collect-evidence":
        print(collect_evidence(args.scenario))
        return 0
    if args.command == "build-index":
        print(build_index())
        return 0
    if args.command == "retrieve":
        print(json.dumps(retrieve(args.query), indent=2))
        return 0
    if args.command == "demo":
        runner = run_single_agent if args.mode == "single" else run_multi_agent
        result = runner(args.scenario)
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.patch.validation_passed else 1
    if args.command == "validate":
        result = run_validation(args.scenario, mode=args.mode)
        print(result.log_path)
        return 0 if result.passed else 1
    if args.command == "eval-mock":
        print(run_eval())
        return 0
    if args.command == "matrix":
        print(create_scenario_matrix())
        return 0
    if args.command == "doctor":
        doctor_json = run_doctor()
        doctor_md = render_doctor_markdown(doctor_json)
        print(doctor_json)
        print(doctor_md)
        return 0
    if args.command == "acceptance":
        result = run_acceptance()
        print(result.markdown_path)
        return 0 if result.passed else 1
    if args.command == "report":
        print(create_final_report())
        return 0
    if args.command == "scorecard":
        result = create_scorecard()
        print(result.scorecard_path)
        return 0 if result.status == "PASS" else 1
    if args.command == "poc-repro":
        print(run_poc_repro(runs=args.runs))
        return 0
    if args.command == "list-scenarios":
        for scenario in list_scenarios():
            print(f"{scenario.scenario_id}: {scenario.title} -> {scenario.root_cause_id}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


def _print_help() -> None:
    print(
        """AegisOps Agent targets:
  make setup
  make quickstart
  make test
  make test-app
  make build-index
  make retrieve QUERY="CrashLoopBackOff invalid environment variable"
  make scenario SCENARIO=S1
  make collect-evidence SCENARIO=S1
  make demo SCENARIO=S4 MODE=multi
  make validate SCENARIO=S1
  make eval-mock
  make matrix
  make doctor
  make acceptance
  make scorecard
  make poc RUNS=3
  make docker-build
  make kind-setup
  make report
"""
    )


if __name__ == "__main__":
    raise SystemExit(main())
