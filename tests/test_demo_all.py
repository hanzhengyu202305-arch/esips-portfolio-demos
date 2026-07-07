from __future__ import annotations

import unittest
from pathlib import Path

from scripts.demo_all import DemoResult, build_demo_runs, render_index


ROOT = Path(__file__).resolve().parents[1]


class DemoAllTests(unittest.TestCase):
    def test_makefile_exposes_demo_all_target(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertIn("demo-all:", makefile)
        self.assertIn("scripts/demo_all.py", makefile)

    def test_portfolio_check_generates_kube_policy_pack_before_scorecard(self):
        script = (ROOT / "scripts" / "portfolio_check.py").read_text(encoding="utf-8")

        policy_pack_position = script.index('"Kube Policy Pack"')
        scorecard_position = script.index('"EvidenceOps scorecard"')
        self.assertLess(policy_pack_position, scorecard_position)
        self.assertIn('"policy-pack"', script)

    def test_demo_all_includes_aegisops_triage_queue(self):
        runs = build_demo_runs("python3")
        triage = next(run for run in runs if run.name == "AegisOps Triage Queue")

        self.assertEqual(triage.display_command, "make -C aegisops-agent triage PYTHON=<python>")
        self.assertIn("aegisops-agent/reports/triage-queue.md", triage.reports)

    def test_demo_all_includes_patch_risk_diff(self):
        runs = build_demo_runs("python3")
        patch_risk = next(run for run in runs if run.name == "Patch Risk Diff")

        self.assertEqual(patch_risk.display_command, "make -C aegisops-agent patch-risk SCENARIO=S4 MODE=multi PYTHON=<python>")
        self.assertIn("aegisops-agent/reports/S4/multi/patch-risk-diff.md", patch_risk.reports)

    def test_demo_all_includes_kube_policy_pack_exporter(self):
        runs = build_demo_runs("python3")
        policy_pack = next(run for run in runs if run.name == "Kube Policy Pack")

        self.assertEqual(policy_pack.display_command, "make -C kube-copilot policy-pack")
        self.assertIn("kube-copilot/reports/policy-pack.json", policy_pack.reports)
        self.assertIn("kube-copilot/reports/policy-pack.md", policy_pack.reports)

    def test_render_index_lists_all_public_evidence_paths(self):
        markdown = render_index(
            [
                DemoResult(
                    name="AegisOps Agent",
                    display_command="make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=<python>",
                    purpose="issue evidence -> RCA -> patch preview -> validation -> PR-style report",
                    reports=(
                        "aegisops-agent/reports/S4/multi/issue-to-pr-report.md",
                        "aegisops-agent/reports/S4/multi/pr-summary.md",
                    ),
                    returncode=0,
                ),
                DemoResult(
                    name="Kube Copilot",
                    display_command="make -C kube-copilot report",
                    purpose="generated Kubernetes/CI artifacts -> deterministic policy findings",
                    reports=("kube-copilot/reports/risk-comparison.md",),
                    returncode=0,
                ),
                DemoResult(
                    name="Haul Truck Planner",
                    display_command="make -C haul-truck-planner report",
                    purpose="energy-aware planning",
                    reports=(
                        "haul-truck-planner/reports/route-experiment.md",
                        "haul-truck-planner/reports/sensitivity-lab.md",
                    ),
                    returncode=0,
                ),
                DemoResult(
                    name="EvidenceOps Scorecard",
                    display_command="make -C evidenceops-scorecard report",
                    purpose="portfolio evidence inventory",
                    reports=("evidenceops-scorecard/reports/evidence-scorecard.md",),
                    returncode=0,
                ),
            ]
        )

        self.assertIn("Overall demo status: **PASS**", markdown)
        self.assertIn("AegisOps Agent", markdown)
        self.assertIn("Kube Copilot", markdown)
        self.assertIn("Haul Truck Planner", markdown)
        self.assertIn("EvidenceOps Scorecard", markdown)
        self.assertIn("aegisops-agent/reports/S4/multi/pr-summary.md", markdown)
        self.assertIn("kube-copilot/reports/risk-comparison.md", markdown)
        self.assertIn("haul-truck-planner/reports/route-experiment.md", markdown)
        self.assertIn("haul-truck-planner/reports/sensitivity-lab.md", markdown)
        self.assertIn("evidenceops-scorecard/reports/evidence-scorecard.md", markdown)
        self.assertIn("does not prove production readiness", markdown)

    def test_render_index_surfaces_failed_run(self):
        markdown = render_index(
            [
                DemoResult(
                    name="AegisOps Agent",
                    display_command="make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=<python>",
                    purpose="issue evidence",
                    reports=("aegisops-agent/reports/S4/multi/pr-summary.md",),
                    returncode=2,
                )
            ]
        )

        self.assertIn("Overall demo status: **FAIL**", markdown)
        self.assertIn("| AegisOps Agent | FAIL |", markdown)


if __name__ == "__main__":
    unittest.main()
