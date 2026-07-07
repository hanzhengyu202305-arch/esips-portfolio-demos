from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evidenceops_scorecard.scorecard import (
    build_release_gate,
    build_scorecard,
    display_report_path,
    render_markdown,
    render_release_gate_markdown,
    write_reports,
)


class EvidenceOpsScorecardTests(unittest.TestCase):
    def test_builds_passing_scorecard_from_required_public_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)

            scorecard = build_scorecard(repo)

            self.assertEqual(scorecard["portfolio_evidence_status"], "PASS")
            self.assertEqual(scorecard["application_submission_status"], "NEEDS_OFFICIAL_CONFIRMATION")
            self.assertEqual(scorecard["summary"]["passed_projects"], 3)
            self.assertEqual(scorecard["summary"]["total_projects"], 3)
            self.assertEqual(scorecard["summary"]["quality_score"], 100)
            self.assertEqual(scorecard["summary"]["weak_evidence"], 0)
            self.assertEqual(scorecard["summary"]["missing_evidence"], 0)
            self.assertEqual(scorecard["missing_evidence"], [])
            self.assertEqual(scorecard["weak_evidence"], [])
            project_names = {project["name"] for project in scorecard["projects"]}
            self.assertEqual(project_names, {"AegisOps Agent", "Kube Copilot", "Haul Truck Planner"})

    def test_missing_required_evidence_fails_scorecard(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            (repo / "kube-copilot/reports/risk-comparison.md").unlink()

            scorecard = build_scorecard(repo)

            self.assertEqual(scorecard["portfolio_evidence_status"], "FAIL")
            self.assertIn("kube-copilot/reports/risk-comparison.md", scorecard["missing_evidence"])
            kube = next(project for project in scorecard["projects"] if project["id"] == "kube-copilot")
            self.assertEqual(kube["status"], "FAIL")

    def test_missing_kube_policy_pack_fails_kube_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            (repo / "kube-copilot/reports/policy-pack.json").unlink()

            scorecard = build_scorecard(repo)

            self.assertEqual(scorecard["portfolio_evidence_status"], "FAIL")
            self.assertIn("kube-copilot/reports/policy-pack.json", scorecard["missing_evidence"])
            kube = next(project for project in scorecard["projects"] if project["id"] == "kube-copilot")
            self.assertEqual(kube["status"], "FAIL")

    def test_weak_evidence_is_reported_without_becoming_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            (repo / "haul-truck-planner/reports/route-experiment.md").write_text(
                "route exists\n",
                encoding="utf-8",
            )

            scorecard = build_scorecard(repo)

            self.assertEqual(scorecard["portfolio_evidence_status"], "WEAK")
            self.assertEqual(scorecard["missing_evidence"], [])
            self.assertIn("haul-truck-planner/reports/route-experiment.md", scorecard["weak_evidence"])
            self.assertLess(scorecard["summary"]["quality_score"], 100)
            haul = next(project for project in scorecard["projects"] if project["id"] == "haul-truck-planner")
            self.assertEqual(haul["status"], "WEAK")
            weak_item = next(item for item in haul["evidence"] if item["path"].endswith("route-experiment.md"))
            self.assertEqual(weak_item["status"], "WEAK")
            self.assertIn("missing keyword: battery", weak_item["quality_issues"])
            self.assertIn("below minimum size", weak_item["quality_issues"][0])

    def test_stale_failed_portfolio_status_does_not_fail_evidence_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            (repo / "PORTFOLIO_STATUS.json").write_text(
                json.dumps({"overall_portfolio_status": "FAIL"}) + "\n",
                encoding="utf-8",
            )

            scorecard = build_scorecard(repo)

            self.assertEqual(scorecard["portfolio_evidence_status"], "PASS")
            self.assertEqual(scorecard["summary"]["portfolio_status_file"], "FAIL")

    def test_renders_markdown_with_boundaries_and_next_steps(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)

            markdown = render_markdown(build_scorecard(repo))

            self.assertIn("# EvidenceOps Scorecard", markdown)
            self.assertIn("Portfolio evidence status: **PASS**", markdown)
            self.assertIn("Application submission status: **NEEDS_OFFICIAL_CONFIRMATION**", markdown)
            self.assertIn("Quality score: **100/100**", markdown)
            self.assertIn("| AegisOps Agent | PASS |", markdown)
            self.assertIn("| Kube Copilot | PASS |", markdown)
            self.assertIn("| Haul Truck Planner | PASS |", markdown)
            self.assertIn("kube-copilot/reports/policy-pack.json", markdown)
            self.assertIn("## Weak Evidence", markdown)
            self.assertIn("public repository uses synthetic fixtures only", markdown)

    def test_release_gate_passes_when_public_evidence_and_validation_are_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            self._write_release_gate_artifacts(repo)

            gate = build_release_gate(repo)

            self.assertEqual(gate["release_gate_status"], "PASS")
            self.assertEqual(gate["required_checks_passed"], 6)
            self.assertEqual(gate["required_checks_total"], 6)
            self.assertEqual(gate["blockers"], [])
            check_names = {check["name"] for check in gate["checks"]}
            self.assertIn("portfolio evidence scorecard", check_names)
            self.assertIn("demo output index", check_names)
            self.assertIn("claim trace", check_names)
            self.assertIn("public boundary check", check_names)

    def test_release_gate_blocks_failed_portfolio_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            self._write_release_gate_artifacts(repo)
            (repo / "PORTFOLIO_STATUS.json").write_text(
                json.dumps(
                    {
                        "overall_portfolio_status": "FAIL",
                        "checks": [
                            {"name": "top-level tests", "status": "PASS"},
                            {"name": "public boundary check", "status": "FAIL"},
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            gate = build_release_gate(repo)

            self.assertEqual(gate["release_gate_status"], "BLOCKED")
            self.assertIn("portfolio status file is FAIL", gate["blockers"])
            self.assertIn("public boundary check did not pass", gate["blockers"])

    def test_release_gate_blocks_missing_demo_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            self._write_release_gate_artifacts(repo)
            (repo / "docs/DEMO_OUTPUT_INDEX.md").unlink()

            gate = build_release_gate(repo)

            self.assertEqual(gate["release_gate_status"], "BLOCKED")
            self.assertIn("docs/DEMO_OUTPUT_INDEX.md is missing", gate["blockers"])

    def test_release_gate_accepts_lowercase_claim_trace_boundary_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            self._write_release_gate_artifacts(repo)
            (repo / "docs/REVIEWER_CLAIM_TRACE.md").write_text(
                "# Reviewer Claim Trace\n\n| claim | boundary |\n| --- | --- |\n| demo | synthetic fixtures only |\n",
                encoding="utf-8",
            )

            gate = build_release_gate(repo)

            self.assertEqual(gate["release_gate_status"], "PASS")

    def test_release_gate_markdown_is_reviewer_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            self._write_release_gate_artifacts(repo)

            markdown = render_release_gate_markdown(build_release_gate(repo))

            self.assertTrue(markdown.startswith("# EvidenceOps Release Gate"))
            self.assertIn("Release gate status: **PASS**", markdown)
            self.assertIn("| check | status | evidence |", markdown)
            self.assertIn("## Boundary", markdown)
            self.assertIn("not official application approval", markdown)

    def test_write_reports_outputs_release_gate_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            self._write_release_gate_artifacts(repo)

            paths = write_reports(repo)

            self.assertIn("release_gate_json", paths)
            self.assertIn("release_gate_markdown", paths)
            self.assertTrue(paths["release_gate_json"].is_file())
            self.assertTrue(paths["release_gate_markdown"].is_file())
            payload = json.loads(paths["release_gate_json"].read_text(encoding="utf-8"))
            self.assertEqual(payload["release_gate_status"], "PASS")

    def test_release_gate_cli_exits_nonzero_when_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._write_required_public_evidence(repo)
            out_dir = repo / "out"

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "evidenceops_scorecard.scorecard",
                    "--root",
                    str(repo),
                    "--out-dir",
                    str(out_dir),
                    "--release-gate",
                ],
                cwd=Path(__file__).resolve().parents[1],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("release-gate.md", completed.stdout)
            payload = json.loads((out_dir / "release-gate.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["release_gate_status"], "BLOCKED")

    def test_display_report_path_is_repository_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            report_path = repo / "evidenceops-scorecard/reports/evidence-scorecard.md"

            self.assertEqual(
                display_report_path(repo, report_path),
                "evidenceops-scorecard/reports/evidence-scorecard.md",
            )

    def _write_required_public_evidence(self, repo: Path) -> None:
        required_files = {
            "README.md": "AI software engineering with validation. EvidenceOps portfolio evidence and reviewer guide.\n",
            "CLAIMS_MATRIX.md": "Claims Matrix with evidence, verified Boundary notes, and safe claims.\n",
            "PORTFOLIO_STATUS.md": "Overall status PASS with portfolio-check validation and boundary notes.\n",
            "PORTFOLIO_STATUS.json": json.dumps({"overall_portfolio_status": "PASS"}) + "\n",
            "aegisops-agent/reports/final-portfolio-report.md": "AegisOps Agent evidence: root cause, validation, report, and patch preview.\n",
            "aegisops-agent/reports/S4/multi/pr-summary.md": "S4 PR summary with evidence, root cause, validation, and human review.\n",
            "kube-copilot/reports/risk-comparison.md": "Kube Copilot Kubernetes risk comparison with PASS FAIL policy validation and manual review.\n",
            "kube-copilot/reports/policy-matrix.md": "Policy matrix with image, resources, probes, securityContext, and CI validation.\n",
            "kube-copilot/reports/policy-pack.json": json.dumps(
                {
                    "pack_id": "kube-copilot-predeploy",
                    "rules": [{"id": "KC001_IMAGE_TAG_PINNED", "severity": "blocking"}],
                    "trust_boundary": "generated Kubernetes artifacts still require human review",
                }
            )
            + "\n",
            "kube-copilot/reports/policy-pack.md": "Kube Copilot Policy Pack with policy rules, validation, evidence, and human review boundary.\n",
            "haul-truck-planner/reports/route-experiment.md": "Route experiment with battery reserve, charging, grade, risk, Dijkstra, and A*.\n",
            "haul-truck-planner/reports/algorithm-comparison.md": "Algorithm comparison for shortest path, Dijkstra, A*, energy, and charging.\n",
        }
        for relative_path, contents in required_files.items():
            path = repo / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".json":
                path.write_text(contents, encoding="utf-8")
            else:
                path.write_text(contents * 4, encoding="utf-8")

    def _write_release_gate_artifacts(self, repo: Path) -> None:
        (repo / "docs").mkdir(parents=True, exist_ok=True)
        (repo / "docs/DEMO_OUTPUT_INDEX.md").write_text(
            "Overall demo status: **PASS**\nKube Policy Pack\nEvidenceOps Scorecard\n",
            encoding="utf-8",
        )
        (repo / "docs/REVIEWER_CLAIM_TRACE.md").write_text(
            "# Reviewer Claim Trace\nverified by `make demo-all` and `make portfolio-check`\nBoundary\n",
            encoding="utf-8",
        )
        (repo / "PORTFOLIO_STATUS.json").write_text(
            json.dumps(
                {
                    "overall_portfolio_status": "PASS",
                    "checks": [
                        {"name": "top-level tests", "status": "PASS"},
                        {"name": "AegisOps acceptance", "status": "PASS"},
                        {"name": "Kube Copilot report", "status": "PASS"},
                        {"name": "Kube Policy Pack", "status": "PASS"},
                        {"name": "Haul Truck Planner report", "status": "PASS"},
                        {"name": "EvidenceOps scorecard", "status": "PASS"},
                        {"name": "public boundary check", "status": "PASS"},
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
