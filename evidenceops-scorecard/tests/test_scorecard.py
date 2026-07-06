from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evidenceops_scorecard.scorecard import build_scorecard, display_report_path, render_markdown


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
            self.assertEqual(scorecard["missing_evidence"], [])
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
            self.assertIn("| AegisOps Agent | PASS |", markdown)
            self.assertIn("| Kube Copilot | PASS |", markdown)
            self.assertIn("| Haul Truck Planner | PASS |", markdown)
            self.assertIn("public repository uses synthetic fixtures only", markdown)

    def test_display_report_path_is_repository_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            report_path = repo / "evidenceops-scorecard/reports/evidence-scorecard.md"

            self.assertEqual(
                display_report_path(repo, report_path),
                "evidenceops-scorecard/reports/evidence-scorecard.md",
            )

    def _write_required_public_evidence(self, repo: Path) -> None:
        required_files = [
            "README.md",
            "CLAIMS_MATRIX.md",
            "PORTFOLIO_STATUS.md",
            "PORTFOLIO_STATUS.json",
            "aegisops-agent/reports/final-portfolio-report.md",
            "aegisops-agent/reports/S4/multi/pr-summary.md",
            "kube-copilot/reports/risk-comparison.md",
            "kube-copilot/reports/policy-matrix.md",
            "haul-truck-planner/reports/route-experiment.md",
            "haul-truck-planner/reports/algorithm-comparison.md",
        ]
        for relative_path in required_files:
            path = repo / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".json":
                path.write_text(json.dumps({"overall_portfolio_status": "PASS"}) + "\n", encoding="utf-8")
            else:
                path.write_text(f"# {path.name}\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
