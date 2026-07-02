import unittest

from kube_copilot.generator import generate_workspace
from kube_copilot.risk_report import compare_safe_and_risky_workspace
from kube_copilot.validator import validate_workspace


class KubeCopilotTests(unittest.TestCase):
    def test_generates_expected_kubernetes_and_ci_artifacts(self):
        workspace = generate_workspace(
            app_name="ore-api",
            image="ghcr.io/example/ore-api:1.2.0",
            port=8080,
            replicas=3,
            cpu_limit="500m",
            memory_limit="512Mi",
        )

        self.assertIn("Dockerfile", workspace.files)
        self.assertIn("k8s/deployment.yaml", workspace.files)
        self.assertIn("k8s/service.yaml", workspace.files)
        self.assertIn(".github/workflows/ci.yml", workspace.files)
        self.assertIn("ore-api", workspace.files["k8s/deployment.yaml"])
        self.assertIn("ghcr.io/example/ore-api:1.2.0", workspace.files["k8s/deployment.yaml"])
        self.assertIn("requests:", workspace.files["k8s/deployment.yaml"])
        self.assertIn("livenessProbe:", workspace.files["k8s/deployment.yaml"])
        self.assertIn("type: ClusterIP", workspace.files["k8s/service.yaml"])

    def test_validator_flags_missing_limits_and_latest_tag(self):
        workspace = generate_workspace(
            app_name="risky-api",
            image="example/risky-api:latest",
            port=8000,
            replicas=1,
            cpu_limit="",
            memory_limit="",
        )

        report = validate_workspace(workspace)

        self.assertFalse(report.passed)
        self.assertIn("image tag must not be latest", report.findings)
        self.assertIn("cpu limit is required", report.findings)
        self.assertIn("memory limit is required", report.findings)
        self.assertIn("cpu request is required", report.findings)
        self.assertIn("memory request is required", report.findings)

    def test_validator_flags_missing_liveness_probe(self):
        workspace = generate_workspace(
            app_name="probe-api",
            image="ghcr.io/example/probe-api:1.0.0",
            port=8000,
            replicas=2,
            cpu_limit="500m",
            memory_limit="512Mi",
        )
        workspace.files["k8s/deployment.yaml"] = workspace.files["k8s/deployment.yaml"].replace(
            "          livenessProbe:\n"
            "            httpGet:\n"
            "              path: /health\n"
            "              port: 8000\n"
            "            initialDelaySeconds: 15\n"
            "            periodSeconds: 20\n",
            "",
        )

        report = validate_workspace(workspace)

        self.assertFalse(report.passed)
        self.assertIn("liveness probe is required", report.findings)

    def test_risk_report_compares_safe_and_risky_generation(self):
        markdown = compare_safe_and_risky_workspace()

        self.assertIn("| safe | PASS |", markdown)
        self.assertIn("| risky | FAIL |", markdown)
        self.assertIn("image tag must not be latest", markdown)
        self.assertIn("## Remediation checklist", markdown)
        self.assertIn("Pin image tags to immutable versions", markdown)
        self.assertIn("Set CPU and memory requests and limits", markdown)
        self.assertIn("Validate probes before rollout", markdown)
        self.assertIn("Accenture_01 Kubernetes_DevOps", markdown)
        self.assertIn("Kubernetes-based CI/CD pipeline", markdown)
        self.assertIn("generated YAML is not production-ready until it passes policy checks", markdown)


if __name__ == "__main__":
    unittest.main()
